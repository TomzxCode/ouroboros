# CLI Interface

## Overview

The CLI provides the primary interface for interacting with Ouroboros. It uses Typer for command definition and supports both autonomous operation and user interaction.

## Available Commands

### run

Start the agent's main loop.

```bash
ouroboros run
```

- Runs forever until interrupted (SIGINT/SIGTERM)
- Reads goals from `agent/goals/active.md`
- Enters self-improvement mode if no goals
- Cannot be run in background (user may use & or nohup)

### status

Show current agent status.

```bash
ouroboros status
```

Displays:
- Running state
- Agent directory
- Last activity timestamp
- Idle time in seconds
- Total tokens used
- Active goals (first 200 characters)

### reflect

Trigger an immediate reflection cycle.

```bash
ouroboros reflect
```

- Runs reflection once
- May trigger self-modification
- Exits after completion

### tail-logs

View or follow log files.

```bash
ouroboros tail-logs [OPTIONS]
```

Options:
- `--follow, -f`: Follow log output (like `tail -f`)
- `--lines, -n`: Number of lines to show (default: 50)

### feedback

Add feedback for the agent.

```bash
ouroboros feedback "Your feedback message here"
```

- Creates `agent/journal/YYYY/MM/DD/user-feedback.md`
- Appends timestamped entry
- Consumed during next reflection cycle

## Requirements

### MUST

- All commands MUST work from any directory within the project
- The agent directory MUST be discovered automatically
- Commands MUST provide helpful output
- Commands MUST handle errors gracefully
- `run` MUST support graceful shutdown on SIGINT/SIGTERM

### SHOULD

- Commands SHOULD have clear help text
- Output SHOULD be human-readable
- Errors SHOULD provide actionable guidance
- Status display SHOULD be concise but informative

### MAY

- Additional commands MAY be added later
- Commands MAY support additional options
- A chat interface MAY be added
- HTTP API MAY be added for external tools

## Agent Directory Discovery

Commands find the agent directory by:

1. Searching upward from current directory for `agent/` subdirectory
2. Falling back to creating `agent/` in current directory

This allows running commands from any subdirectory.

## Signal Handling

The agent handles:

- `SIGINT` (Ctrl+C) - Graceful shutdown
- `SIGTERM` - Graceful shutdown

Shutdown process:
1. Set `running = False`
2. Exit run loop gracefully
3. Final log entry
4. Exit

## Future Enhancements

- `ouroboros pause` - Pause execution without exiting
- `ouroboros goals add/remove/list` - Goal management commands
- `ouroboros journal` - Direct journal access
- `ouroboros chat` - Interactive chat interface
- `--agent-dir` flag to override auto-discovery
