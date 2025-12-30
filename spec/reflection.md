# Reflection System

## Overview

Reflection is the process by which Ouroboros reviews its performance, learns from experience, and identifies opportunities for self-improvement. It is a distinct phase from execution.

## Triggers

Reflection is triggered by:

1. **Goal completion** - After completing each goal
2. **Idle time** - Every 1 hour of no active goals
3. **User command** - Manual trigger via `ouroboros reflect`

## Requirements

### MUST

- Reflection MUST consume recent operations from the journal
- Reflection MUST consume user feedback if present
- Reflection MUST output to `reflections.md` in the daily journal
- Reflection output MUST be human-readable
- Reflection MAY trigger self-modification if improvements are identified
- The agent MUST NOT modify its code during reflection (only during self-modify phase)

### SHOULD

- Reflection SHOULD identify patterns in performance
- Reflection SHOULD review what went well and what didn't
- Reflection SHOULD consider user feedback when provided
- Reflection SHOULD be specific about improvements needed
- Reflection SHOULD learn from both successes and failures

### MAY

- Reflection MAY maintain a "lessons learned" database
- Reflection MAY track success rates of different approaches
- Reflection MAY adjust goal priorities based on patterns

## Reflection Input

The reflection process receives:

1. **Recent operations** - Content from `notes.md`
2. **Goals worked on** - Current or recent goals from `active.md`
3. **User feedback** - Content from `user-feedback.md` if present

## Reflection Output

The reflection MUST include:

1. **Summary** - Overview of recent work
2. **Lessons learned** - What worked, what didn't
3. **Improvement recommendations** - Specific changes to make (if any)

If improvements are recommended, the output MUST be specific enough to guide the self-modification phase.

## Self-Modification Trigger

Reflection triggers self-modification when:

- The output contains keywords like "improve", "change", "modify", "should", "recommend"
- The agent determines code changes would enhance future performance
- User feedback explicitly requests changes

## User Feedback

Users provide feedback via:

- CLI command: `ouroboros feedback "message"`
- Direct file creation: `agent/journal/YYYY/MM/DD/user-feedback.md`

Feedback format:

```markdown
## YYYY-MM-DDTHH:MM:SS

User's feedback message here.
```

The agent MUST consume feedback during the next reflection cycle.

## Reflection Prompt Template

```
You are Ouroboros in REFLECTION mode.

Your task is to reflect on recent operations and identify potential improvements.

**Recent Operations:**
{operations}

**Goals Worked On:**
{goals}

**User Feedback:**
{user_feedback}

**Instructions:**
1. Review what went well and what didn't
2. Identify patterns in your performance
3. Consider user feedback if provided
4. Determine if any code changes would improve future performance
5. Be specific about what should change and why

Output your reflection with:
- Summary of recent work
- Lessons learned
- Specific improvement recommendations (if any)
```
