# Ouroboros

An autonomous self-improving agent.

## Overview

Ouroboros continuously improves its own implementation while working on assigned goals. It operates without human intervention but can accept feedback.

## Installation

```bash
uv sync
```

## Usage

```bash
# Start the agent (runs forever)
uv run ouroboros run

# Check status
uv run ouroboros status

# Trigger a reflection cycle
uv run ouroboros reflect

# Provide feedback
uv run ouroboros feedback "You should focus more on X"

# View logs
uv run ouroboros tail-logs
```

## Adding Goals

Edit `agent/goals/active.md` to add new goals in natural language.

## Project Structure

```
ouroboros/
├── src/ouroboros/    # Agent source code
├── agent/            # Agent data directory
│   ├── goals/        # Active and completed goals
│   ├── journal/      # Daily notes and reflections
│   └── logs/         # Structured logs
└── plan.md           # Design documentation
```

## Philosophy

**Do → Learn → Improve → Retry**

1. Work on goals using current capabilities
2. Journal everything
3. Reflect on performance
4. Modify own code based on insights
5. Repeat
