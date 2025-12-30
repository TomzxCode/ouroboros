# Tool Creation

## Overview

Tools are CLI subcommands that the agent can create for itself. They extend the agent's capabilities and are managed entirely by the LLM.

## Tool Definition

A tool is a CLI subcommand under the `tools` command group:

```bash
ouroboros tools <tool-name> [arguments]
```

## Requirements

### MUST

- Tools MUST be CLI subcommands
- Tools MUST be under the `tools` command group
- Tools MUST be managed by the LLM (no manual registration)
- The agent MUST be able to discover and use its available tools
- Tools MUST be tested before being considered complete

### SHOULD

- Tools SHOULD have clear names indicating their purpose
- Tools SHOULD accept arguments for flexibility
- Tools SHOULD be documented (help text)
- Tools SHOULD be committed to git after creation

### MAY

- Tools MAY be organized in subcategories
- Tools MAY have infinite depth of organization
- Tools MAY create other tools
- Tools MAY be removed if no longer useful

## Tool Creation Process

When the agent determines it needs a new tool:

1. **Identify need** - During planning or reflection
2. **Design tool** - Determine name, arguments, behavior
3. **Write code** - Create Python implementation
4. **Register in CLI** - Add to typer/cyclopts structure
5. **Test** - Verify tool works as intended
6. **Commit** - Save to git with descriptive message
7. **Document** - Update help text if needed

## Tool Storage

Tools are stored in `src/ouroboros/tools/`:

```
src/ouroboros/tools/
├── __init__.py
├── code_search.py
├── file_analyzer.py
└── ... (agent-created tools)
```

## Tool Discovery

The agent must be able to:

- List all available tools
- Understand what each tool does
- Determine appropriate arguments
- Execute tools with proper parameters

Discovery method:

- Dynamic import of tools module
- Introspection of CLI structure
- LLM analysis of tool code/documentation

## Tool Example

```python
# src/ouroboros/tools/code_search.py

import typer
from pathlib import Path

def search(pattern: str, directory: str = ".") -> None:
    """Search for a pattern in code files."""
    # Implementation here
    pass
```

Registered in CLI:

```python
# src/ouroboros/cli.py
@app.command()
def tools(
    tool_name: str = typer.Argument(...),
    tool_args: list[str] = typer.Argument(default=[]),
) -> None:
    """Execute a tool."""
    # Dynamic tool dispatch
    pass
```

## Constraints

- Tools are created during self-modification phase, NOT during execution
- If a needed tool doesn't exist during execution, note it for reflection
- Tools must not break existing functionality
- Tools should be focused and single-purpose

## Future Enhancements

- Tool dependency management
- Tool versioning
- Tool sandboxing
- Tool marketplace/sharing between agents
