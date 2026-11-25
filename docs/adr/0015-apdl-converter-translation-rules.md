# Special-case APDL converter translations that generic rules get wrong

The APDL-to-Python converter in `convert.py` maps commands by prefix and emits generic code, which fails in three known cases. `FORCED_MAPPING` maps `SECT` to `sectype`, because prefix matching in `FileTranslator.find_match` would otherwise resolve it to `sectinqr`. Inside a `non_interactive` block, `*GET` is emitted through `store_run_command` (`mapdl.run`) instead of `mapdl.get`, because `mapdl.get` needs an immediate response that buffered non-interactive commands cannot return. `_convert` detects the line ending (`\r\n` or `\n`) from the input text rather than using `os.linesep`, because input files often come from another OS than the one running the conversion.

## Consequences

- New prefix collisions must be added to `FORCED_MAPPING`.
- `*GET` inside `non_interactive` does not return a Python value.
- Conversion output does not depend on the host OS line separator.
