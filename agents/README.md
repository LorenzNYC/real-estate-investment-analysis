# Claude Code System Prompts (Reverse-Engineered)

Reverse-engineered system prompts from [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts).

These are the extracted system prompts from Anthropic's Claude Code CLI tool (npm package v2.1.77), organized by category.

## Structure

```
agents/
├── system-prompts/        # 32 agent-specific prompts (Explore, Plan, Security, etc.)
├── core-system-prompts/   # 79 core system prompt segments
├── tool-descriptions/     # 56 tool description prompts (Bash, Edit, Glob, etc.)
├── system-reminders/      # 47 contextual system reminder prompts
├── skills/                # 11 skill definitions (commit, review-pr, simplify, etc.)
├── data/                  # 26 reference data files (API docs, SDK patterns, etc.)
├── CHANGELOG.md           # Version history across 127+ Claude Code releases
├── CLAUDE.md              # Meta-guidance for CLAUDE.md file creation
└── LICENSE                # License from source repository
```

## Source

- **Repository**: https://github.com/Piebald-AI/claude-code-system-prompts
- **Claude Code Version**: 2.1.77 (March 16, 2026)
- **Maintainer**: Piebald AI (not affiliated with Anthropic)

## Notes

- These are reference materials only -- editing them does not affect Claude Code behavior
- Template variables (e.g. `${VARIABLE_NAME}`) are interpolated at runtime
- Prompts are conditionally included based on environment and configuration
- See [tweakcc](https://github.com/nicobailon/tweakcc) for local prompt customization
