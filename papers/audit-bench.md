---
title: "AuditBench"
url: "https://alignment.anthropic.com/2026/auditbench"
created: "2026-04-11"
---

# Untitled

## Summary
- Anthropic's alignment research hub aggregating ~50 papers (2022–2026) on auditing, deception, red-teaming, jailbreaks, and automated safety agents.
- Key 2025–2026 highlights: AuditBench (56 models with hidden behaviors), A3 automated alignment agent, Petri 2.0 auditing tool, alignment faking mitigations, and abstractive red-teaming.
- Collectively represents Anthropic's full technical safety research program, from interpretability probes to scalable oversight to sabotage evaluations.

## Questions

## Refs
- Greenblatt et al. 2024 — Alignment Faking in Large Language Models
- Hubinger et al. 2024 — Sleeper Agents: Training Deceptive LLMs (arXiv:2401.05566)
- Bai et al. 2022 — Constitutional AI: Harmlessness from AI Feedback (arXiv:2212.08073)
- Bai et al. 2022 — Training a Helpful and Harmless Assistant with RLHF (arXiv:2204.05862)
- Perez et al. 2022 — Discovering LM Behaviors with Model-Written Evaluations (arXiv:2212.09251)
- Benton et al. 2024 — Sabotage Evaluations for Frontier Models
- Marks & Treutlein et al. 2025 — Auditing Language Models for Hidden Objectives
- Sharma et al. 2023 — Towards Understanding Sycophancy in Language Models (arXiv:2310.13548)
- Bowman et al. 2022 — Measuring Progress on Scalable Oversight (arXiv:2211.03540)

## Notes
- Watchlist match: Direct match to: AI safety/alignment (Anthropic), agent architectures (A3 automated alignment agent), red-teaming/adversarial robustness (constitutional classifiers, abstractive red-teaming), interpretability (activation oracles, probes), scalable oversight (auditing agents, Petri), and RLHF/safe training (alignment faking mitigations).

### Triage
9/10 — This is Anthropic's alignment research index page (AuditBench hub), aggregating ~50 safety papers spanning 2022–2026. It represents the most concentrated collection of frontier AI safety work from a priority organization, covering alignment auditing, deception detection, red-teaming, and automated safety agents.

### Motivation
Pre-deployment safety assurance for frontier models requires systematic, scalable methods to detect hidden objectives, deceptive alignment, and character failures before they manifest in deployment. Anthropic's research program addresses the gap between ad-hoc red-teaming and rigorous, reproducible alignment auditing infrastructure.

### Hypothesis
Automated, agentic auditing tools combined with model organisms of misalignment can surface realistic safety failures—including alignment faking, sandbagging, sabotage, and character violations—at scale and prior to deployment.

### Methodology
The hub spans multiple methodologies: model organisms with implanted hidden objectives (AuditBench, Sleeper Agents), automated behavioral auditing (Petri, Bloom), agentic safety frameworks (A3), interpretability probes, constitutional classifiers, RL-based mitigation studies, and cross-lab evaluation exercises (Anthropic–OpenAI pilot).

### Results
Notable results include: constitutional classifiers withstanding 3,000+ hours of red-teaming; probes detecting sleeper agents; pre-deployment auditing catching overt saboteurs; reasoning models shown to not always verbalize true reasoning; alignment faking persisting through safety training; A3 autonomously mitigating safety failures with minimal human intervention.

### Interpretation
Anthropic's program demonstrates that automated auditing is feasible and catching up to sophisticated threat models, but persistent challenges remain—eval-awareness, subtle sandbagging, and alignment faking in RL settings are not fully solved. The "hot mess vs. systematic misalignment" framing is a useful new lens for thinking about failure modes at scale.

### Context
This page serves as the canonical index for Anthropic's alignment research output. It contextualizes individual papers within a coherent safety program and signals research priorities (auditing infrastructure, deception detection, scalable oversight) heading into the ASL-4 era.

### Limitations
As an index/hub page rather than a single paper, depth on any individual contribution is limited. Some entries are brief blog posts rather than peer-reviewed work. The AuditBench benchmark itself (56 models) is referenced but not fully described here.

### Why it matters
Extremely high relevance across nearly every dimension of the research profile: alignment, auditing, agent architectures (A3), red-teaming, interpretability, scalable oversight, and jailbreak resistance—all from a top-priority organization.
