---
title: "Acceptability verification: a research agenda"
url: "https://docs.google.com/document/d/199Lkh78UA2uI9ljLEy_aWR8RBetQLRO6Kqo3_Omi1e4/edit"
created: "2022-07-04"
---

# Acceptability verification: a research agenda

I interpret this document as a summary of Evan’s thinking on alignment, a “presentation of [his] worldview rather than just a list of open problems”. The idea of the document is to recruit more people to work on this problem.

I’ve read the first two sections of this document.

# 1. The challenge of prosaic AI alignment

## Preliminaries

- this research agenda operates in the prosaic alignment alignment paradigm, i.e. we’re not missing any fundamental insight about intelligence before we can build human-level AI; we can just scale up what we have now
- Evan expects that the “basic paradigm of machine learning—where we build simple training processes that then train more complex models that then act in the world—to continue”
    - we likely will not be building these models from scratch
- why prosaic AI?
    - aligning current systems not so promising because some problems that might arise in future systems just do not arise in these systems yet
    - aligning “in the abstract” not so promising because our best guess is still the kind of stuff that we have today
    - aligning “far-future” systems: well, we’ll have more time to align those relative to how long we have to align systems we’ll get very soon
- Evan’s framework for thinking about this is “charting safe paths through model space”
    - make sure that as a model is trained it does not enter unrecoverable regimes where the model becomes dangerous and our feedback mechanisms cannot fix it
    - example: deceptive alignment (DA)
- there’s some chance that we get alignment by default, which Evan estimates at 5-10%;
    - related to the broad basin of corrigibility (BBOC) argument that Paul Christiano makes in Corrigibility (AI alignment on Medium): most proxies for models to learn tend to be the ones we want anyway
- close (in some space) to those worlds, there are worlds where alignment almost works by default, but we need to do some clever work to push training in the right direction
    - it might not take that many more bits of optimisation to push training in the right direction, i.e. to find the right models rather than wrong sorts of models; see more on: Operationalizing compatibility with strategy-stealing
    - absent those bits to nudge optimisation in the right direction, we’re at the mercy of inductive biases, which in the case of e.g. stochastic gradient descent (SGD) are actually against us (simplicity prior (SP) → deceptive alignment)
        - the more we can do to nudge, the better we can overcome the extent to which these inductive biases do not overlap with out preferences
- one side-take: Evan thinks that we live in a “messy alignment” kind of world, where we have to figure out what to do before we’ll ever know what alignment *is really about* (we never develop a clear theory of AI alignment)
    - in a clean alignment world we’d be able to come up with something like “provably beneficial AI”, but it doesn’t seem like that’s going to be possible here
    - we can still do our best to survive conditional on messy alignment though

## The crux of the prosaic alignment problem

- Evan also believes that the difficulty of the prosaic alignment problem is related to the “exact nature and structure of the inductive biases of the training process we end up using to produce the first advanced AI”
    - operationalising inductive biases of a training process as “everything that goes into determining what model it produces that isn’t the loss function” including the impact of “the architecture, of SGD, and of initialisation”
    - The other thing that can help us influence training is incentives:
        - behavioural incentives := defined in terms of the model’s output
        - mechanistic incentive (MI2)  := defined in terms of the model’s internal cognition
- the whole P=NP? thing that applies to adversarial examples basically means that we can’t get good worst-case guarantees about how our model will behave just from the behaviour of the model
    - we need to understand our models better than just simple validation/test performance
- Evan then makes the case that deception is probably one of the hardest problems we can grapple with right now, because it undermines our feedback mechanisms and leads to unrecoverable errors
    - lots of other problems to solve, of course, but this one in particular really screws us over if we can’t take care of it
- by undermining feedback Evan essentially means that deceptive AIs measure well on our evaluations – they can get good loss if the loss is defined using behavioural incentives, and still be deceptive and turn on us at the right moment
    - one of the ways to get around it is mechanistic incentives – Evan calls this the **path-dependency approach** := accept that there are deceptive models in the model space you’re searching over, and try to make sure that your search process just never finds them
    - the other is **model space restriction :=** restrict the model space such that it does not contain deceptively aligned models
        - this is unlikely to work though, because it’s compute that leverages most AI progress recently, not careful design of the models
        - also, if you “align” one architecture and a different one comes along that is just much better, you have to start again

## A solution to deceptive alignment

- the path-dependency approach is the one Evan’s most excited about, and he sees it as having two main levers that we can pull: inductive biases and incentives
    - and more specifically the relaxed adversarial training (RAT) approach, where the overseer has access to the internals of the model $M$ and can use transparency tools to evaluate the probability that a model is deceptive or catastrophic overall/on a given input
- the gist of the idea is that we want to use transparency tools to understand what we need to know so we can disincentivise deceptive alignment
    - what kind of properties do we need to look for?
- at some point, we want to have training transparency, so we can steer our training process away from areas that might feature deceptive models
    - currently we only have “inspection” transparency: we can look inside models after they’re deployed and glean *some* insight, but this isn’t something we can do, say, at each optimisation step
- we want to find acceptability predicate (AP2)s that aren’t hard to incentivise but guarantee nice properties, like not having deception
    - these should be mechanistic properties that imply the thing we want, they aren’t that thing itself (e.g. corrigibility implies that you don’t get deception)
- apparently, Rice’s theorem (RT3) says that we can’t even evaluate whether some model has a particular behavioural property, even with mechanistic access
    - but we can check for a mechanistic property that implies a desirable behavioural property
- bottom line: we need better interpretability/transparency tools so we can implement acceptability verification

# 2. Bridging the gap: from current transparency research to acceptability verification

- right now, there are certain predicates an overseer can check and certain acceptability predicates that we might want to verify to get aligned systems
    - they don’t overlap, and we want to get them to overlap

!Untitled

- the main body of work on transparency is Chris Olah’s work on circuits, most recently transformer circuits and induction heads
    - limited, sure, but it’s getting better and better
    - Chris’ intuition: as models get stronger, they develop more and more human-like abstractions, and then less human-like after they pass our performance threshold
- there is also Daniel Filan’s work on clusterability ($\simeq$ the ability to separate portions of a network into neighbourhoods that only functionally connect to each other via minimal edges)
- our transparency tools aren’t there yet so we want to do two things
    - make better tools
    - make more transparent systems: since we don’t depend on random chance to find the systems we want, we can incentivise higher transparency
- Evan thinks there’s low-hanging fruit in transparency work, mainly because there are not that many people who are working on it directly
    - there are related areas like explainability which is not entirely the same (= producing explanations of what models are doing without actually making the models themselves easier to train)
        - equivalently, picking some other model type (or machine learning approach) that is much more interpretable, but not as competitive
- it could be that training transparency is hard because our approaches don’t give us real information: models that look transparent may not necessarily be transparent, so we Goodhart's law (GL) on those metrics
    - again, it seems like most of the issue here comes from deceptive AIs that obfuscate their reasoning to seem transparent but are not really transparent, e.g. they can control which neuron seems to maximally activate for a particular input
    - Evan: “I’m generally pretty skeptical of any strategy that relies on being robust to potentially superintelligent adversarial optimization pressure, of which this is exactly such a case—similarly to why I’m skeptical of something like AI boxing”
        - tl; dr: don’t play stupid games with beings more intelligent than you
-
