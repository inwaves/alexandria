---
title: "Introducing Superalignment"
url: "https://openai.com/index/introducing-superalignment/"
created: "2026-04-27"
---

# Introducing Superalignment

OpenAI's July 2023 announcement of a dedicated research programme on superintelligence alignment, co-led by Ilya Sutskever (Chief Scientist) and Jan Leike (Head of Alignment). The post is short but the commitments inside it are unusually concrete for an AI lab safety announcement — and the gap between those commitments and what was actually delivered, by May 2024, became one of the more public ruptures in AI safety.

## The thesis

Three claims drive the post:

1. **Superintelligence within the decade is plausible** and qualitatively more dangerous than current frontier systems.
2. **No current technique aligns it.** RLHF works because humans can evaluate outputs. Superhuman systems will produce outputs humans can't reliably evaluate. The supervision signal that aligns today's models breaks at the relevant capability level.
3. **The plan is to build a "roughly human-level automated alignment researcher" and let it solve the rest.** From the post: *"We can then use vast amounts of compute to scale our efforts, and iteratively align superintelligence."*

This is the **automated alignment researcher (AAR) thesis** in its purest form. It does not claim alignment is solvable in advance; it claims it is solvable *by an aligned-enough early system, given enough compute*.

## The two operational commitments

- **Four-year deadline.** *"Our goal is to solve the core technical challenges of superintelligence alignment in four years"* — i.e. by July 2027.
- **20% of compute.** *"We are dedicating 20% of the compute we've secured to date over the next four years to solving the problem of superintelligence alignment"* — billed as "the largest investment in alignment ever made."

## The plan

Three workstreams:

1. Develop a scalable training method (using AI to assist evaluation of AI outputs).
2. Validate the resulting model (through automated interpretability and adversarial testing).
3. Stress-test the alignment pipeline on deliberately misaligned models.

The most-developed empirical leg of (1) was [Weak-to-Strong Generalization](../papers/weak-to-strong-generalization.md) (Burns et al., Dec 2023).

## The team

Co-led by Sutskever and Leike. Reported founding members included Collin Burns, Pavel Izmailov, Leopold Aschenbrenner, Bowen Baker, Yuri Burda, Nat McAleese, Adrien Ecoffet, Harri Edwards, plus the prior alignment team. Aimed for ~20% of OpenAI staff allocated to the programme.

## The dissolution (May 2024)

Timeline of departures:

- **Feb 2024**: William Saunders (Superalignment) leaves.
- **Apr 2024**: Leopold Aschenbrenner and Pavel Izmailov fired (ostensibly for leaking). Daniel Kokotajlo (governance) resigns separately and refuses the non-disparagement clause.
- **May 14 2024**: Sutskever announces departure.
- **May 15 2024**: Leike resigns.
- **May 17 2024**: Leike publishes his X thread (status 1791498174659715494). Excerpts: *"I have been disagreeing with OpenAI leadership about the company's core priorities for quite some time, until we finally reached a breaking point."* — *"Over the past few months my team has been sailing against the wind. Sometimes we were struggling for compute and it was getting harder and harder to get this crucial research done."* — *"safety culture and processes have taken a backseat to shiny products."*
- The Superalignment team is dissolved and folded into other research orgs. John Schulman is named scientific lead for alignment work.

The 20% pledge was never delivered. Fortune (May 21 2024), citing six sources, reported that routine GPU requests from the team were rejected by VP Research Bob McGrew, with CTO Mira Murati involved; the original commitment was never operationalised (annual? cumulative? cohort?). Ordinary inter-quarter "flex" requests were also denied. Leike's resignation thread is the public confirmation that the team had been resource-starved.

## Where the work went

- **Jan Leike → Anthropic** (May 28 2024) to co-lead a "scalable oversight / weak-to-strong generalization / automated alignment research" team. Effectively the Superalignment programme rebranded under different management.
- **Collin Burns → Anthropic**, continuing W2S work.
- **Leopold Aschenbrenner → "Situational Awareness"** essay (June 2024) and a thematic hedge fund.
- **John Schulman → Anthropic** (Aug 2024), then to Mira Murati's Thinking Machines Lab (Feb 2025).
- **William Saunders → Senate Judiciary testimony** (Sept 2024) on AI safety.
- **Daniel Kokotajlo → AI Futures Project** (Oct 2024); subsequent work includes AI 2027.
- **At OpenAI**: scalable oversight and weak-to-strong generalization survive as workstreams listed on alignment.openai.com. The "Deliberative Alignment" line (Dec 2024) is a descendant. A separate "Mission Alignment" team was disbanded Feb 2026.

The honest read: the original Superalignment team is gone, the 20% commitment did not hold, and the four-year deadline was abandoned nine months in. The research line continues at OpenAI in name, at substantially reduced scale and with the original leadership working on the same problem at a different lab.

## Why the announcement matters in retrospect

The announcement was the most concrete public commitment any frontier lab has made to a safety programme. Its trajectory — public commitment, internal resource starvation, public dissolution under a competing-priorities frame — is the canonical case study for the question of whether lab-internal safety culture can hold under product-deployment pressure. That question is load-bearing for the slowdown branch of AI 2027, which assumes a similar commitment can be sustained for long enough to bank alignment progress. The Superalignment story is the existence proof that — at least at OpenAI, between 2023 and 2024 — it could not.

## Refs

- Source post: [openai.com/index/introducing-superalignment](https://openai.com/index/introducing-superalignment/)
- Earlier programmatic statement: [Our approach to alignment research (Aug 2022)](https://openai.com/index/our-approach-to-alignment-research/)
- Leike's elaboration: [Why I'm optimistic about our alignment approach (Dec 2022)](https://aligned.substack.com/p/alignment-optimism)
- [Weak-to-Strong Generalization paper note](../papers/weak-to-strong-generalization.md)
- [Alignment via AI Assistance — analysis](../research/alignment-via-ai-assistance.md)
- AI 2027
- Daniel Kokotajlo profile
- Jan Leike profile
- Collin Burns profile
- Fortune (May 21 2024): [the 20% pledge that never materialised](https://fortune.com/2024/05/21/openai-superalignment-20-compute-commitment-never-fulfilled-sutskever-leike-altman-brockman-murati/)
- TechCrunch (May 18 2024): [team withered](https://techcrunch.com/2024/05/18/openai-created-a-team-to-control-superintelligent-ai-then-let-it-wither-source-says/)
- Leike's resignation thread: [x.com/janleike/status/1791498174659715494](https://x.com/janleike/status/1791498174659715494)
