"""Shared scalar validators for task readers and completion proposal gates."""


def text(value):
    return isinstance(value, str) and bool(value.strip())


def sha256(value):
    return (isinstance(value, str) and len(value) == 64
            and all(character in '0123456789abcdef' for character in value))
