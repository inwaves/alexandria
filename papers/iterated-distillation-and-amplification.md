---
title: "Iterated Distillation and Amplification"
url: "https://ai-alignment.com/iterated-distillation-and-amplification-157debfd1616"
created: "2026-04-05"
---

# Iterated Distillation and Amplification

## Summary

The foundational blog post introducing Christiano's IDA (Iterated Distillation and Amplification) framework — his core alignment research agenda through ~2020.

The idea: start with a weak but aligned agent (a human, or a simple model trained to imitate a human). Amplify it by allowing it to consult copies of itself (producing a slow but more capable system). Then distill this amplified system back into a fast model. Repeat: the distilled model becomes the base for the next round of amplification.

Key properties:
- **Competitive**: the resulting system can in principle match the capabilities of any AI system, because amplification can reach arbitrary capability levels.
- **Aligned by construction**: at each step, the system is trained to approximate a process that is itself aligned (a human consulting copies of the previous aligned system).
- **Analogous to AlphaGoZero**: the amplification step is like MCTS (slow but good), and the distillation step is like the neural network policy (fast approximation of the slow process).

The framework connects to several of Christiano's other ideas:
- **Approval-directed agents**: the base case for IDA.
- **HCH** (Humans Consulting HCH): the theoretical limit of iterated amplification — a tree of humans consulting each other.
- **Debate**: an alternative amplification mechanism.

## Significance

IDA was the dominant alignment research agenda at OpenAI during Christiano's tenure (~2017-2021) and heavily influenced subsequent work on scalable oversight, debate, and RLHF. It is the intellectual ancestor of the "Bumpers" approach at Anthropic.

## Refs

- Approval-directed agents — the base case
- [Supervising strong learners by amplifying weak experts](supervising-strong-learners-by-amplifying-weak-exp.md) — the formal paper version
- [AI Safety via Debate](ai-safety-via-debate.md) — debate as an alternative amplification mechanism
- [Outer alignment and imitative amplification](outer-alignment-and-imitative-amplification.md) — Hubinger's analysis of IDA's outer alignment properties
- Paul's research agenda FAQ — detailed FAQ about IDA

---

*Last updated: 2026-04-05.*
