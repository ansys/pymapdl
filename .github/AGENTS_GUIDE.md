# PyMAPDL Specialized Agents Guide

This guide explains how to effectively use the specialized AI agents configured for the PyMAPDL repository.

## Quick Reference

| Agent | Primary Use Case | Key Command |
|-------|-----------------|-------------|
| **Documentation Specialist** | Review docs, check spelling, validate docstrings | `cd doc && make html` |
| **PyMAPDL Developer** | Write features, fix bugs, optimize code | `uv run pre-commit run --all-files` |
| **Test Engineer** | Write tests, ensure coverage, minimize MAPDL usage | `uv run pytest --cov=src/ansys/mapdl/core` |
| **Code Reviewer** | Comprehensive PR review before merge | Review all of the above |

## Using Agents with GitHub Copilot

### In VS Code

When using GitHub Copilot Chat in VS Code, you can reference these agents:

```
@workspace Use the PyMAPDL Developer agent to add a new feature for [describe feature]
```

```
@workspace Use the Documentation Specialist agent to review the docstrings in this file
```

```
@workspace Use the Test Engineer agent to add tests for this new method
```

```
@workspace Use the Code Reviewer agent to review this PR
```

### In Other IDEs (Cursor, JetBrains, etc.)

Most modern IDEs with LLM integration can access the `AGENTS.md` file. Simply:

1. Reference the agent in your prompt:
   ```
   Acting as the Test Engineer agent from AGENTS.md, help me write tests for...
   ```

2. Or ask the LLM to read the file:
   ```
   Read AGENTS.md and use the Documentation Specialist agent guidelines to...
   ```

## Typical Workflows

### Adding a New Feature

1. **Developer Agent**: Implements the feature
   ```python
   # Developer writes the feature code in src/ansys/mapdl/core/
   ```

2. **Test Engineer Agent**: Adds comprehensive tests
   ```python
   # Tests in tests/test_new_feature.py with mocking
   from unittest.mock import Mock, patch


   def test_new_feature():
       mock_mapdl = Mock()
       # Test implementation
   ```

3. **Documentation Specialist Agent**: Documents the feature
   - Updates user guide in `doc/source/user_guide/`
   - Ensures numpydoc docstrings with examples
   - Adds links to `doc/source/links.rst` if needed
   - Considers adding example to `examples/` gallery

4. **Code Reviewer Agent**: Reviews everything before merge
   - Runs all checks
   - Verifies quality standards met
   - Approves PR

### Fixing a Bug

1. **Developer Agent**: Analyzes and fixes the bug
2. **Test Engineer Agent**: Adds regression test
3. **Code Reviewer Agent**: Verifies fix and reviews

### Improving Documentation

1. **Documentation Specialist Agent**: Primary agent
   - Reviews documentation changes
   - Runs vale and codespell
   - Ensures proper style and formatting

2. **Code Reviewer Agent**: Final review before merge

### PR Review Process

1. **Code Reviewer Agent** orchestrates the review:
   - Checks code quality (Developer agent expertise)
   - Verifies test coverage (Test Engineer agent expertise)
   - Validates documentation (Documentation Specialist agent expertise)
   - Ensures all CI checks pass
   - Provides comprehensive feedback

## Agent-Specific Commands

### Documentation Specialist

```bash
# Check spelling
uv run codespell doc/ src/

# Run vale linter
vale doc/source/

# Build documentation
cd doc
make clean
make html

# Add word to dictionary
echo "your_technical_term" >> doc/styles/config/vocabularies/ANSYS/accept.txt
```

### PyMAPDL Developer

```bash
# Install pre-commit hooks
uv run pre-commit install

# Run all pre-commit checks
uv run pre-commit run --all-files

# Run specific checks
uv run black src/
uv run isort src/
uv run flake8 src/

# Type checking
uv run mypy src/ --follow-imports=silent --config-file=pyproject.toml

# Security scan
uv run bandit -c pyproject.toml -r src/
```

### Test Engineer

```bash
# Run tests without MAPDL instance (recommended for development)
export PYMAPDL_START_INSTANCE=False
export TESTING_MINIMAL=YES
uv run pytest

# Run with coverage
uv run pytest --cov=src/ansys/mapdl/core --cov-report=html --cov-report=term

# Run specific test file
uv run pytest tests/test_specific.py -v

# Run without random order for debugging
uv run pytest -p no:randomly --maxfail=100 tests/test_foo.py

# Run only fast tests (skip slow integration tests)
uv run pytest -m "not slow"
```

### Code Reviewer

```bash
# Complete review checklist
uv run pre-commit run --all-files
uv run pytest --cov=src/ansys/mapdl/core --cov-report=term
cd doc && make clean && make html
cd ..
uv run bandit -c pyproject.toml -r src/

# Review PR from command line
gh pr checkout 123
uv run pre-commit run --all-files
uv run pytest
```

## Configuration Files

All agents reference these key configuration files:

- **`AGENTS.md`**: Complete agent specifications (this is the source of truth)
- **`pyproject.toml`**: Python project configuration, dependencies, tool settings
- **`.pre-commit-config.yaml`**: Code quality checks that run before commits
- **`doc/.vale.ini`**: Vale linting configuration for documentation
- **`doc/styles/`**: Vale style rules and vocabulary
- **`tests/conftest.py`**: Pytest fixtures and test utilities
- **`codecov.yml`**: Test coverage requirements

## Best Practices

### For Developers

1. **Always run pre-commit** before pushing:
   ```bash
   uv run pre-commit run --all-files
   ```

2. **Use mocking in tests** to avoid launching MAPDL:
   ```python
   from unittest.mock import Mock

   mock_mapdl = Mock()
   ```

3. **Write docstrings with examples**:
   ```python
   def my_function(param: str) -> int:
       """Short summary.

       Parameters
       ----------
       param : str
           Description of param.

       Returns
       -------
       int
           Description of return value.

       Examples
       --------
       >>> my_function("test")
       42
       """
   ```

### For Documentation

1. **Add new links to links.rst**:
   ```rst
   .. _my_new_link: https://example.com/
   ```

2. **Use vale-friendly technical terms** or add to accept.txt

3. **Follow Google documentation style**

### For Testing

1. **Target ~90% coverage** for new code

2. **Use requires() decorator** for conditional tests:
   ```python
   from conftest import requires


   @requires("local")
   def test_local_only(mapdl): ...
   ```

3. **Write deterministic tests** - no flaky tests!

## Troubleshooting

### Agent Not Following Guidelines

If an AI agent isn't following the AGENTS.md guidelines:

1. Explicitly reference the agent: "Act as the [Agent Name] from AGENTS.md"
2. Point to specific sections: "Follow the responsibilities in AGENTS.md for [Agent Name]"
3. Ensure the LLM has access to the file in its context

### CI Failures

1. Run pre-commit locally first
2. Check coverage requirements
3. Ensure tests pass with mocked MAPDL
4. Review error messages from CI logs

### Documentation Build Failures

1. Check for RST syntax errors
2. Run vale and codespell locally
3. Verify all cross-references exist
4. Check Sphinx warnings in build output

## Contributing

When contributing to PyMAPDL:

1. Read `CONTRIBUTING.md` for general guidelines
2. Reference the appropriate agent in `AGENTS.md` for specific tasks
3. Ensure your work meets the standards defined by the relevant agent
4. Have the Code Reviewer agent review before submitting PR

## Additional Resources

- [PyMAPDL Documentation](https://mapdl.docs.pyansys.com/)
- [PyAnsys Developer Guide](https://dev.docs.pyansys.com/)
- [Numpydoc Style Guide](https://numpydoc.readthedocs.io/)
- [Google Documentation Style Guide](https://developers.google.com/style)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)

---

**Note**: This guide complements the detailed specifications in `AGENTS.md`. Always refer to `AGENTS.md` for authoritative agent behavior and responsibilities.
