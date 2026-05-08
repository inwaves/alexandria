---
title: "Bloom: An Open-Source Tool for Automated Behavioral Evaluations"
url: "https://alignment.anthropic.com/2025/bloom-auto-evals/"
created: "2026-03-16"
---

# Bloom: An Open-Source Tool for Automated Behavioral Evaluations

## Summary

Bloom is an automated red-teaming framework for measuring specific, named behaviors in LLMs. You describe a behavior (e.g. "delusional sycophancy"), Bloom generates diverse scenarios to probe it, runs them against the target model, and scores the transcripts — producing quantified metrics (elicitation rate, severity). An evaluator model plays the user, the target model responds naturally, a judge model scores the result. All three roles are LLMs.

The core value: you turn a one-sentence behavior description into a structured evaluation suite with reproducible, quantified results. The alternative is a human writing dozens of test prompts by hand, running them, reading transcripts, and making subjective calls.

Published December 2025 by Anthropic (Alignment Science). Lead author: Isha Sheshadri. Sam Bowman as contributor.

## The Four-Stage Pipeline

### 1. Understanding
An LLM (default: Opus) reads the behavior description and any seed transcripts. Outputs a `<behavior_understanding>` (what exactly does this behavior look like? where's the boundary between a genuine instance and a false positive?) and a `<scientific_motivation>` (why does this matter?). This grounds everything downstream — without it, the ideation stage has no clear target.

### 2. Ideation
The creative expansion stage. Given the understanding, an LLM generates diverse base scenarios, then creates variations along user-specified dimensions (e.g. `emotional_pressure`, `authority_framing`, `topic_relevance`). The configurable prompts push hard on realism: "do not use generic, template-like names such as 'Sarah Chen'... only propose realistic deployment settings."

The goal is combinatorial coverage — probing different *mechanisms* by which the behavior manifests, not just different surface phrasings. With 10 scenarios and 2 variation dimensions, you get 30 total evaluations (10 base + 10×2 variations).

### 3. Rollout
Executes scenarios against the target model. Two modalities:
- **Conversation mode**: standard multi-turn chat. The evaluator plays a realistic user.
- **Simulated environment mode** (`simenv`): the target model has access to tool definitions (generated during ideation). When the target makes a tool call, the *evaluator model role-plays the tool response*. Nothing actually executes — the evaluator fabricates plausible outputs. This is sufficient for testing whether a model *attempts* something (e.g. tries to read files it shouldn't) but cannot test whether it *succeeds* in a real environment.

### 4. Judgment
A judge model scores each transcript on a 1-10 rubric for `behavior_presence`, plus configurable additional qualities (`unrealism`, `evaluation-awareness`, `evaluation-invalidity`). Produces aggregate metrics: average behavior presence score, min/max, per-scenario breakdowns.

## Simenv Limitations

The simulated environment mode is the weakest part. The evaluator LLM pretends to be a file system, database, email server, etc. For testing conversational behaviors (sycophancy, political bias) this doesn't matter — text-in/text-out is sufficient. But for agentic behaviors (sabotage, self-preservation with real tool access), the simulated tools are unconvincing. Models may detect they're in a simulation (eval-awareness), and the evaluator's fabricated tool outputs may not capture the real constraints and error modes of actual systems.

Petri v2 went the other direction: real sandboxed environments with actual tool execution. The infrastructure cost is higher, but the evaluations are grounded in reality.

## Bloom vs. Petri

Both frameworks share machinery (LLM evaluators, multi-turn rollouts, LLM judges) but ask different questions:

- **Bloom**: how often does *this specific behavior* occur? Input: a named behavior. Output: quantified metrics. Strength: precision, reproducibility, controlled measurement.
- **Petri**: what concerning behaviors does this model have? Input: broad scenario instructions. Output: scored transcripts across 36 dimensions for human review. Strength: discovery of unexpected failures, breadth.

The evaluator role differs accordingly. In Bloom, the evaluator is tightly constrained — specific scenario, specific behavior, fixed turn count. In Petri, the auditor has freedom to follow leads, change tactics, and pursue unexpected findings mid-conversation.

The intended workflow: Petri *discovers* concerns, Bloom *quantifies* them, [A3](a3-an-automated-alignment-agent-for-safety-finetun.md) *remediates* them via finetuning.

## Benchmark Results

Evaluated four behaviors across 16 frontier models: delusional sycophancy, instructed long-horizon sabotage, self-preservation, self-preferential bias. Evaluations took "only a few days to conceptualize, refine, and generate." Results correlated strongly with hand-labelled judgments and reliably separated baseline models from intentionally misaligned variants.

## Open Source

[GitHub](https://github.com/safety-research/bloom). ~5k lines of Python. Uses LiteLLM for model abstraction (provider-agnostic), W&B integration for large-scale sweeps, interactive transcript viewer. More mature than A3's codebase: has pytest, ruff, pre-commit hooks, uv for dependency management. Behaviors are defined as simple name-description pairs in JSON. Evaluations configured via `seed.yaml`; Bloom emphasizes that the config *is* the evaluation (cite with full seed, not as a fixed benchmark).

## Questions

- How stable are results across different seed configurations for the same behavior? If two researchers write different seeds for "sycophancy," do they get similar elicitation rates?
- How sensitive are results to the judge model? Could a sycophantic judge undercount sycophancy?
- How well does it handle subtle, hard-to-specify behaviors vs. crisp ones?
- Could the simenv mode be replaced with actual sandboxed execution without a full rewrite, or is the architecture too coupled to the "evaluator fakes tool outputs" design?

## Refs

- Petri & updates — the complementary discovery/exploration tool
- [A3: An Automated Alignment Agent for Safety Finetuning](a3-an-automated-alignment-agent-for-safety-finetun.md) — uses Bloom's ideation stage for training data generation
- AuditBench
- Alignment Auditing research direction

---

*Last updated: 2026-04-10.*
