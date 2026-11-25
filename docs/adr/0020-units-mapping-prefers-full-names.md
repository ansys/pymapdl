# Never let a unit short name overwrite a full-name entry

The units mapping in `information.py` is a case-insensitive `dict` subclass. `_parse_units` stores each unit under its lowercased full name and, if available, its short name, but only when the short-name key is not already present. That check uses `super().__contains__()` to inspect the actual dict without the class's own case conversion, so a short name never overwrites an existing full-name entry.

## Consequences

- Full-name lookups always return the value parsed for that full name.
- When a short name collides with an existing key, the short name is not stored.
