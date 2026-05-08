---
title: "A3: An Automated Alignment Agent for Safety Finetuning"
url: "https://alignment.anthropic.com/2026/automated-alignment-agent/"
created: "2026-04-04"
---

# A3: An Automated Alignment Agent for Safety Finetuning

## Summary

A3 is an agentic framework that automates the cycle of identifying, expanding, and remediating safety failures in LLMs via targeted finetuning. Given a known safety issue (e.g. sycophancy), the system autonomously generates diverse adversarial training data, iteratively finetunes the model using LoRA, and evaluates whether the failure is fixed — all with minimal human intervention. The core claim is that safety improvements need not require proportional human effort.

Fellowship work: Jifan Zhang (Anthropic Fellows Program), Henry Sleight (Constellation / Astra fellowship), supervised by Joe Benton (Anthropic, Scalable Oversight).

## The Pipeline

A3 operates as a 4-step pipeline with three core components:

### 1. Data Generation Agent
- Takes a seed example of a safety failure and a behavior description as input.
- Uses [Bloom](bloom-an-open-source-tool-for-automated-behavioral.md) to decompose the failure into hypotheses about *why* the model fails, then generates diverse adversarial prompts that test each hypothesis.
- Also generates **benign counterparts** for every harmful prompt — structurally similar queries that *should not* be refused — to control false positive rates.
- Uses Claude (Sonnet) with extended thinking for hypothesis generation and prompt creation.

### 2. Finetuning Agent
- Splits generated data into train / validation / OOD evaluation sets.
- Generates expected model responses (what the model *should* say) for both harmful and benign prompts using Claude.
- **Iterative LoRA finetuning**: Claude acts as the finetuning agent — it reads the experiment log, selects hyperparameters (LoRA rank/alpha, learning rate, epochs, data mixing weights), launches a HuggingFace Trainer run, evaluates, and iterates.
- **Data mixing**: blends generated safety data with [DOLCI](https://huggingface.co/datasets/allenai/Dolci-Instruct-SFT) (a general instruction-following dataset) at agent-controlled ratios (typically 15-30% DOLCI) to prevent catastrophic forgetting.
- Tracks general capabilities via MMLU-Pro and GPQA benchmarks each epoch.

### 3. Experiment Log
- Structured text log shared between agents, tracking hypotheses tested, prompts generated, training runs attempted, and evaluation results.
- Gives the system memory across iterations so the finetuning agent can learn from past failures (e.g. "mixing ratio X caused forgetting, try lower").
- Stored as plain text files — readable by both agents and humans.

### Three Simultaneous Objectives
The system optimizes for:
1. Minimize unsafe behavior on the target failure mode.
2. Prevent catastrophic forgetting of general capabilities.
3. Reduce false positive rates (over-refusal on benign queries).

## Results

Tested on three safety issues: sycophancy, political bias, and nesting jailbreaks. Target models: Llama 3.1 8B and Qwen (open-weight, small-scale).

A3 outperformed:
- Non-adaptive baselines (fixed training data without the iterative loop).
- Other existing models on targeted safety evaluations.

The paper also compares against two non-finetuning defenses: in-context learning (ICL) and DSPy prompt optimization (GEPA). LoRA finetuning via A3 outperformed both.

## Relationship to Other Work

A3 is explicitly downstream of two other Anthropic safety tools:
- **Petri** — automated auditing environment that *discovers* safety issues.
- **[Bloom](bloom-an-open-source-tool-for-automated-behavioral.md)** — automated behavioral evaluation tool that *generates diverse test cases* for known issues.

Together these form the beginning of an automated safety pipeline: Petri finds problems → Bloom generates evaluations → A3 remediates via finetuning.

## Open-Source Implementation

[GitHub repo](https://github.com/safety-research/A3). ~5,500 lines of Python. Research-quality code with clean architecture but no tests, no CI, print-based logging, and fragile subprocess management (vLLM, bloom-evals). The configuration system is well-designed (JSON configs with dataclass validation, everything parameterized). The iterative finetuning loop uses Claude as the hyperparameter selection agent — no formal search algorithm (no Bayesian optimization or population-based training), just "Claude reads past results and suggests what to try next."

## Limitations and Scope

- **Scale**: demonstrated on LoRA finetuning of 8B-parameter models. The iterative loop is cheap at this scale but does not straightforwardly transfer to frontier-scale post-training.
- **Known failures only**: A3 remediates failures you can already specify. It has no mechanism for discovering new failure modes — that's Petri/Bloom's job.
- **Safety engineering, not alignment**: this fixes behavioral issues (sycophancy, jailbreaks), not inner alignment failures. A model that is deceptively aligned would not be fixed by targeted SFT on observable behaviors.
- **Hyperparameter "intelligence"**: the finetuning agent's reasoning about what to try next is unstructured LLM inference, not a principled optimization method. May work for 3-5 iterations on small models but unclear how it scales.

## Questions

- Does the iterative data generation + finetuning loop actually find qualitatively different training data than a single-shot approach, or does it mostly just find *more* of the same?
- How sensitive is the mixing strategy to the choice of general-capability dataset (DOLCI)? Would results differ with a different retention dataset?
- Could targeted SFT on observable failures inadvertently affect model character in ways not captured by MMLU-Pro/GPQA? The reward hacking literature suggests narrow training can generalize unpredictably.
- The Petri → Bloom → A3 pipeline is compelling, but who audits the pipeline? If A3 generates training data autonomously, adversarial or subtly wrong training data is a possible failure mode.
- Can this approach handle failure modes that require multi-turn or context-dependent evaluation, or is it limited to single-turn behavioral rubrics?

## Refs

- [Bloom: An Open-Source Tool for Automated Behavioral Evaluations](bloom-an-open-source-tool-for-automated-behavioral.md)
- Petri & updates
- Anthropic alignment landscape — Layer 5 (automated alignment research)
- AI Control research direction
- Alignment Auditing research direction
- Joe Benton profile

---

*Last updated: 2026-04-10.*
