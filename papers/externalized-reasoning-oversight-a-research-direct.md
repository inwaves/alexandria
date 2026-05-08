---
title: "Externalized reasoning oversight: a research direction for language model alignment"
url: "https://www.lesswrong.com/posts/FRRb6Gqem8k69ocbi/externalized-reasoning-oversight-a-research-direction-for"
created: "2022-08-05"
---

# Externalized reasoning oversight: a research direction for language model alignment

## Summary

This approach tries to address some of the subproblems of alignment, if not alignment itself, by carrying out oversight on the chain of reasoning of a LLM. Some recent work with LLM has uncovered that in some situations, getting the model to lay out arguments for why it made a particular prediction leads to better accuracy overall. The idea here is to force these models to always explain their reasoning, and to oversee that reasoning. If the reasoning itself is doing something undesirable, then we fine-tune the model using reinforcement learning from human feedback (RLHF). There are three conceptual steps for this to work: we want to verify that the reasoning is authentic, we want to create models that reason authentically, and we want to oversee the reasoning itself. (Here “authentic” is used in an idiosyncratic way.)

I think the core idea is that chain of thought (CoT) gives you a window into what a model “thinks”, and what it is using to make a particular prediction. It is a weaker form of mechanistic interpretability (MI2) –– where ideally you’d be able to point to a component and say that it is responsible for an outcome –– which means that it’s more tractable (you can play with it today) and possibly easier to game by a sufficiently advanced AI (by my lights, you can game outputs, but you can’t game internals). For example, I don’t think that this addresses deception; an AI that is deceptive can obfuscate its reasoning such that it seems authentic, maybe similarly to how in gradient hacking (GH) a model forces itself to “think” something so it does not get updated in an undesirable way.

I don’t feel excited about this proposal at this time, though I haven’t thought through the implications of it enough to see it working. Right now, it’s floating as just another thing that people have thought about, thrown into the grab-bag of proposals I’ve glanced over. However, the proposal seems to be more falsifiable today than other approaches: we can play with these models and see if the tests work.

If Tamera Lanham made progress on this, how would that change my views?

- I’d feel more optimistic about mechanistic interpretability fully solving deception/inner misalignment if this could detect it;
- I’d be more optimistic that we can align current systems
- I’d maybe be more optimistic that something like eliciting latent knowledge (ELK) is possible, in the naive reading I have of the term now before I’ve even read the full proposal doc/other write-ups related to it. I think that if you can get a model’s knowledge by just asking it to use it publicly, that’s a pretty easy way out. It’s easier/more immediate than the “brain surgery telling us what this person thinks” kind of approach of mechanistic interpretability (MI2), but I also wonder if it’s more limited.

## Questions

- Are there cognitive processes that you can’t externalise through this method? Are there things that a model would never be able to show us, even if they were relevant to the prediction it made? (Disentangle “could” from “would do so if requested”.)
-

# Original notes

TLDR

- force a model to lay out its chain of thought
- do oversight on the chain of thought/reasoning
- ???
- fix deception, power seeking, “disapproved reasoning”

- recently, getting large language model (LLM)s to do chain of reasoning has improved their performance, notably on Maths tasks
    - why don’t we try and use this for alignment?
- one statement that I agree with: “reasoning oversight should provide stronger guarantees of alignment than oversight on model outputs alone”
- externalised reasoning := a prompting strategy for a LLM that makes it “show its work”, producing a bunch of steps of reasoning

What needs to happen for this to work as an alignment strategy

1. verify authenticity of reasoning
    - causal responsibility: the reasoning is what the model actually uses to make a decision
    - completeness: no steps are missing at the current level of detail
    - straightforwardness: no hidden messages encoded in the reasoning
2. create authentically reasoning models
    - make models dependent on doing externalised reasoning by limiting their serial computing power (fewer parameters, less depth)
3. oversee the reasoning
    - given 1. and 2., we can rule out unacceptable reasoners, or fine-tune to get acceptable ones
    - use some automated oversight tools to scan reasoning for elements we don’t approve of: convergent instrumental goals, deception, non-myopia
    - if we see those, fine-tune using RLHF over the reasoning process itself
