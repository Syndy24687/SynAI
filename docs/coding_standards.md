# Coding Standards

## Python

- Python 3.13+
- Use type hints everywhere.
- Use dataclasses where appropriate.
- Use pathlib instead of os whenever possible.
- Use logging instead of print().
- Prefer composition over inheritance.

---

## Functions

- Keep functions under 40 lines whenever practical.
- One responsibility per function.
- Avoid nested logic deeper than three levels.

---

## Classes

- One responsibility.
- Constructor should remain lightweight.
- Use dependency injection.

---

## Documentation

Every public function must contain a docstring.

Example

```python
def speak(text: str) -> None:
    """
    Convert text into speech.

    Args:
        text: Text to be spoken.
    """
```

---

## Imports

Standard library

↓

Third-party

↓

Project imports

---

## Logging

Never use

```python
print()
```

Always use

```python
logger.info(...)
```

---

## Naming

snake_case

PascalCase

UPPER_CASE constants

---

## Comments

Explain WHY

Not WHAT