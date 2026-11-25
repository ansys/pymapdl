# Check only the lowest license tier, via library-controlled `subprocess` calls

The license checker in `licensing.py` runs Ansys utilities such as `ansysli_util` with `subprocess` (`import subprocess  # nosec B404`, `subprocess.Popen(...)  # nosec B603`). The bandit checks are excluded because the executable path (`ansysli_util_path`) and arguments are built by the library, not taken from user input. Of the available licenses (`Ansys` Enterprise, `meba`, `mech_2`, `mech_1`), the checker checks only `mech_1` (Pro, the most limited), because PyMAPDL only needs to know a solve is possible and the check is kept general.

## Consequences

- Any future change that passes user input to these `subprocess` calls invalidates the `# nosec` exemptions.
- The checker cannot tell which higher tier is available; a warning for insufficient license rights is not implemented.
