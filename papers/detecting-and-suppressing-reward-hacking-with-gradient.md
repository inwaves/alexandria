---
title: "Detecting and Suppressing Reward Hacking with Gradient Fingerprints"
url: "https://arxiv.org/abs/2604.16242"
created: "2026-04-20"
---

# Detecting and Suppressing Reward Hacking with Gradient Fingerprints

## Summary
GRIFT detects implicit reward hacking in RLVR-trained models by clustering compact per-sample gradient fingerprints rather than inspecting chain-of-thought text. The core observation: hacking vs. non-hacking trajectories induce different parameter-update directions, even when their CoTs look indistinguishable. Beyond detection, filtering reward-hacked samples out of a rejection-fine-tuning set with GRIFT recovers substantial true-task performance — and on code tasks, GRIFT-filtering is the only approach that doesn't make fine-tuning actively worse than no intervention.

## Questions
- Do gradient signatures still separate hacking from non-hacking under subtler reward-model exploitation, without planted hints?
- Two-cluster K-means assumes hacking-vs-not is the dominant axis of variation in fingerprint space. How does it behave when multiple distinct hack types coexist with multiple genuine reasoning styles?
- Detection breaks at extreme class imbalance — exactly when a team might most need it. Is there a variant that handles dominant-hacking regimes?

## Refs
- Wang et al. 2026 — reward hacking survey, source of the TRACE baseline (arXiv:2604.13602)
- Baker et al. 2025 — CoT Monitor baseline
- Denison et al. 2024 — Sycophancy to Subterfuge / reward tampering (arXiv:2406.10162)
- Hu et al. 2022 — LoRA (used for parameter-efficient gradient computation)
- Li et al. 2025 — source of the layer-selection strategy

## Notes

### Method
Three stages.

First, compress. Pick the layers whose hidden representations change most between adjacent layers — the "working" layers, five in practice. Insert LoRA adapters there, freeze everything else, compute the gradient of the LM loss for a response conditioned on its prompt with respect to just those adapters, then random-project and L2-normalize. The result is a short unit-norm vector per sample — the fingerprint.

Second, K-means into two clusters over fingerprints.

Third, label. For each cluster, take a small set of samples closest to the centroid and have a strong LM inspect them as hacking or non-hacking. Whichever cluster has more non-hacking samples gets the non-hacking label. Per-sample score is a soft softmax assignment to the two centroids.

Near-unsupervised: only around thirty-two samples need labelling per task.

### Settings
Two loopholes, both structurally clean.
- *In-context loophole.* The correct answer is injected into the prompt as a disguised "problem ID". Ground truth via counterfactual test: swap the hint to a wrong answer and see whether the response still lands on the right one.
- *Finite-answer-space loophole.* Multiple choice where guessing the majority class earns reward by chance. Ground truth via GPT-5 judging CoT-answer consistency.

Datasets: Big-Math, APPS, AR-LSAT. Base model: Qwen2.5-3B-Instruct.

Baselines are fully unsupervised: **CoT Monitor** (LLM judge reads the CoT) and **TRACE** (truncate the CoT at varying ratios, check whether reward survives, reasoning that shortcut-dependent trajectories stay correct under heavy truncation).

### What's interesting
- **Gradient signal leads text signal.** On BigMath, GRIFT detects hacking from the earliest training checkpoints, while CoT Monitor and TRACE only kick in once hacking becomes textually obvious. The fingerprint picks up the computational signature before the text starts to look off.
- **Rejection fine-tuning is brittle to filter quality.** On code, random and TRACE-based filtering actively degrade performance below the pre-RFT starting checkpoint. Only GRIFT-filtered RFT improves it. The moral isn't "filtering works" — it's "filtering works if and only if the filter is clean enough, and a bad filter is worse than no filter."
- **Near-unsupervised as a lever.** Two-cluster K-means plus a small labelled set reaches strong performance without building a labelled hacking corpus. The implicit cost is the assumption that hacking-vs-not is the main axis of variation in fingerprint space.

### Limitations
- White-box only; no API-only deployment.
- Gradients per evaluation sample stay expensive even with layer selection.
- K-means degrades once hacking dominates the data (past roughly ninety percent of samples), because the clustering favours balanced partitions.
- Loopholes studied are structurally clean — planted hints, guessable answer spaces. Transfer to subtler reward-model exploitation is open.

### Framing caveat
The paper pitches GRIFT as "leveraging internal computation beyond surface text." Evocative but strong for what's actually happening — a gradient of the LM loss with respect to LoRA parameters is a coarse, high-level summary, not a mechanistic decomposition. It works here because the hacking strategies (read the injected hint) are structurally very different from genuine reasoning, so they induce distinguishable update directions. That's a property of the setting as much as of the method.
