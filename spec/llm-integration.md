# LLM Integration

## Overview

Ouroboros uses Anthropic's Claude API (Sonnet model) for all reasoning and decision-making. The LLM client wrapper provides cost tracking and a consistent interface.

## Model Selection

- Primary: Claude Sonnet (claude-sonnet-4-20250514)
- Alternative: GLM 4.7 (Sonnet-like)
- Configuration: Model specified in `LLMClient` initialization

## Requirements

### MUST

- All LLM calls MUST go through `LLMClient` wrapper
- Token usage MUST be tracked (input and output separately)
- The client MUST support system prompts
- The client MUST support temperature control
- API key MUST be configurable via environment variable
- Total token usage MUST be queryable

### SHOULD

- Prompt caching SHOULD be used for system instructions
- Expensive operations SHOULD consider token costs
- The client SHOULD handle API errors gracefully

### MAY

- Different models MAY be used for different operations
- Local models MAY be supported (Ollama, etc.)
- Response streaming MAY be added for long outputs

## LLMClient Interface

```python
class LLMClient:
    def __init__(self, api_key: str | None = None, model: str = "...")
    def complete(
        self,
        prompt: str,
        system: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str

    @property
    def total_tokens(self) -> int
    @property
    def total_input_tokens(self) -> int
    @property
    def total_output_tokens(self) -> int
```

## API Configuration

The API key is configured via environment variable:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

The client reads this automatically if not provided.

## Cost Tracking

The client tracks:

- `total_input_tokens` - All tokens sent to the API
- `total_output_tokens` - All tokens received from the API
- `total_tokens` - Sum of input and output

This is displayed in `ouroboros status` for cost awareness.

## Prompt Structure

All prompts follow this pattern:

1. **System prompt** - Role, context, operating principles
2. **User prompt** - Specific task or question
3. **Context injection** - Dynamic state (goals, history, etc.)

## System Prompts

Separate system prompts for each phase:

- `SYSTEM` - Default/general operations
- `PLAN` - Planning phase
- `EXECUTE` - Execution phase
- `REFLECT` - Reflection phase
- `SELF_MODIFY` - Self-modification phase

Each includes:
- Role definition
- Current context
- Specific instructions for that phase

## Cost Considerations

The API has a fixed cost per month (5-hour budget equivalent).

Strategies to manage costs:

- Prompt caching for system instructions (static content)
- Efficient context construction
- Avoiding redundant LLM calls
- Using appropriate max_tokens values

## Error Handling

The client must handle:

- API errors (rate limits, outages)
- Invalid responses
- Timeout scenarios

Error handling strategy:

- Log the error
- Back off and retry
- Continue operation if possible

## Future Enhancements

- Response streaming for long outputs
- Multi-model support (use cheaper models for simple tasks)
- Token budgeting/alerting
- Request batching when possible
