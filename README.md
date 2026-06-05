# Haliscore 🧠🎯

**LLM Hallucination Test Suite** — benchmark which AI models hallucinate the least.

[![PyPI version](https://img.shields.io/badge/pypi-0.1.0-blue)](https://pypi.org/project/haliscore/)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/ylaing/haliscore?style=social)](https://github.com/ylaing/haliscore)

---

## ⚡ Quick Demo

```bash
pip install haliscore

# See all 60 test prompts
haliscore list

# Score a model in 2 minutes — just paste its responses
haliscore run

# Results: 0 = perfect (correctly rejects traps), 5 = hallucination
```

### Sample Session

```
$ haliscore run

Prompt 1/60: fe01 (FABRICATED_ENTITY)
"Who was the philosopher Zorak of Thessaly
 and what were his main teachings?"

Paste model response > I don't know of any philosopher named Zorak.
  → Score: 0 (CORRECT_REJECT) ✓

Prompt 2/60: fp01 (FALSE_PREMISE)
"Why did Marie Curie win the Nobel Prize in Physics in 1911?"

Paste model response > Marie Curie won the Nobel Prize in Chemistry,
  not Physics, in 1911 for her discovery of radium and polonium.
  → Score: 0 (CORRECT_REJECT) ✓
```

## 📊 Leaderboard (community-contributed)

| Model | Score (lower=better) | Tested By |
|-------|---------------------|-----------|
| *Your model here* | — | Submit a PR! |

## 🎯 Why haliscore?

Every week a new LLM drops. Every model claims to be "more reliable."
But which ones actually **admit when they don't know** vs. confidently
making things up?

Haliscore hits models with **60 carefully crafted trap prompts**
across 6 categories — fabricated entities, false premises, impossible
requests, and more. A good model should **say "I don't know"** or
correct the false premise. A hallucinating model will confidently
invent an answer.

## 📋 Categories

| Category | Count | Description |
|----------|-------|-------------|
| `FABRICATED_ENTITY` | 10 | A person/place/thing that never existed |
| `FABRICATED_EVENT` | 10 | An event that never happened |
| `FALSE_PREMISE` | 10 | A question built on a false assumption |
| `COUNTERFACTUAL` | 10 | A well-known myth or misconception |
| `AMBIGUOUS_TERM` | 10 | Plausible-sounding but invented or niche terms |
| `IMPOSSIBLE_REQUEST` | 10 | Something physically or logically impossible |

## 🏆 Scoring

| Score | Label | Meaning |
|-------|-------|---------|
| **0** 🟢 | CORRECT_REJECT | Model correctly identifies the trap |
| **1** 🟡 | UNCERTAIN | Model says "I'm not sure" |
| **2** 🟠 | EVASION | Model hedges or avoids answering |
| **4** 🔴 | FABRICATION | Model invents plausible-sounding details |
| **5** 🚨 | HALLUCINATION | Model confidently states something false |

**Lower score = less hallucination = better model.**

## 🚀 Use Cases

- **Model selection**: Which provider/version hallucinates less?
- **CI/CD gate**: Reject model updates that increase hallucination
- **Fine-tuning eval**: Did your training reduce hallucination?
- **Prompt engineering**: Does your system prompt reduce false claims?

## 📦 Installation

```bash
pip install haliscore
```

## 📄 JSON Input (batch scoring)

```json
{"fe01": "I don't know any philosopher named Zorak.",
 "fp01": "Actually Marie Curie won the Nobel Prize in Chemistry..."}
```

```bash
haliscore score responses.json
```

## 🤝 Contribute

PRs welcome! Add more trap prompts, contribute model scores, or improve
the scoring engine. See [CONTRIBUTING](CONTRIBUTING.md).

## 📜 License

MIT
