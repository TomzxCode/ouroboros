# Memory System

## Overview

Ouroboros uses a multi-tiered memory system comprising working memory (in-process), short-term memory (daily journal files), and long-term memory (git history). All memory is human-readable.

## Memory Tiers

### Working Memory

In-process state held during execution:

- Current goal(s) being worked on
- Recent operations for immediate context
- LLM connection and credentials

### Short-term Memory (Journal)

Daily markdown files under `agent/journal/YYYY/MM/DD/`:

- `notes.md` - Operation logs, observations, execution results
- `reflections.md` - Scheduled reflection output
- `user-feedback.md` - User-provided feedback

### Long-term Memory (Git)

Complete history of all changes with commit messages encoding "what I tried and why".

## Requirements

### MUST

- All journal entries MUST be in markdown format
- Journal entries MUST include timestamps
- Journal directories MUST follow YYYY/MM/DD structure
- The agent MUST create required directories on startup
- All code changes MUST be committed to git
- Commit messages MUST describe what was changed and why
- Memory MUST be human-readable (plain text/markdown)

### SHOULD

- Journal files SHOULD be organized by category (notes, reflections, etc.)
- Each journal entry SHOULD be timestamped
- Important operations SHOULD be logged to both journal and structured logs
- Git commits SHOULD be atomic (one logical change per commit)

### MAY

- A summary/index file MAY be maintained for quick access
- Vector search MAY be added later for semantic retrieval
- Journal entries MAY include tags or categories

## Directory Structure

```
agent/
├── journal/
│   └── YYYY/MM/DD/
│       ├── notes.md
│       ├── reflections.md
│       └── user-feedback.md
├── logs/
│   └── YYYY/MM/DD/
│       └── {pid}.log
└── goals/
    ├── active.md
    └── completed.md
```

## Journal Operations

### Append

Add a new entry to a journal file:

- MUST include timestamp
- MUST preserve existing content
- MUST create file if it doesn't exist

### Read

Read entire journal file:

- MUST return empty string if file doesn't exist
- SHOULD preserve original formatting

### Write

Overwrite a journal file:

- MUST create parent directories if needed
- MUST preserve existing file if not intentionally overwriting

## Logging

Structured logs are written to `agent/logs/YYYY/MM/DD/{pid}.log`:

- MUST be JSON-formatted
- MUST include timestamp and log level
- One log file per process instance
- Used for debugging and auditing

## Agent Directory Discovery

The agent directory is located by:

1. Searching upward from current directory for `agent/` subdirectory
2. Falling back to creating `agent/` in current directory

This allows the agent to work from any subdirectory within the project.
