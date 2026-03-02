# PyMAPDL AI Agents - Quick Reference Card

## 🤖 Available Agents

### 📚 Documentation Specialist
**When to use**: Doc changes, docstring validation, spelling/style checks

**Key commands**:
```bash
cd doc && make html                    # Build docs
vale doc/source/                       # Check style
uv run codespell doc/ src/            # Check spelling
```

**Checklist**:
- [ ] Numpydoc-style docstrings with examples
- [ ] Google documentation style
- [ ] Links added to `doc/source/links.rst`
- [ ] Technical terms in `accept.txt` if needed
- [ ] Vale and codespell pass

---

### 💻 PyMAPDL Developer
**When to use**: New features, bug fixes, code optimization

**Key commands**:
```bash
uv run pre-commit install              # Setup hooks
uv run pre-commit run --all-files      # Run all checks
uv run mypy src/ --config-file=pyproject.toml
```

**Checklist**:
- [ ] Code follows repository patterns
- [ ] Type hints used appropriately
- [ ] Cannot modify `src/ansys/mapdl/core/_commands/`
- [ ] Override in `_MapdlCommandExtended` if needed
- [ ] Pre-commit hooks pass
- [ ] Tests added (coordinate with Test Engineer)
- [ ] Documentation added (coordinate with Doc Specialist)

---

### 🧪 Test Engineer
**When to use**: Writing tests, improving coverage, mocking strategies

**Key commands**:
```bash
# Without MAPDL instance (recommended)
export PYMAPDL_START_INSTANCE=False
export TESTING_MINIMAL=YES
uv run pytest --cov=src/ansys/mapdl/core --cov-report=html

# Run specific tests
uv run pytest tests/test_file.py -v
uv run pytest -p no:randomly --maxfail=100
```

**Checklist**:
- [ ] Target ~90% coverage
- [ ] Mock MAPDL instances (avoid launching)
- [ ] Use `requires()` decorator for conditional tests
- [ ] Tests work in local and remote modes
- [ ] No flaky/intermittent failures

**Mocking example**:
```python
from unittest.mock import Mock, patch


def test_feature():
    mock_mapdl = Mock()
    mock_mapdl.run.return_value = "Expected"
    # Test logic
```

---

### 👀 Code Reviewer
**When to use**: PR reviews before merge

**Key commands**:
```bash
# Complete review
uv run pre-commit run --all-files
uv run pytest --cov=src/ansys/mapdl/core --cov-report=term
cd doc && make clean && make html
uv run bandit -c pyproject.toml -r src/
```

**PR Checklist**:
- [ ] All CI checks passing
- [ ] Pre-commit hooks pass
- [ ] Documentation complete
- [ ] Test coverage >= 90%
- [ ] No security issues (bandit)
- [ ] Breaking changes documented
- [ ] Changelog entry added

---

## 🔄 Typical Workflow

```
Developer → Writes code
    ↓
Test Engineer → Adds tests with mocking
    ↓
Documentation Specialist → Adds docs & examples
    ↓
Code Reviewer → Reviews everything → ✅ Merge
```

## 🛠️ Environment Setup

```bash
# Install dependencies
uv sync

# Setup pre-commit
uv run pre-commit install

# Run without MAPDL (for testing)
export PYMAPDL_START_INSTANCE=False
export TESTING_MINIMAL=YES
```

## 📍 Key Files

- `AGENTS.md` - Complete agent specifications
- `.github/AGENTS_GUIDE.md` - Detailed usage guide
- `pyproject.toml` - Configuration & dependencies
- `.pre-commit-config.yaml` - Code quality checks
- `tests/conftest.py` - Test fixtures & helpers
- `doc/source/links.rst` - Documentation links
- `doc/styles/` - Vale style rules

## 🔗 Using with LLMs

**GitHub Copilot (VS Code)**:
```
@workspace Use the [Agent Name] to [task]
```

**Other IDEs**:
```
Acting as the [Agent Name] from AGENTS.md, help me [task]
```

## 📚 More Information

- Full details: `AGENTS.md`
- Usage guide: `.github/AGENTS_GUIDE.md`
- Contributing: `CONTRIBUTING.md`
- PyMAPDL Docs: https://mapdl.docs.pyansys.com/

---

**Remember**: All agents share the same Python environment setup. Always use `uv` for dependency management and run pre-commit before committing!
