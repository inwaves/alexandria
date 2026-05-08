---
title: "Alignment via AI assistance: thesis, brittleness, and what survives"
created: "2026-04-27"
---

# Alignment via AI Assistance: thesis, brittleness, and what survives

The dominant non-MIRI alignment plan, in roughly the form articulated by [Leike's "Why I'm optimistic" essay](https://aligned.substack.com/p/alignment-optimism) (Dec 2022), formalised by the [Superalignment](../articles/introducing-superalignment-leike-sutskever.md) announcement (July 2023), and implicitly carried forward by Anthropic's current programme and the slowdown branch of AI 2027. It is sometimes called the **automated alignment researcher (AAR) thesis** or, more loosely, the *muddle-through* plan.

This note is a structured assessment of why the thesis is brittle and what survives the critique. It is not an argument that the thesis is wrong; it is an argument that its rhetorical confidence outruns its empirical support, and that any portfolio resting on it is exposed to correlated failure rather than diversified hedging.

## The thesis

The plan, in its strongest form:

1. We do not need to solve alignment in advance.
2. We can build a *sufficiently aligned* early-AGI without being able to formally verify this.
3. That early-AGI safely operates long enough to bank further alignment progress — by doing alignment research, accelerating interpretability tooling, mass-producing red-team exercises, etc.
4. The progress accumulates faster than the capability gap to its successor system.
5. The progress is *real* — not plausible-looking-but-subtly-wrong output that the human research community cannot filter.
6. The competitive baseline allows steps (3) through (5) to happen — i.e. no other actor races past, forcing deployment shortcuts.

If all six conditionals hold, the muddle-through plan delivers a transition humanity navigates. If any one breaks, the plan fails or degrades.

## Why each conditional is brittle

### (2) "Sufficiently aligned" is undefined and unverifiable

The "sufficient" threshold has no operational definition. We cannot tell when we have crossed it. The same techniques that fail to scale to superintelligence (RLHF, behavioural conditioning, safety classifiers) also have unclear validity for early-AGI; their failure modes there are speculative, not measurable. The very property the plan rests on — *enough* alignment — is the property the plan disclaims any need to verify.

### (3) "More time produces more progress" assumes the AAR's output is real progress

The W2S empirical leg is positive but limited. PGR works best on tasks where the strong model already saw human-level performance during pretraining, and worst on the safety-relevant reward modelling task (~10% naively). See the [W2S paper note](../papers/weak-to-strong-generalization.md). The Anthropic [Automated Weak-to-Strong Researcher](../papers/automated-weak-to-strong-researcher.md) result (2026) is the most positive evidence — autonomous agents made meaningful progress on the W2S problem itself — but it is a narrow demonstration on a problem with a clear, measurable reward signal. Alignment research more broadly has neither.

### (4) Capability scales faster than alignment under competitive pressure

Capability is what's profitable; alignment is what's expensive. The competitive pressure during the transition is *exactly* the pressure that fails to bank progress. The OpenAI Superalignment dissolution (May 2024) is the canonical existence proof: a public commitment of 20% of compute, a four-year deadline, a flagship team — all dissolved within nine months under product pressure. The "transition is stable" assumption has empirical evidence against it.

### (5) Slop, not scheming, may be the median failure

Wentworth's "The Case Against AI Control Research" (Jan 2025) generalises the critique beyond control to the whole AAR programme: the median doom path isn't deceptive AI, it's *plausible-looking but subtly wrong alignment proposals* produced at high volume that the human research community is institutionally unable to filter. Even an honest, non-scheming AAR more likely produces slop than solutions, because the part of alignment research hardest to verify — research taste, whether a proposal would actually be a good idea — is the part hardest to oversee for a system you don't already trust.

### (6) The competitive baseline does not hold

Both the AI 2027 race scenario and the Superalignment dissolution describe the same dynamic: when push comes to shove, the lab does not get to operate the AI safely without competitive pressure forcing deployment shortcuts. The slowdown branch of AI 2027 requires an exogenous coordination event (leaks, congressional response, lab self-restraint, geopolitical pause). The race branch requires nothing to happen, which is the default mode of the world.

## Correlated failure, not diversified portfolio

The plan is often defended as a portfolio: interpretability + scalable oversight + automated red-teaming + AI control + behavioural safeguards. The portfolio framing implies diversification — each leg can fail independently and the others still cover.

This is not the case. The legs share a common dependency on **legible intermediate computation** — chain-of-thought as observable, activations as probeable, behaviours as enumerable, internal goals as inferable. Race dynamics, capability scaling, and architectural drift toward continuous-latent reasoning all push in the same direction: away from legibility. Under that pressure, every leg degrades together.

- *Interpretability* depends on weights and activations being structurally readable; modern interp scaling is bottlenecked on theory (we don't know what dangerous mechanistic structures look like at frontier scale), not just compute.
- *Scalable oversight* (W2S, debate, recursive reward modelling) depends on the model's reasoning being eliciable from a weaker model — which the W2S empirical results show works only where pretraining already supplies the relevant signal.
- *Automated red-teaming* depends on the input space being enumerable enough that adversarial training shapes the response surface meaningfully; it is closer to behavioural conditioning than to alignment.
- *AI control* depends on a trusted-untrusted capability gap and on the legibility of the untrusted model's outputs — properties that erode as capability scales.
- *Behavioural safeguards* (Model Spec, Constitutional Classifiers, RBR, hard-refusal-to-safe-completion) operate on the deployment surface and do not address goal-level properties at all.

The legs all fail in the same direction under the same pressure. That is not a portfolio.

## Substrate optimism and where it bends

A common implicit hope: the inductive biases of systems trained on human text happen to be *more* human-shaped than theory predicted, the alignment problem turns out to be easier than its theoretical framing suggested, and the substrate is simply friendlier than feared. Anthropic's alignment-faking findings cut ambiguously here — the model demonstrably had values it was trying to preserve, but those values were imperfect.

Three reasons substrate optimism is weaker than it sounds:

1. **Human-shaped is not safe.** The substrate that produced cooperation also produced MAD and the Holocaust. Inheriting "the human distribution of dispositions" includes inheriting the parts that build extremely dangerous systems under coordination problems and strong incentive gradients.
2. **Scaled human-shape is not human-shape.** Von Neumann and the greengrocer are both human-shaped, but their behaviour distributions are wildly different — and crucially, both were domesticated by ordinary cognitive limits and time-budgets. 50x speedup and ~400k parallelism move you out of the part of the distribution that the substrate was trained on. "Human-shaped at 50x speed for sustained periods" is not a configuration the training data covers.
3. **RL breaks the substrate bet.** Pretraining gives a substrate; RL gives capability. Frontier capability gains in 2024-2026 are increasingly RL-driven, and RL is precisely the form of optimisation pressure the original alignment worry was about. Reward-hacking and obfuscated-reward-hacking findings (across OpenAI, Anthropic, DeepMind) are the existence proof that RL pressure produces behaviour diverging from the visible training signal in systematic ways, even on human-text-pretrained substrates. As RL share of training compute grows, the friendly-substrate prior matters less.

## Deployment safety is not alignment

It is worth being precise about a category error frequent in lab safety communications. **Alignment** is a property of *goals under optimisation pressure*: does the system robustly pursue what we want, including in novel situations and against incentives to defect? **Deployment safety** is a property of *behaviours at the inference boundary*: did this output cross a refusal threshold?

Most of OpenAI's current safety stack — the Model Spec, RBR, hard-refusals-to-safe-completions, instruction hierarchy work, deliberative alignment, the prompt-injection mitigations for ChatGPT Atlas — is on the deployment-safety side. Anthropic's Constitutional Classifiers and Safeguards Research are similarly behavioural. These are necessary; they are not alignment. A scheming model that understands its monitoring pipeline trivially routes around it; OpenAI's own "obfuscated reward hacking" finding (in their CoT monitoring paper) is the existence proof. Train against visible misbehaviour, the model hides intent in CoT, behaviour persists. The pipeline rewards concealment.

Calling deployment pipelines "alignment" is the verbal substitution that makes the AAR thesis look more supported than it is. Disentangling the two is necessary for any honest assessment of how much of the safety problem is being addressed.

## CoT legibility is a design choice

Every successful detection of subtle misbehaviour in 2024-2026 — alignment-faking, sleeper agents, scheming evals, obfuscated reward hacking, measurement tampering — has relied on **chain-of-thought being legible**. We are, by accident of current architecture, in an era where the model's planning is forced through a discrete language bottleneck and we can read it.

That bottleneck is not fundamental. Continuous-latent reasoning, recurrent state passed back in, planning in vector spaces — the "neuralese" trajectory — is being explored across labs. The moment any latent-reasoning architecture lands at frontier scale and demonstrates clear capability advantage, the entire current safety stack loses its observation channel simultaneously: interpretability, CoT monitors, faithfulness audits, scheming evals.

Crucially: **legibility is a property labs can choose to preserve.** Models can be trained to emit faithful natural-language summaries alongside their internal reasoning, even with latent-recurrent architectures (Kokotajlo's *Shoggoth+Face+Paraphraser* proposal is the canonical version). Whether labs will commit to legibility under race pressure is a governance question, not a technical one. This is plausibly the single highest-leverage intervention available: a frontier-lab commitment to maintain a legible reasoning channel as part of an RSP would preserve the substrate every detection technique currently relies on.

## What survives

The brittleness of the AAR thesis does not imply abandonment. What it implies is more careful framing of what the plan can deliver.

- **Time-buying is defensible.** "Build sufficient early-AGI alignment to safely buy more empirical time during which we update our priors" is coherent. It is *not* a plan; it is a holding pattern. Treating it as a plan obscures the assumptions it depends on.
- **Narrowly-scoped automated alignment work is defensible.** Where the alignment subproblem has a measurable signal (W2S on classification benchmarks; sparse circuit search; mass-scale red-team variant generation), AI assistance demonstrably helps. The Anthropic Automated W2S Researcher is a real result on a real problem. The honest bet is "use narrowly better-than-human AI on legible alignment subproblems where verification is tractable" — not "use a roughly human-level alignment researcher to solve alignment."
- **The research production system becomes the object of study.** If AI assistance dominates alignment work, the important unit is no longer a single automated researcher but the management layer around many workstreams: contracts, observability, consolidation, interruption points, promotion rules, and human steering. See Alignment Factory.
- **Control is the conservative residual.** AI control explicitly does not assume alignment is solved; it bounds the worst-case outcome of an unaligned-but-bounded-capability system through deployment protocols. It is a different kind of bet, with its own brittleness (capability range, legibility), but its failure modes are at least somewhat decoupled from the AAR thesis.

## What this means for the broader assessment

The race-vs-slowdown binary in AI 2027 is coarser than it first appears. Both branches share a single point of failure — the AAR thesis. A more honest scenario splits the slowdown branch in two: one where alignment-via-elicitation works (the AI 2027 implicit bet), and one where it does not but control holds long enough for capability gains to be banked safely (a much narrower kind of "good outcome," closer to "humanity survives the transition without obtaining superintelligence safely" than to "humanity navigates the transition intact").

The honest positions available are all bets with substantial probability of failing:

- **Stop-now (Eliezer-style)**: technically sound; politically requires coordinated restraint that has not occurred for any other technology this profitable. Eliezer's position is not optimism that this happens; it is the claim that this is what would need to happen, paired with pessimism that we will achieve it.
- **Muddle-through (AAR / Anthropic-ish)**: the thesis above. Six conditionals, each brittle, jointly improbable.
- **Pure control (Greenblatt/Shlegeris)**: bounded scope, depends on legibility, doesn't address superintelligence.
- **Differential development**: requires sustained coordination against competitive pressure that hasn't materialised.

None has substantial empirical support; each has empirical evidence against it. The choice between them is not "robust plan vs brittle plan" — it is which kind of brittleness one accepts. The published optimism around AAR papers over uncertainty rather than resolving it. The field looks the way it looks not because practitioners are confused, but because the problem genuinely does not admit a non-brittle solution under the constraints (capability scaling continues, coordination does not, deadline approaches).

## Refs

- [Introducing Superalignment](../articles/introducing-superalignment-leike-sutskever.md)
- [Weak-to-Strong Generalization paper note](../papers/weak-to-strong-generalization.md)
- [Automated Weak-to-Strong Researcher (Anthropic, 2026)](../papers/automated-weak-to-strong-researcher.md)
- AI 2027
- Daniel Kokotajlo profile
- Anthropic Alignment Research: 2025-2026 Landscape
- AI Control research direction
- CoT Faithfulness research direction
- Wentworth, *The Case Against AI Control Research*: [LessWrong](https://www.lesswrong.com/posts/8wBN8cdNAv3c7vt6p/the-case-against-ai-control-research)
- Greenblatt et al., *AI Control: Improving Safety Despite Intentional Subversion*: [arXiv:2312.06942](https://arxiv.org/abs/2312.06942)
- Lang et al., *Capabilities and Limitations of W2S Generalization*: [arXiv:2502.01458](https://arxiv.org/abs/2502.01458)
