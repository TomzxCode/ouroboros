# Goal Management

## Overview

Goals are the primary input mechanism for Ouroboros. They are specified in natural language and managed through markdown files.

## Goal Format

Goals are specified in natural language, similar to GitHub issues or PR descriptions. They are stored in `agent/goals/active.md`.

## Requirements

### MUST

- Goals MUST be stored in `agent/goals/active.md`
- Goals MUST be in natural language format
- The agent MUST be able to parse and select goals from the active file
- Completed goals MUST be moved to `agent/goals/completed.md`
- The goal files MUST use markdown format
- The agent MUST handle an empty active.md file (enter idle mode)

### SHOULD

- Goals SHOULD be clearly specific and achievable
- Goals SHOULD include success criteria when ambiguous
- The goal format SHOULD support multiple simultaneous goals
- Completed goals SHOULD be timestamped when moved to completed.md
- The agent SHOULD interact with the user if goals are ambiguous

### MAY

- Goals MAY include priority indicators
- Goals MAY include deadline information
- Goals MAY include dependencies on other goals
- A goal queue MAY be implemented (currently single goal selection)

## Goal Selection

When multiple goals exist:

- The agent MUST select one goal to work on
- Selection strategy MAY be: first in file, highest priority, or LLM-determined
- Unselected goals MUST remain in active.md

## Goal Completion

A goal is considered complete when:

- The agent determines it has satisfied the completion criteria
- The completion criteria are determined by the agent based on goal content
- If unclear, the agent interacts with the user to define criteria

## User Interaction

When goal content is ambiguous:

- The agent MUST determine what information is needed
- The agent MAY create a journal entry requesting clarification
- The agent MAY wait for user input in user-feedback.md
- The agent MUST not proceed until clarity is achieved

## File Format

### active.md

```markdown
# Active Goals

## Goal Title

Description of what needs to be done.

Additional details, constraints, or context.
```

### completed.md

```markdown
# Completed Goals

## Completed: YYYY-MM-DDTHH:MM:SS

**Goal:** (original goal text)

**Result:** (outcome of the work)
```
