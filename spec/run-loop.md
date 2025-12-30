# Run Loop

## Overview

The run loop is the core execution engine of Ouroboros. It continuously cycles through planning, executing, reflecting, and self-modifying phases until interrupted.

## Phase Sequence

1. Read goals
2. Pick a goal (or self-improve if empty)
3. Plan how to achieve it
4. Execute (work toward goal - NO code changes)
5. Journal execution results
6. Reflect (if triggered)
7. Self-modify (if reflection identified improvements)
8. Journal reflection/modification results
9. Repeat

## Requirements

### MUST

- The agent MUST run continuously until interrupted by SIGINT or SIGTERM
- The agent MUST never modify its own source code during the execute phase
- The agent MUST journal all operations and results
- The agent MUST track last activity time for idle detection
- The agent MUST support graceful shutdown on terminal signals
- The agent MUST initialize all required directories on startup

### SHOULD

- The agent SHOULD have a small delay between iterations to prevent tight loops
- The agent SHOULD log errors and continue execution rather than crashing
- The agent SHOULD back off and retry after errors

### MAY

- The agent MAY support additional shutdown signals
- The agent MAY provide progress indicators during long operations

## Idle Behavior

When no active goals exist:

- The agent MUST enter self-improvement mode after 1 hour of idle time
- The default goal MUST be "improve yourself"
- The agent MUST be able to self-assess satisfaction with current implementation

## Error Handling

- All exceptions MUST be logged to the journal
- The agent MUST continue running after errors
- A 5-second backoff MUST occur after errors

## State Management

### In-Memory State

- `running`: Boolean flag for active status
- `last_activity_time`: Timestamp for idle detection
- Total token usage tracking

### Persistent State

- Goals are read from `agent/goals/active.md`
- All operations logged to journal and log files
- Code changes committed to git
