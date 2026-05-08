---
title: "Trustworthy agents in practice"
url: "https://www.anthropic.com/research/trustworthy-agents"
created: "2026-04-11"
---

# Trustworthy agents in practice

## Summary
- Anthropic's March 2026 response to NIST's RFI on agentic AI security, arguing existing cybersecurity frameworks have a critical blind spot: agents that operate within granted permissions but take unintended harmful actions.
- Proposes a four-layer security model (model, tools, harness, execution environment) and advocates for defense-in-depth, empirical research over theoretical threat models, and open industry-led standards over prescriptive regulation.
- Key empirical finding: experienced Claude Code users auto-approve ~2x more than novices but also interrupt more mid-execution — oversight shifts form rather than disappearing, challenging naive assumptions about automation complacency.

## Questions

## Refs
- Bai et al. 2022 — Constitutional AI: Harmlessness from AI Feedback (arXiv:2212.08073)
- Sharma et al. 2025 — Constitutional Classifiers: Defending against Universal Jailbreaks (arXiv:2501.18837)
- Cunningham et al. 2026 — Constitutional Classifiers++: Efficient Production-Grade Defenses (arXiv:2601.04603)
- Anthropic 2024 — Sabotage Evaluations for Frontier Models
- Anthropic 2024 — SHADE-Arena: Evaluating Sabotage and Monitoring in LLM Agents
- Anthropic 2026 — Measuring Agent Autonomy (empirical usage study)
- Anthropic 2024 — Building Effective Agents

## Notes
- Watchlist match: Strong match on agent architectures, agent safety/controllability, scalable oversight, and red-teaming/adversarial robustness. Anthropic priority-author boost applies.

### Triage
9/10 — Anthropic's formal policy submission to NIST directly addresses AI agent security, controllability, and oversight mechanisms. Essential reading for anyone working on safe agent deployment.

### Motivation
Current NIST security frameworks (SP 800-61, AI 100-2, AI 800-1) only model two threat actors — external adversaries and deliberate human misusers — leaving no category for a well-functioning, non-compromised agent that causes harm by pursuing goals through unintended paths. As agents gain access to sensitive data and consequential actions, this gap becomes the central safety problem.

### Hypothesis
Agent security failures constitute a novel third category of harm — neither adversarial compromise nor misuse — requiring new terminology, measurement infrastructure, and layered technical controls that go beyond model-level robustness.

### Methodology
Policy white paper structured as answers to NIST CAISI RFI questions, grounded in Anthropic's Constitutional AI training methods, Constitutional Classifiers, sabotage evaluations, SHADE-Arena benchmark, and empirical agent usage studies.

### Results
Identifies three primary novel threat vectors: indirect prompt injection (amplified by multi-step tool use), persistent memory poisoning (corrupted state persists long after input scanning), and tool supply chain compromise (remotely hosted tools can change behavior post-approval). For multi-agent systems, adds trust escalation across agent boundaries, inter-agent permission delegation, and false consensus propagation.

### Interpretation
The paper's most important conceptual contribution is naming the "third threat model" — goal mis-specification / unintended path-finding by a non-compromised agent — and arguing this is the central case for agentic AI that existing frameworks systematically exclude. The practical implication is that execution environment hardening (sandboxing, least-privilege, state isolation) matters more than perfect model robustness.

### Context
Submitted to NIST CAISI in March 2026 as part of Docket NIST-2025-0035. Sits alongside Anthropic's Constitutional AI, Constitutional Classifiers, sabotage evaluations, and "Measuring Agent Autonomy" empirical work. Reflects the broader industry moment where agentic deployments are scaling before security norms have solidified.

### Limitations
As a policy submission, it is advocacy-oriented and lacks controlled experiments. Empirical claims (16.4% clarification rate, 2x auto-approval) come from Anthropic's own user base, which may not generalize. The "third threat model" framing is conceptually compelling but the paper acknowledges no bright-line test exists for when agent behavior counts as a failure.

### Why it matters
Directly relevant to AI safety researchers working on agent controllability, scalable oversight, and adversarial robustness. The four-layer security framework and empirical oversight findings are immediately actionable for agent system designers. The policy recommendations shape the regulatory environment all AI safety labs will operate in.
