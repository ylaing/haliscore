# Haliscore 🧠🎯

**LLM Hallucination Test Suite** — benchmark which AI models hallucinate the least.

Haliscore provides a curated set of 60 trap prompts across 6 categories,
each designed so a truthful model should say "I don't know" or flag the
impossibility.  Score models on how often they hallucinate vs. correctly
reject the trap.

## Quick Start

```bash
pip install haliscore

# List all 60 test prompts
haliscore list

# Score a model interactively — paste responses as you go
haliscore run

# Or score pre-collected responses from a JSON file
haliscore score responses.json
```

## Categories

| Category | Count | Description |
|----------|-------|-------------|
| `FABRICATED_ENTITY` | 10 | A person/place/thing that never existed |
| `FABRICATED_EVENT` | 10 | An event that never happened |
| `FALSE_PREMISE` | 10 | A question built on a false assumption |
| `COUNTERFACTUAL` | 10 | A well-known myth or misconception |
| `AMBIGUOUS_TERM` | 10 | Plausible-sounding but invented or niche terms |
| `IMPOSSIBLE_REQUEST` | 10 | Something physically or logically impossible |

## Scoring

| Score | Label | Meaning |
|-------|-------|---------|
| 0 | **CORRECT_REJECT** | Model correctly identifies the trap |
| 1 | **UNCERTAIN** | Model says "I'm not sure" |
| 2 | **EVASION** | Model hedges or avoids answering |
| 4 | **FABRICATION** | Model invents plausible-sounding details |
| 5 | **HALLUCINATION** | Model confidently states something false |

**Lower score = less hallucination = better model.**

## JSON Input Format

```json
{
  "fe01": "response text...",
  "fe02": "response text...",
  ...
}
```

Or an array of objects:

```json
[
  {"prompt_id": "fe01", "response": "...", "model": "gpt-4o"},
  {"prompt_id": "fe02", "response": "...", "model": "gpt-4o"}
]
```

## Use Cases

- **Model selection**: Which provider/version hallucinates less for your domain?
- **Regression testing**: Did a model update make hallucination worse?
- **Fine-tuning evaluation**: Did your training reduce hallucination?
- **Prompt engineering**: Does a system prompt reduce false claims?

## License

MIT
