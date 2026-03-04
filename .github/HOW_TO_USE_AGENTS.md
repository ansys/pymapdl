# How to Use PyMAPDL AI Agents

This guide shows how to invoke the specialized AI agents for PyMAPDL development in various IDEs and tools.

## Available Agents

- **[Developer](agents/developer.agent.md)** - Implements features and fixes bugs
- **[Documentation Specialist](agents/documentation.agent.md)** - Reviews and improves documentation
- **[Tester](agents/tester.agent.md)** - Writes tests and ensures coverage
- **[Reviewer](agents/reviewer.agent.md)** - Comprehensive PR reviews

See [AGENTS.md](../AGENTS.md) for complete specifications.

## How to Invoke Agents by IDE

### GitHub Copilot CLI

Use the `/agent` slash command to browse and select an agent, or reference by name in a prompt:

```
/agent
```

```
Use the developer agent to implement a new method for exporting mesh data
```

```
Use the tester agent to add tests for the new export_mesh method with mocking
```

```
Use the documentation agent to review docstrings in src/ansys/mapdl/core/mesh.py
```

```
Use the reviewer agent to review my latest changes for quality and completeness
```

### GitHub Copilot (VS Code)

Use `@workspace` to give Copilot access to the repository context including agent definitions:

```
@workspace Use the Developer agent to implement a new method for exporting mesh data
```

```
@workspace Use the Tester agent to add tests for the new export_mesh method with mocking
```

```
@workspace Use the Documentation Specialist agent to review docstrings in src/ansys/mapdl/core/mesh.py
```

```
@workspace Acting as the Code Reviewer agent, review this PR for quality and completeness
```

### Claude Code

`CLAUDE.md` at the repo root loads the agent context automatically. Reference agents by name:

```
Act as the developer agent and implement a new method for exporting mesh data
```

```
Act as the tester agent and add tests for the new export_mesh method with mocking
```

```
Act as the documentation agent and review docstrings in src/ansys/mapdl/core/mesh.py
```

```
Act as the reviewer agent and review my latest changes
```

### Cursor IDE

Cursor has built-in agent support. Use `@` to reference files:

```
@AGENTS.md Act as the Developer agent and help me fix bug #123
```

```
@.github/agents/tester.agent.md Write comprehensive tests for the new feature
```

```
Using the Documentation Specialist agent guidelines from @AGENTS.md, improve these docstrings
```

### JetBrains IDEs (PyCharm, IntelliJ)

With JetBrains AI Assistant:

```
Reference AGENTS.md and act as the Test Engineer agent to help me write tests for this class
```

```
Follow the Code Reviewer checklist in AGENTS.md to review my changes
```

### Claude Desktop / ChatGPT / Other LLMs

When working with standalone LLMs, provide context explicitly:

```
I'm working on the PyMAPDL project. Read the AGENTS.md file in my repository and act as the Developer agent to help me implement [feature].
```

```
Acting as the Documentation Specialist agent from PyMAPDL's AGENTS.md, review these docstrings: [paste content]
```

### Command Line with LLM Tools

If using CLI tools like `aider`, `gpt-engineer`, or similar:

```bash
# Add AGENTS.md to context
aider --read AGENTS.md --message "Act as the Developer agent to implement feature X"
```

## Quick Command Reference

### Developer Agent
```bash
uv run pre-commit run --all-files
uv run mypy src/ --config-file=pyproject.toml
```

### Documentation Specialist Agent
```bash
cd doc && make html
vale doc/source/
uv run codespell doc/ src/
```

### Tester Agent
```bash
# Without MAPDL instance
SET PYMAPDL_START_INSTANCE=False
SET TESTING_MINIMAL=YES
uv run pytest --cov=src/ansys/mapdl/core --cov-report=html
```

### Code Reviewer Agent
```bash
uv run pre-commit run --all-files
uv run pytest --cov=src/ansys/mapdl/core --cov-report=term
cd doc && make html
uv run bandit -c pyproject.toml -r src/
```

## Typical Workflow

1. **Developer** implements code → Run pre-commit hooks
2. **Tester** adds tests with mocking → Verify ≥90% coverage
3. **Documentation Specialist** adds docs → Build and validate
4. **Reviewer** approves → All checks pass → Merge

## Tips for Effective Agent Use

1. **Be specific** - Reference the agent name and the specific task
2. **Provide context** - Share relevant file paths, error messages, or requirements
3. **Reference guidelines** - Point to specific sections in AGENTS.md when needed
4. **Iterate** - Work with the agent to refine the solution
5. **Verify** - Run the agent's suggested commands to validate changes

## Examples

### Example 1: Adding a New Feature

**Developer Agent:**
```
@workspace Act as the Developer agent. I need to add a method to export
MAPDL results to CSV format. The method should be in the Mapdl class.
```

**Tester Agent:**
```
@workspace Act as the Tester agent. Add comprehensive tests for the
export_to_csv method, using mocking to avoid launching MAPDL.
```

**Documentation Specialist:**
```
@workspace Act as the Documentation Specialist. Review and improve the
docstring for export_to_csv, ensuring numpydoc compliance with examples.
```

### Example 2: Fixing a Bug

**Developer Agent:**
```
@workspace Act as the Developer agent. Fix the connection timeout issue
in remote mode described in issue #456.
```

**Tester Agent:**
```
@workspace Act as the Tester agent. Add a regression test for the timeout
fix that works in both local and remote modes.
```

### Example 3: PR Review

**Code Reviewer Agent:**
```
@workspace Act as the Code Reviewer agent. Review my PR that adds async
support for mesh operations. Check code quality, tests, and documentation.
```

## Troubleshooting

**Agent not following guidelines?**
- Explicitly reference: "Follow the [Agent Name] guidelines in AGENTS.md"
- Point to specific sections: "Use the mocking strategy from the Tester agent section"

**Agent lacks context?**
- Use `@workspace` (VS Code) or `@AGENTS.md` (Cursor) to include files
- Paste relevant code sections in your prompt
- Reference specific file paths

**Commands not working?**
- Ensure you're in the repository root directory
- Check that `uv` is installed and configured
- Verify Python environment is activated

## Additional Resources

- **[AGENTS.md](../AGENTS.md)** - Complete agent specifications
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - General contribution guidelines
- **[PyMAPDL Documentation](https://mapdl.docs.pyansys.com/)** - Full project documentation
