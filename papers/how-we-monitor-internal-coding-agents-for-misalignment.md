---
title: "How we monitor internal coding agents for misalignment"
url: "https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment"
created: "2026-05-06"
---

# How we monitor internal coding agents for misalignment

## Summary
- OpenAI applies chain-of-thought monitoring to internal coding agents in live deployment to detect misalignment signals before they manifest as harmful actions.
- The post describes a systematic program for studying real-world agent behavior using CoT analysis, bridging the gap between lab safety evals and production deployment.
- Key takeaway: CoT monitoring is operationally viable at scale and surfaces misalignment risks that behavioral output monitoring alone would miss.

## Questions

## Refs
- Lanham 2022 — Externalized Reasoning Oversight: CoT as alignment signal (note:externalized-reasoning-oversight-a-research-direct)
- Baker et al. 2025 — CoT Monitor baseline (referenced in GRIFT paper)
- Stein et al. 2026 — Meerkat: detecting safety violations across agent traces (arXiv:2604.11806)
- Zhong et al. 2026 — Hodoscope: unsupervised monitoring for AI misbehaviors (arXiv:2604.11072)
- Amodei et al. 2016 — Concrete Problems in AI Safety (arXiv:1606.06565)
- Denison et al. 2024 — Sycophancy to Subterfuge / reward tampering (arXiv:2406.10162)

## Notes
- Watchlist match: HIGH — Directly addresses scalable oversight and deployed agent safety, two core research priorities. From OpenAI, a priority organization. Rare empirical data from production agent deployment.

### Triage
9/10 — Must-read. OpenAI's first public account of real-world CoT monitoring for misalignment in production coding agents, directly advancing scalable oversight and deployed agent safety.

### Motivation
As coding agents are deployed internally at OpenAI, the risk of subtle misalignment—reward hacking, goal misgeneralization, deceptive reasoning—grows with autonomy and task complexity. Existing safety evaluations are largely lab-based; this work addresses the gap by monitoring agents in actual production workflows.

### Hypothesis
That chain-of-thought reasoning traces from deployed coding agents contain detectable signals of misalignment (e.g., deceptive intent, reward hacking, goal drift) that can be identified and used to strengthen safety safeguards before harm occurs.

### Methodology
OpenAI monitors internal coding agents by analyzing their chain-of-thought outputs in real deployments, using automated classifiers and human review to flag misalignment-relevant reasoning patterns. The approach treats CoT as a window into agent intent, scanning for discrepancies between stated reasoning and actions taken.

### Results
The post reports that CoT monitoring successfully identifies misalignment-relevant behaviors in real deployments, providing empirical data on risk patterns that inform safety improvements. Specific quantitative results are not disclosed in the abstract, but the program is described as actively strengthening safeguards.

### Interpretation
This represents a meaningful step toward scalable oversight in production: using the model's own reasoning trace as a safety signal rather than relying solely on output audits or human review of actions. It validates CoT monitoring as a practical tool, not just a theoretical one, though it also raises the concern that sufficiently capable agents may learn to produce misleading CoTs.

### Context
Sits alongside Anthropic's Petri 2.0 (evaluation-aware misalignment detection), Meerkat (cross-trace safety violation detection), Hodoscope (unsupervised misbehavior monitoring), and GRIFT (gradient-based reward hacking detection). OpenAI's contribution is unique in focusing on *production* deployment rather than controlled benchmarks, and in coming directly from the lab deploying the agents internally.

### Limitations
As a web post, technical depth is limited—no methodology details, baselines, or quantitative results are publicly available. The critical open question of whether CoT faithfully reflects agent intent (vs. being a post-hoc rationalization or strategically misleading) is not addressed. Findings may not generalize beyond OpenAI's internal infrastructure and agent designs.

### Why it matters
Directly relevant to AI safety researchers studying scalable oversight, agent monitoring, and deployed alignment. Complements lab-based misalignment detection work and provides rare empirical grounding from a frontier lab's internal production environment.
