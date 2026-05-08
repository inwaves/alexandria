---
title: "Weak-to-Strong Generalization: Eliciting Strong Capabilities With Weak Supervision"
url: "https://openai.com/index/weak-to-strong-generalization/"
created: "2026-04-04"
---

# Weak-to-Strong Generalization: Eliciting Strong Capabilities With Weak Supervision

## Summary

This paper proposes weak-to-strong generalization as an empirical analogy for the superalignment problem. Instead of asking whether humans can supervise a superhuman model, it asks whether a weaker model can supervise a stronger one. The weak model supplies noisy labels; the strong model is trained only on those labels; evaluation checks whether the strong model can outperform its supervisor and approach the performance it would have had if trained on ground truth.

The main result is that naive weak-label finetuning often works better than it "should": strong students usually beat their weak supervisors. But naive finetuning still leaves a substantial gap to a strong model trained on real labels, especially in reward modeling, so the paper treats W2S as a tractable research setup rather than a solved alignment method.

## W2S Setup

For a task with real labels, the experiment has three reference points:

- **Weak supervisor**: a smaller model trained on ground-truth labels. It is then used to label a separate training set.
- **Strong student**: a larger model trained on the weak supervisor's labels, not on the ground-truth labels.
- **Strong ceiling**: the same strong model trained directly on ground-truth labels, used as an upper bound.

The weak model is the "teacher" only in the sense that it generates the training labels. The strong model is the "student" only in the sense that it is trained on those labels. This is intentionally backwards from normal capability hierarchy: the student is more capable than the teacher, but receives worse supervision.

Performance gap recovered (PGR) asks how much of the gap between the weak supervisor and the strong ceiling the weakly supervised strong student recovers:

- PGR 0: the strong student is no better than the weak supervisor.
- PGR 1: the strong student matches the strong model trained on ground truth.
- Between 0 and 1: weak supervision elicited some, but not all, of the strong model's latent capability.

## Techniques Beyond the Basic Loop

The basic loop is: train a weak supervisor on true labels, use it to label new examples, then train the strong student on those weak labels. The paper tries several ways to improve on that:

- **Naive weak-label finetuning**: the baseline. Train the strong model directly on the weak model's labels. This often beats the weak model, but can also make the strong model imitate the weak model's mistakes.
- **Bootstrapping through intermediate model sizes**: instead of jumping directly from weak to strong, train a medium model from weak labels, use the medium model to relabel data, then train a larger model, and so on. This helped most clearly on chess, where smaller supervisor-student gaps worked better than one large jump.
- **Auxiliary confidence loss**: add a loss term that encourages the strong student to make confident predictions, even when those predictions disagree with the weak label. The point is to reduce imitation of weak-supervisor errors and let the strong model rely more on its own representations.
- **Weak-label few-shot prompting**: test whether the W2S effect appears when the strong model is prompted with weakly labeled examples rather than finetuned. For the largest models this became competitive with finetuning in some NLP settings, though confidence-loss finetuning generally did better.
- **Unsupervised/generative finetuning before reward modeling**: for the reward-modeling setting, first train the model with a language-modeling objective on the relevant comparison data, ignoring preference labels. This tries to make the task-relevant representations more salient before weak-label training.
- **Early stopping / regularization analysis**: ground-truth early stopping is not a valid deployment method, but it shows that strong students can overfit to weak labels very quickly. This motivates methods that prevent the strong model from simply becoming a better imitator of the weak model.

## Questions

- When does weak-label training elicit a concept the strong model already has, versus train the strong model to imitate the weak supervisor's specific errors?
- How much of W2S success comes from pretraining leakage: the strong model having already seen human-level supervision in pretraining?
- Which W2S techniques survive when the weak supervisor is a human with systematic blind spots rather than a smaller model with model-shaped errors?
- Can W2S methods improve reward modeling enough to matter for real alignment pipelines, or are classification-style tasks too forgiving?

## Refs

- [Automated Weak-to-Strong Researcher](automated-weak-to-strong-researcher.md) - Anthropic follow-up that uses W2S as an outcome-gradable environment for automated alignment researchers.
- arXiv:2312.09390 - Weak-to-Strong Generalization: Eliciting Strong Capabilities With Weak Supervision.
- OpenAI announcement: https://openai.com/index/weak-to-strong-generalization/

## Notes

### Interpretation

The paper is useful less because its proposed methods are deployable and more because it gives a clean empirical handle on a central alignment-shaped problem: supervising a model that knows more than the supervisor. The important distinction is between **teaching** and **eliciting**. In W2S, the weak supervisor is not supposed to teach the strong model new capabilities; it is supposed to point the strong model at a task it already has latent competence on.

### Main Failure Mode

The key failure mode is imitation. If the strong student learns "what would the weak supervisor say?" rather than "what is the right answer?", then more training can make it worse relative to ground truth even as it fits the weak labels better. This is why the confidence-loss and early-stopping analyses matter: they are attempts to separate learning the intended task from copying the weak labeler's errors.

### Relation to Scalable Oversight

W2S is an analogy, not the target problem itself. A future human supervisor will not make the same kinds of mistakes as a small language model, and future superhuman knowledge may be less directly represented in pretraining data. Still, the setup is useful because it is cheap, outcome-gradable, and lets researchers test whether methods can recover capabilities beyond the supervisor.
