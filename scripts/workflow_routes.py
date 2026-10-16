"""Read-only route contract used by validation; not a hook or model selector."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_routes(root=ROOT):
    return json.loads((Path(root) / 'references/workflow-routing.json').read_text(encoding='utf-8'))


def resolve(name, arguments='', root=ROOT):
    """Translate one explicit legacy name without changing its trailing scope."""
    routes = load_routes(root)
    if name in routes['primary'] + routes['specialized'] + routes['shortcuts']:
        return name, arguments
    route = routes['redirects'].get(name)
    if route is None:
        raise ValueError('Unknown Hirameki workflow: ' + name)
    remaining = arguments.strip()
    parts = remaining.split(maxsplit=1)
    first = parts[0] if parts else ''
    variant = route.get('variants', {}).get(first)
    if variant:
        route = variant
        remaining = parts[1] if len(parts) == 2 else ''
    return route['target'], ' '.join(part for part in (route['mode'], remaining) if part)


def task_contract(root, name):
    """Resolve the task capability preserved behind the legacy redirect."""
    root = Path(root)
    return root / ('capabilities/tasks.md' if name == 'tasks' else name + '.md')
