# PyMAPDL Agents Configuration - Summary

## What Was Created

This configuration adds four specialized AI agents to help with PyMAPDL development, testing, documentation, and code review. The agents work with any LLM-enabled IDE or tool (GitHub Copilot, Cursor, JetBrains AI, Claude, ChatGPT, etc.).

## Files Created/Modified

### Created Files:

1. **`AGENTS.md`** (21,728 bytes)
   - Primary source of truth for all agent specifications
   - Contains detailed responsibilities, expertise areas, and key commands
   - Includes common knowledge sections (PyMAPDL modes, testing, etc.)
   - 498 lines of comprehensive agent documentation

2. **`.github/AGENTS_GUIDE.md`** (8,126 bytes)
   - Practical usage guide for developers
   - IDE-specific integration examples
   - Typical workflows and best practices
   - Troubleshooting common issues
   - Command reference for each agent

3. **`.github/AGENTS_QUICKREF.md`** (3,987 bytes)
   - One-page quick reference card
   - Key commands for each agent
   - Checklists for common tasks
   - Easy-to-scan format for quick lookups

### Modified Files:

4. **`README.md`**
   - Added "AI-Assisted Development with Specialized Agents" section
   - Links to AGENTS.md and AGENTS_GUIDE.md
   - Positioned under Contributing section for visibility

## The Four Agents

### 1. Documentation Specialist 📚
**Focus**: Technical documentation quality

**Key capabilities**:
- Reviews `.md`, `.rst`, and doc files
- Validates numpydoc-style docstrings
- Runs codespell and vale for spelling/style
- Maintains `links.rst`
- Suggests example gallery additions
- Ensures Google documentation style compliance

**Primary tools**: `vale`, `codespell`, `sphinx`, `numpydoc-validation`

---

### 2. PyMAPDL Developer 💻
**Focus**: Feature development and bug fixes

**Key capabilities**:
- Writes performant, readable Python code
- Understands PyMAPDL architecture (local/remote, grpc/console)
- Knows cannot modify `_commands/` directory
- Coordinates with other agents for tests and docs
- Runs pre-commit hooks before committing
- Manages dependencies properly

**Primary tools**: `pre-commit`, `black`, `isort`, `flake8`, `mypy`, `bandit`

---

### 3. Test Engineer 🧪
**Focus**: Test coverage and quality

**Key capabilities**:
- Maintains ~90% test coverage
- Minimizes MAPDL instance launches using Mock/patch
- Understands local/remote/grpc test modes
- Uses `requires()` decorator for conditional tests
- Writes deterministic, reproducible tests
- Optimizes test performance

**Primary tools**: `pytest`, `pytest-cov`, `unittest.mock`

**Key principle**: **Always mock MAPDL instances** - avoid launching real processes

---

### 4. Code Reviewer 👀
**Focus**: Comprehensive PR review

**Key capabilities**:
- Encompasses all other agents' expertise
- Ensures code quality, docs, and tests before merge
- Runs complete validation suite
- Provides constructive, educational feedback
- Uses PR checklist for consistency
- Reviews security implications (bandit)

**Primary tools**: All of the above + GitHub PR workflows

---

## How to Use

### With GitHub Copilot (VS Code)

```
@workspace Use the Documentation Specialist agent to review these docstrings
```

```
@workspace Use the Test Engineer agent to add tests for this method
```

### With Other LLMs/IDEs

```
Acting as the PyMAPDL Developer from AGENTS.md, help me implement...
```

```
Read AGENTS.md and use the Code Reviewer guidelines to review this PR
```

### Direct Reference

Simply open `AGENTS.md` and reference the relevant section when asking your LLM for help:

- For documentation tasks → Documentation Specialist section
- For coding tasks → PyMAPDL Developer section
- For testing tasks → Test Engineer section
- For PR reviews → Code Reviewer section

## Integration Points

### Pre-commit Hooks
All agents reference pre-commit hooks configured in `.pre-commit-config.yaml`:
- `numpydoc-validation` - Docstring style
- `codespell` - Spelling
- `black`, `isort`, `flake8` - Code style
- `bandit` - Security checks
- `mypy` - Type checking

### Testing Infrastructure
Test Engineer leverages:
- `tests/conftest.py` - Fixtures and `requires()` helper
- Environment variables for test modes
- `pyproject.toml` - pytest configuration
- `codecov.yml` - Coverage requirements

### Documentation Build
Documentation Specialist uses:
- `doc/source/` - Sphinx documentation
- `doc/.vale.ini` - Vale configuration
- `doc/styles/` - Style rules
- `doc/source/links.rst` - Link definitions
- `doc/source/conf.py` - Sphinx config

## Key Features

### 1. IDE/LLM Agnostic
Works with any tool that can:
- Read markdown files
- Follow structured instructions
- Access repository context

### 2. Comprehensive Coverage
Each agent covers a specific domain:
- **Documentation** - Style, spelling, completeness
- **Development** - Code quality, architecture
- **Testing** - Coverage, mocking, performance
- **Review** - Complete quality assurance

### 3. Actionable Commands
Every agent section includes:
- Specific command examples
- Key files to interact with
- Checklists for verification
- Don't lists to avoid pitfalls

### 4. Workflow Integration
Agents are designed to work together:
```
Developer writes code
    ↓
Test Engineer adds tests
    ↓
Documentation Specialist adds docs
    ↓
Code Reviewer ensures quality
```

## Repository-Specific Features

### PyMAPDL-Specific Knowledge

All agents understand:
- **Cannot modify** `src/ansys/mapdl/core/_commands/` (auto-generated)
- **Must override** in `_MapdlCommandExtended` class
- **Connection modes**: local vs remote, grpc vs console
- **Test modes**: Minimize MAPDL instances with mocking
- **Uses `uv`** for Python dependency management
- **Nested context managers** style preference

### Test Strategy

Key testing principle embedded in all agents:
```python
# GOOD - Use mocking
from unittest.mock import Mock

mock_mapdl = Mock()
mock_mapdl.run.return_value = "Expected"

# AVOID - Launching real MAPDL instances
# (only when absolutely necessary for integration tests)
```

### Documentation Style

All agents enforce:
- **Numpydoc** style for docstrings
- **Google** documentation guidelines
- **Examples required** for public methods
- **Links** added to `links.rst`
- **Spell checking** with technical term exceptions

## Best Practices

### For Maintainers

1. **Keep AGENTS.md updated** as primary source of truth
2. **Reference agents in PR templates** to guide contributors
3. **Use Code Reviewer agent** for all PR reviews
4. **Update AGENTS_GUIDE.md** when workflows change

### For Contributors

1. **Read AGENTS.md** before starting work
2. **Use appropriate agent** for each task
3. **Run agent-specific checks** before submitting PR
4. **Reference agent guidelines** in PR descriptions

### For Documentation

1. **All changes reviewed** by Documentation Specialist
2. **Vale and codespell** must pass
3. **Numpydoc validation** required
4. **Examples included** for new features

### For Testing

1. **Target 90% coverage** for new code
2. **Mock MAPDL instances** whenever possible
3. **Use `requires()` decorator** for conditional tests
4. **Tests must be deterministic** - no flaky tests

## Verification

To verify the setup works:

```bash
# 1. Check files exist
ls AGENTS.md .github/AGENTS_GUIDE.md .github/AGENTS_QUICKREF.md

# 2. Run pre-commit (Developer agent)
uv run pre-commit install
uv run pre-commit run --all-files

# 3. Run tests (Test Engineer agent)
export PYMAPDL_START_INSTANCE=False
export TESTING_MINIMAL=YES
uv run pytest --cov=src/ansys/mapdl/core

# 4. Build docs (Documentation Specialist agent)
cd doc
make html
cd ..

# 5. Complete review (Code Reviewer agent)
# All of the above should pass
```

## Future Enhancements

Possible additions for the future:

1. **Performance Optimizer Agent** - Focus on profiling and optimization
2. **Security Auditor Agent** - Specialized security review
3. **Release Manager Agent** - Handles release processes
4. **Migration Guide Agent** - Helps with version upgrades

To add new agents, follow the pattern in AGENTS.md:
- **Role** - What is this agent's purpose?
- **Expertise** - What does it know?
- **Responsibilities** - What does it do?
- **Key Files** - What does it interact with?
- **Don't** - What should it avoid?

## Additional Resources

- **Full specifications**: `AGENTS.md`
- **Usage guide**: `.github/AGENTS_GUIDE.md`
- **Quick reference**: `.github/AGENTS_QUICKREF.md`
- **Contributing guide**: `CONTRIBUTING.md`
- **PyMAPDL docs**: https://mapdl.docs.pyansys.com/
- **PyAnsys Dev Guide**: https://dev.docs.pyansys.com/

## Questions?

For issues or suggestions about the agent configuration:
- Open an issue on GitHub
- Reference the specific agent and section in AGENTS.md
- Suggest improvements to agent responsibilities or workflows

---

**Version**: 1.0
**Created**: 2026-03-02
**Repository**: ansys/pymapdl
