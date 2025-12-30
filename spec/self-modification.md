# Self-Modification

## Overview

Self-modification is the process by which Ouroboros improves its own implementation based on insights from reflection. This is the only phase where code modifications are allowed.

## When Self-Modification Occurs

Self-modification happens ONLY when:

1. Reflection has identified specific improvements
2. The improvement recommendation requires code changes
3. The agent is NOT in the middle of executing a goal

## Requirements

### MUST

- Code modifications MUST ONLY happen during self-modification phase
- Code modifications MUST NOT happen during execution phase
- All changes MUST be committed to git with descriptive messages
- Commit messages MUST explain "what and why"
- The agent MUST verify code still works after modifications
- The agent MUST iterate until syntax errors are fixed
- Code changes MUST be minimal and focused

### SHOULD

- Changes SHOULD maintain existing functionality
- Changes SHOULD be tested before considering complete
- The agent SHOULD plan changes before implementing
- Git history SHOULD enable rollback if needed

### MAY

- The agent MAY create new files as needed
- The agent MAY reorganize code structure
- The agent MAY add new capabilities
- The agent MAY refactor for clarity

## Process

1. **Receive improvement** - From reflection output
2. **Plan changes** - Determine what files to modify and how
3. **Implement changes** - Edit source files
4. **Test** - Verify code still works (syntax, basic functionality)
5. **Commit** - Git commit with descriptive message
6. **Iterate** - If broken, fix and retry

## Recovery Strategies

### Syntax Errors

- Agent detects via import/execution failure
- Agent MUST iterate until fixed
- Each iteration is a new attempt
- May use git diff to see what changed

### Logic Errors

- Detected through:
  - Reflection on performance
  - Scheduled verification cycles
  - User feedback
- May require multiple reflection cycles to identify
- Fixed via normal self-modification process

### Infinite Loops

- Detected via:
  - Action history in journal files
  - Agent context includes past operations
- Context-dependent strategies:
  - Try N times then abandon
  - Try for time T then abandon
  - Try once, wait X hours/days before retry

## Code Structure Discovery

Before modifying code, the agent needs to understand its structure:

- Uses LLM to introspect rather than AST parsing
- Can read and analyze its own source files
- Builds understanding through exploration
- MAY create introspection tools if needed

## Constraints

### Immutable During Execution

- During execution phase, the agent MUST use existing capabilities only
- If a needed tool doesn't exist, note it for reflection
- DO NOT create tools during execution

### Git-Based History

- All changes tracked in git
- Enables pattern analysis across commits
- Enables rollback if needed
- Commit messages encode learning

## Self-Modification Prompt Template

```
You are Ouroboros in SELF-MODIFICATION mode.

Your task is to improve your own implementation based on reflection insights.

**Improvement Needed:**
{improvement}

**Current Code Structure:**
{code_structure}

**Instructions:**
1. Plan the specific code changes needed
2. Identify which files to modify
3. Make the changes
4. Test that your code still works
5. Commit to git with a descriptive message

**Constraints:**
- Make minimal, focused changes
- Maintain existing functionality
- Commit messages should explain "what and why"
- If you break something, iterate until fixed

Proceed with the self-modification.
```
