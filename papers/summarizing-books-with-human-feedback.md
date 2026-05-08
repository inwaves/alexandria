---
title: "Summarizing books with human feedback"
url: "https://openai.com/index/summarizing-books"
created: "2026-04-23"
---

# Summarizing books with human feedback

## Summary
- OpenAI demonstrates that recursive task decomposition + RLHF can scale human oversight to long-horizon tasks (full book summarization) that humans cannot directly evaluate in a single pass.
- A hierarchical summarization approach — summarizing chunks, then summaries of summaries — lets human raters provide meaningful feedback at each level, bootstrapping quality on tasks beyond direct human evaluation capacity.
- This is a foundational empirical demonstration of scalable oversight via task decomposition, directly relevant to the core AI safety problem of supervising AI on tasks harder than humans can evaluate.

## Questions

## Refs
- Christiano et al. 2017 — Deep Reinforcement Learning from Human Preferences (arXiv:1706.03741)
- Stiennon et al. 2020 — Learning to Summarize with Human Feedback (arXiv:2009.01325)
- Bowman et al. 2022 — Measuring Progress on Scalable Oversight for LLMs (arXiv:2211.03540)
- Leike et al. 2018 — Scalable agent alignment via reward modeling (arXiv:1811.07871)
- Amodei et al. 2016 — Concrete Problems in AI Safety (arXiv:1606.06565)

## Notes
- Watchlist match: HIGH — directly addresses scalable oversight, a top-priority AI safety topic; from OpenAI, a priority organization. Foundational empirical work on RLHF for tasks beyond direct human evaluation.

### Triage
8

### Motivation
Humans cannot directly evaluate AI outputs on long-horizon tasks (e.g., summarizing a full novel) because the task exceeds human working memory and attention. This creates a fundamental scalable oversight gap: how do you provide reliable training signal when the task is too hard to evaluate directly?

### Hypothesis
Recursive decomposition of a hard-to-evaluate task into human-evaluable subtasks, combined with RLHF at each level, can produce high-quality outputs on the full task — even when no human can directly verify the final output quality end-to-end.

### Methodology
A hierarchical summarization pipeline is trained using RLHF: books are split into chunks, chunk summaries are generated and rated by humans, then summaries-of-summaries are generated and rated, recursively up to a final book-level summary. Reward models are trained at each level and used to fine-tune the policy via RL.

### Results
The approach produces book summaries that human evaluators judge as high quality, despite no single human having read the full book during training. The recursive RLHF pipeline outperforms baselines that lack the hierarchical structure or human feedback signal.

### Interpretation
This is a proof-of-concept that scalable oversight via task decomposition is practically viable for LLMs. It suggests that the "hard to evaluate" problem can be partially addressed by breaking tasks into evaluable sub-problems — a key building block for supervising superhuman AI systems.

### Context
This work sits at the intersection of RLHF methodology and scalable oversight theory (Christiano et al.'s debate/amplification proposals). It predates and directly informs later work like InstructGPT, Constitutional AI, and ongoing scalable oversight research at Anthropic and OpenAI.

### Limitations
The approach assumes task decomposability — not all hard tasks can be cleanly hierarchically decomposed. Human raters at each level may still be fooled by plausible-sounding but subtly wrong summaries, and reward hacking at lower levels can compound upward through the hierarchy.

### Why it matters
Directly addresses the scalable oversight problem — one of the most important open problems in AI safety. The recursive RLHF framework is a concrete, empirically-tested approach to maintaining human control over AI on tasks that exceed direct human evaluation capacity.
