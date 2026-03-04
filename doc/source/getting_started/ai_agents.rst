.. _ai_agents:

============================
AI Agents for Development
============================

.. note::
    This section is a work in progress and may be updated frequently as we
    refine our AI agent strategy and implementation.

PyMAPDL uses structured AI agents to automate and improve development, testing,
documentation, and code review. These agents are available in any LLM-enabled IDE
(GitHub Copilot, Cursor, JetBrains AI, etc.) and are configured in the `.github/agents/`
directory.

Available Agents
----------------

- **Developer**: Implements features, fixes bugs, optimizes performance, and designs APIs.
- **Documentation Specialist**: Reviews and improves documentation, validates docstrings, checks spelling and style.
- **Tester**: Maintains test coverage, implements mocking strategies, and ensures test infrastructure quality.
- **Reviewer**: Performs comprehensive PR reviews and enforces quality gates before merging.

Workflow
--------

The typical workflow is:

1. **Developer** implements code and features
2. **Tester** adds or updates tests, ensuring ≥90% coverage
3. **Documentation Specialist** reviews and improves documentation and docstrings
4. **Reviewer** checks code quality, documentation, and tests before merge

Agent Usage
-----------

You can invoke agents by referencing their names in prompts or using slash commands
in supported IDEs. See :ref:`how_to_use_agents` for detailed instructions and examples
for each IDE.

Agent Guidelines
----------------

- Each agent follows a detailed specification in `.github/agents/` and summarized in
  :file:`AGENTS.md`.
- Agents enforce project standards for code style, documentation, testing, and review.
- See :file:`AGENTS.md` and :file:`.github/HOW_TO_USE_AGENTS.md` for full details and usage tips.

For more information, see:

- :ref:`how_to_use_agents`
- :ref:`write_documentation`
- :ref:`developing_pymapdl`
- :file:`AGENTS.md`
- :file:`.github/HOW_TO_USE_AGENTS.md`
