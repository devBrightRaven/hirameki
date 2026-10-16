"""Canonical restore schemas and canonical-JSON digest used by the reader."""
import hashlib
import json
from datetime import datetime

from task_contract_primitives import text, sha256


def offset_timestamp(value):
    if not isinstance(value, str) or 'T' not in value:
        return False
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).utcoffset() is not None
    except ValueError:
        return False


def digest(value, excluded=None):
    data = {key: item for key, item in value.items() if key != excluded}
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':'), allow_nan=False).encode('utf-8')).hexdigest()


def obj(properties):
    return {'type': 'object', 'required': list(properties), 'properties': properties,
            'additionalProperties': True}


STRING = {'type': 'string', 'minLength': 1}
TEXT = {'type': 'string', 'format': 'nonblank'}
HASH = {'type': 'string', 'format': 'sha256-lowercase'}
TIME = {'type': 'string', 'format': 'timestamp-with-offset'}
OP = {'type': 'string', 'const': 'restore'}
VERSION = {'type': 'integer', 'const': 1}
REQUEST_SCHEMA = obj({
    'schema_version': VERSION, 'request_id': STRING, 'task_id': STRING,
    'base_index_revision': HASH, 'base_task_revision': {'type': 'integer', 'minimum': 1},
    'base_source_digests': {'type': 'object', 'minProperties': 1,
                          'propertyNames': TEXT, 'additionalProperties': HASH},
    'reason': STRING,
    'reason_kind': {'type': 'string', 'enum': ['archival_error', 'scope_changed', 'reopened', 'unknown']},
    'created': TIME,
    'approval': obj({'source_ref': TEXT, 'approving_user': TEXT, 'operation': OP, 'scope': TEXT}),
    'payload_digest': HASH,
})
APPROVAL_SCHEMA = obj({
    'schema_version': VERSION, 'approval_id': TEXT, 'request_id': TEXT, 'task_id': TEXT,
    'request_digest': TEXT, 'operation': OP, 'approved_at': TIME,
    'source_ref': TEXT, 'recorded_by': TEXT,
})


def matches(value, schema):
    kind = schema['type']
    if kind == 'string':
        if not isinstance(value, str) or len(value) < schema.get('minLength', 0):
            return False
        validators = {'nonblank': text, 'sha256-lowercase': sha256,
                      'timestamp-with-offset': offset_timestamp}
        if schema.get('format') and not validators[schema['format']](value):
            return False
    elif kind == 'integer':
        if type(value) is not int or value < schema.get('minimum', value):
            return False
    elif kind == 'object':
        if not isinstance(value, dict) or len(value) < schema.get('minProperties', 0):
            return False
        properties = schema.get('properties', {})
        if not all(key in value for key in schema.get('required', [])):
            return False
        for key, item in value.items():
            if schema.get('propertyNames') and not matches(key, schema['propertyNames']):
                return False
            child = properties.get(key, schema.get('additionalProperties', True))
            if isinstance(child, dict) and not matches(item, child):
                return False
    return (('const' not in schema or value == schema['const'])
            and ('enum' not in schema or value in schema['enum']))


def request_valid(record):
    return (matches(record, REQUEST_SCHEMA)
            and record['approval']['scope'] == record['task_id']
            and record['payload_digest'] == digest(record, 'payload_digest'))


def approval_valid(record):
    return matches(record, APPROVAL_SCHEMA)


MATCH_FIELDS = [('request_id', 'request_id'), ('task_id', 'task_id'),
                ('request_digest', 'payload_digest'), ('operation', 'approval.operation')]


def approval_matches_request(approval, request):
    for approval_key, request_key in MATCH_FIELDS:
        expected = request['approval']['operation'] if request_key == 'approval.operation' else request[request_key]
        if approval.get(approval_key) != expected:
            return False
    return True


def pair_errors(request, approval):
    errors = []
    if not request_valid(request): errors.append('request-digest-or-schema')
    if not approval_valid(approval): errors.append('invalid-approval')
    if not errors and not approval_matches_request(approval, request):
        errors.append('request-approval-mismatch')
    return errors


def public_contract():
    return {
        'contract': 'hirameki-restore-v1', 'read_only': True,
        'schemas': {'request': REQUEST_SCHEMA, 'approval_record': APPROVAL_SCHEMA},
        'formats': {'nonblank': 'string containing a non-whitespace character',
                    'sha256-lowercase': '64 lowercase hexadecimal characters',
                    'timestamp-with-offset': 'ISO datetime containing T and UTC offset; Z accepted'},
        'digest': {'algorithm': 'SHA-256', 'encoding': 'UTF-8', 'sort_keys': True,
                   'ensure_ascii': False, 'separators': [',', ':'], 'allow_nan': False,
                   'request_excluded_field': 'payload_digest',
                   'python': "hashlib.sha256(json.dumps({k:v for k,v in request.items() if k != 'payload_digest'},sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf-8')).hexdigest()",
                   'file_hash_is_not_payload_digest': True},
        'bindings': ['request.approval.scope == request.task_id'] +
                    ['approval.' + a + ' == request.' + b for a, b in MATCH_FIELDS],
        'validate_pair': 'reader --validate-restore; JSON stdin {request, approval_record}; nonzero on mismatch; no vault or file writes',
        'record_locations': {'request': 'restore-requests/<request_id>.json',
                             'approval_record': 'restore-approvals/<approval_id>.json'},
        'source_map': {'base_index_revision': 'task query.index_revision',
                       'base_task_revision': 'task query.task.revision',
                       'base_source_digests': 'task query.validation.expected_source_digests',
                       'approval.scope': 'selected task_id',
                       'request_digest': 'completed request.payload_digest'},
        'steps': ['resolve entry and bundled reader/gate', 'read this contract',
                  'task-ID query and inspect full target/global validation',
                  'obtain explicit user-approved scope and source reference',
                  'build request in memory and compute payload_digest',
                  'build matching approval record in memory',
                  'exclusive-create approval file, then request file',
                  'immediate task-ID query; retain global diagnostics and pending request IDs'],
        'limits': ['schema matching does not establish human consent',
                   'do not write index or execute underlying task',
                   'if second file save fails, report partial state; never overwrite or delete evidence',
                   'unknown ID, invalid/unavailable target or output-limit-exceeded is not a successful inspection'],
    }
