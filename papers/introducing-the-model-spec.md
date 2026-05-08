---
title: "Introducing The Model Spec"
url: "https://openai.com/index/introducing-the-model-spec"
created: "2026-05-06"
---

# Introducing The Model Spec

## Summary
- OpenAI formally publishes its Model Spec — a normative document specifying how its models should reason, prioritize, and behave across safety, ethics, and helpfulness dimensions.
- The spec codifies a principal hierarchy (OpenAI > operators > users), honesty norms, harm avoidance heuristics, corrigibility requirements, and guidance for agentic contexts.
- This May 2026 post marks the official public launch, following a preview shared in April 2026, and represents OpenAI's most comprehensive public statement on alignment philosophy to date.

## Questions

## Refs
- Bai et al. 2022 — Constitutional AI: Harmlessness from AI Feedback (arXiv:2212.08073)
- Ouyang et al. 2022 — InstructGPT: Training LMs to follow instructions with human feedback (arXiv:2203.02155)
- Leike et al. 2018 — Scalable agent alignment via reward modeling (arXiv:1811.07871)
- Amodei et al. 2016 — Concrete Problems in AI Safety (arXiv:1606.06565)
- OpenAI 2026 — Sharing the latest Model Spec (web preview, April 2026)
- Anthropic 2023/2024 — Claude Model Spec / Character overview (web)

## Notes
- Watchlist match: HIGH — Directly from OpenAI on alignment and behavioral specification. Core reading for AI safety researchers tracking how frontier labs operationalize alignment philosophy into training targets.

### Triage
9 — OpenAI's formal public release of their Model Spec is a landmark alignment document directly relevant to AI safety, behavioral guidelines, and the principal hierarchy problem. Essential reading for anyone tracking how frontier labs operationalize alignment.

### Motivation
Frontier AI models are deployed across enormously diverse contexts, yet must behave consistently with safety and ethical principles. OpenAI needed a single authoritative document to specify model values, resolve conflicts between principals, and guide both training and deployment behavior.

### Hypothesis
A well-specified normative document — covering priority ordering, honesty, harm avoidance, and corrigibility — can serve as a foundation for training models that are simultaneously safe, ethical, adherent to OpenAI's principles, and genuinely helpful.

### Methodology
This is a normative/policy document rather than an empirical paper. It articulates behavioral principles, priority orderings, and decision heuristics derived from OpenAI's internal alignment research, deployment experience, and the broader alignment literature (RLHF, Constitutional AI, scalable oversight).

### Results
The spec formalizes: (1) a four-level priority stack — broadly safe > broadly ethical > adherent to OpenAI principles > genuinely helpful; (2) a principal hierarchy with differentiated trust levels; (3) explicit honesty norms (non-deception, non-manipulation, calibration); (4) harm avoidance heuristics with hardcoded vs. softcoded behaviors; and (5) agentic safety guidelines emphasizing minimal footprint and human oversight.

### Interpretation
The Model Spec is OpenAI's most explicit public alignment artifact — it operationalizes abstract safety goals into trainable behavioral norms. The framing of corrigibility as a temporary but necessary stance, and the explicit acknowledgment that unhelpfulness is not automatically safe, reflect mature alignment thinking consistent with Anthropic's Claude spec and the broader field.

### Context
This follows Anthropic's public Claude character/model spec and directly parallels it in structure. The April 2026 "Sharing the latest Model Spec" preview from OpenAI's Alexandria entry confirms this is an iterative public release. It sits within a broader industry trend of frontier labs publishing normative alignment documents as both internal training guides and external accountability signals.

### Limitations
As a normative document, it lacks empirical validation of whether trained models actually internalize these norms. The gap between spec and model behavior — especially under adversarial conditions or distributional shift — remains an open research problem. The document also cannot fully resolve genuine value conflicts; it provides heuristics rather than decision procedures.

### Why it matters
Directly central to AI safety and alignment research. Provides a concrete reference point for studying how frontier labs operationalize alignment, and is a key artifact for researchers working on corrigibility, honesty, harm avoidance, and agentic safety.
