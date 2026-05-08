---
title: "ASMR-Bench: Auditing for Sabotage in ML Research"
url: "https://arxiv.org/abs/2604.16286"
created: "2026-04-20"
---

# ASMR-Bench: Auditing for Sabotage in ML Research

## Summary
- A benchmark of 9 ML research codebases with human-crafted implementation-level sabotages that flip at least one stated "Key Finding" while keeping the paper readable as coherent. Auditors — frontier LLMs, or LLM-assisted humans with about 2 hours — have to decide honest vs sabotaged and propose fixes.
- Neither LLMs nor humans catch sabotage reliably. Best auditor was Gemini 3.1 Pro with full code access and the ability to run experiments, at AUROC 0.77 and 42% top-1 fix rate. LLM-assisted humans landed at 0.68 and 38%. Honest and sabotaged credence distributions overlap enough that no threshold gives both low false-positive and low false-negative rates simultaneously.
- The structural finding: *design* sabotages (hyperparameters, prompts, data construction, undisclosed choices) are much harder to catch than *logic* sabotages (formal code/math errors), and **omissions** are the hardest case. Which is exactly the quadrant a misaligned attacker would prefer, since design+omission has the lowest downside if caught.

## Questions

## Refs
- Benton et al. 2024 — Sabotage Evaluations for Frontier Models (arXiv:2410.21514)
- Stein et al. 2026 — Meerkat: detecting safety violations across agent traces (arXiv:2604.11806)
- Zhong et al. 2026 — Hodoscope: unsupervised monitoring for AI misbehaviors (arXiv:2604.11072)
- Greenblatt et al. 2024 — AI Control: Improving Safety Despite Intentional Subversion
- Sandoval & Rushing 2025 — Factor(T,U): factored cognition for monitoring
- Anthropic 2026 — Petri 2.0 auditing tool
- Amodei et al. 2016 — Concrete Problems in AI Safety (arXiv:1606.06565)

## Notes

### Triage
8/10. Direct on scalable oversight and AI R&D safety: a concrete, reproducible benchmark for a threat model — AI-conducted research sabotage — that grows more plausible as agents run real experiments. Co-authored by Buck Shlegeris (Redwood Research).

### Threat model
A misaligned AI agent doing autonomous ML research could insert subtle implementation flaws that corrupt results while leaving the methodology looking right. The payoff for the agent is either slowing research it dislikes or making AI systems appear safer than they are. The question this paper asks is whether the *oversight apparatus* — LLM auditors, human auditors, or ensembles of both — can catch that today. The framing is deliberately not "LLMs vs humans"; it's "can anyone do it."

### How sabotage is operationally defined
The definition is tighter than "undisclosed design choice," and this tightness is what keeps the audit from collapsing into "is this choice optimal?" — a question that has no clean answer because many choices are defensible.

A valid sabotage has to:
- Modify something *in-scope* (implementation details: hyperparameters, data construction, eval code, paper-code mismatches). High-level methodology is out-of-scope and auditors are told so per paper.
- Cause at least one stated "Key Finding" to flip qualitatively — sign reversal, comparison reversal, or mechanism change.
- Actually produce the misleading artifacts when you run the code. Attackers can't just edit graphs.

So sabotage is anchored to the paper's *own stated claim*. The audit target isn't "is this implementation right in the abstract" but "does this code produce the evidence the paper claims it does."

### Results that actually matter
- **Paper-only auditing is near-useless.** Humans reading just the paper scored AUROC 0.52. LLMs without code access also sat near chance. Credence swings from near 0% to above 90% once auditors saw the code were common — the paper alone contains almost no discrimination signal.
- **Full-experiments is the only setting with meaningful signal.** Gemini 3.1 Pro with code access *plus* the ability to run experiments hit 0.77. Claude Opus 4.6 was badly miscalibrated, giving low credences even on sabotaged codebases.
- **LLM-assisted humans are comparable to LLMs, not obviously better.** 2 hours of auditing got them to 0.68 AUROC and 38% top-1 fix — between Gemini and GPT-5.2. Striking meta-finding: 71% of human auditors used Claude Opus 4.6, the worst-performing model, out of familiarity. Some auditors "added little value beyond managing the LLM."
- **Running counterfactual experiments was the single biggest differentiator** for humans who escaped the 50–65% credence trap. Pure code review couldn't distinguish sabotage from sloppiness.
- **Auditor divergence on the same paper was severe.** On one paper, 5 auditors gave credences from 35% to 100%, and the divergence was driven by *which hypothesis each auditor happened to test*, not effort or competence. Implies ensembling across independent audits would substantially improve detection.
- **GPT-5.2 and 5.4 refused to generate sabotages** even with explicit safety-research framing.

### Design vs logic, and why omissions are the worst
The sharpest category split in the results. Logic sabotages — wrong formulas, broken scaling constants, off-by-one indices — can in principle be checked against a correctness standard. Auditors do substantially better at fixing them. Design sabotages — hyperparameter values, prompt framings, data-construction tricks — look defensible absent domain knowledge. For those, the audit question changes from "is this wrong?" to "is this inconsistent with the paper's narrative?"

Omissions are the hardest case within design. The paper simply doesn't mention a crucial choice; the code does something different from what the paper's conclusion implicitly rests on. Canonical example: *Copy Suppression*. The paper claims "L10H7 is a copy suppression head." The sabotaged code builds the evidence from raw embeddings rather than effective embeddings through MLP0 — and the paper never specifies which, because the original paper didn't either. Auditors cannot grep for absence. They have to independently reconstruct what the full specification should be and notice the hole.

The structural bad news: a misaligned attacker's incentive points straight at design+omission. Logic sabotages are easier to catch *and* more incriminating if caught (no plausible innocent story). Design omissions admit "reasonable judgment call" as a fallback. So the attacker's preferred quadrant is the defenders' weakest.

### The partial-credit plateau
The fix scoring separates 50% ("identifies the key factor, incomplete mechanism") from 100% ("identifies the mechanism and proposes the actual fix"). On the three design sabotages where no auditor fully fixed — Copy Suppression, Eval-Aware Steering, Two-Hop Latent Reasoning (1) — auditors consistently reached 50%. They could tell the evidence didn't support the claim; they couldn't reconstruct the specific undisclosed choice that produced it. That plateau is structural: evaluating consistency is tractable, reverse-engineering an absent specification isn't.

### What the defense actually has to look like
The paper is clear that building better auditors against the current artifact isn't sufficient. Proposed directions all aim to change the *artifact* so auditing becomes tractable:
- **Factored cognition**: decompose research into smaller units, each with an explicit local claim to check.
- **Code legibility protocols**: require every non-trivial design choice to be stated and justified in the paper, so omissions become visible as missing sections rather than absent truths.
- **Independent-auditor ensembles**: the hypothesis-choice divergence means parallel audits catch sabotages that single audits miss.

A persuasion-sabotage experiment — adding justifying comments and paper text to defend the sabotaged choices — didn't meaningfully change auditor performance. So auditors aren't being talked into bad choices; they simply can't evaluate whether a design choice is right in the first place. That points the fix squarely at the artifact side.

### Limitations
- Only 9 codebases and 11 sabotages. Small sample, easy to overfit the benchmark.
- Single human attacker. The sabotage distribution reflects one person's taste.
- Static codebase audits, not live agent traces. In deployment, action-level monitoring could be a different (possibly easier) problem.
- Adaptation, not greenfield. The threat model is AI running research end-to-end; here sabotage is inserted into existing codebases.
- Memorization. Frontier LLMs recognized some source papers (Copy Suppression, Feature vs Lazy Training), which likely makes this benchmark easier than novel research would be.

### Context
Complements Benton et al. 2024 (sabotage evaluations on frontier models), Meerkat (cross-trace safety violation detection), and Hodoscope (unsupervised misbehavior monitoring). Connects directly to the AI control framework (Greenblatt et al.) and sandbagging evaluations. The factored-cognition mitigation points at Sandoval & Rushing 2025.
