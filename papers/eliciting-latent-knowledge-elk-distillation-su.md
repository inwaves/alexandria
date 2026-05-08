---
title: "Eliciting Latent Knowledge (ELK) - Distillation/Summary"
url: "https://www.lesswrong.com/posts/rxoBY9CMkqDsHt25t/eliciting-latent-knowledge-elk-distillation-summary"
created: "2022-08-20"
---

# Eliciting Latent Knowledge (ELK) - Distillation/Summary

# Introduction

- regardless of the alignment strategy you choose, you still run into the scenario where sufficiently powerful models create problems that can only be solved if you can understand what the model “truly thinks”; this is what eliciting latent knowledge is
    - example: in debate you want to trust the debate AIs, which you could do if you had ELK
- ELK: “how would the model explain what it was doing if it had just drunk a truth serum?”
- How ELK work has gone so far: come up with a theory, then counterexamples, then patch those counterexamples

# Summary of the ELK paper

## Toy scenario: the SmartVault

- you want to build a vault to prevent a diamond from being stolen
- you have a smart vault that can take many actions to ensure the safety of the diamond, like opening trap doors, using robot arms, whatever
    - some actions the vault takes are obvious to us, some are impossible to understand
    - you can evaluate the state before and after the action by looking through a camera
- you want to train an AI to operate all the actuators for you by training on observations
- the problem is that observations can appear good but be bad in reality, e.g. row 2 below

Untitled

- you could add more sensors, but those could be gamed as well;
    - what you actually want is the AI to not try to fool us, you want it to tell us that someone has tampered with the sensors
- so ask the AI the right questions: “is the diamond still on the pedestal? is there a screen in front of the camera?”
- jointly train a reporter model to answer questions about the internal state of the vault AI, i.e. about its knowledge
    - failure mode with direct translation and simulator
    - the direct translator actually tells you what you should know about the state of the SmartVault AI
    - the simulator learns how you think, and tells you what you want to hear, without raising suspicion;
        - analogy with powerful political leaders accidentally surrounding themselves with yes-men and getting successively worse advice
- one way of looking at the way ELK research is designed is as a game between a builder and a breaker:

    Untitled

    - the builder is designing the model (choosing a training strategy, describing a kind of reporter that it wants) and the breaker red-teams those proposals by finding test cases where the strategy fails, or ways in which an alternative reporter could be learned
- you play this game until you
    - find an algorithm that addresses all counter-examples, which is then our best bet for actually implementing ELK;
    - find a counterexample that can’t be addressed by any algorithm you can come up with, in which case it seems like ELK is not something we could implement (for now/at all
- ELK research works with worst-case guarantees: if some strategy works in the average case of that counter-example but fails in the worst case, then the strategy is defeated
- what’s a counterexample?
    - it’s an example where the reporter gives an answer that is unambiguously bad:
        - the reporter understands the question,
        - the answer it gives is wrong in a way that a human can understand, and
        - the model knows that this answer is wrong, i.e. it makes predictions as if that were not an accurate description of its latent knowledge)

## Constructing a dataset that separates “correct” from “looks correct to a human”

- or: how do you get the reporter to learn the direct translator rather than the human simulator?
1. Have a human operate the vault instead, generating data that is more reliable than an observer looking through the sensors
    - in this case the reporter learns to simulate the operator’s knowledge rather than the observer’s
    - but then the reporter learns to simulate a combination of human observer + human operator
2. have AI help humans improve our understanding of the SmartVault
    - assume that there is an AI that can do science (i.e. learn about the world) and describe its results as well as possible
    - then we now learn things about the SmartVault and add test cases around those such that any reporter that simulates the observer doesn’t know about those and fails the test cases
    - but this is not training-competitive: the science AI would take much longer to train relative to the SmartVault AI, so it’s not a good solution to ELK
        - put another way, learning everything about the world in order to learn something about a small domain seems (a) overkill, (b) much slower
3. have humans adopt the optimal model, e.g. through imitative generalisation (IG)
    - search a space of changes that one could make to the model to maximise a function which maps from [proposed change to the model] → [how a human + AI assistant would make predictions after that change]
    - the idea is to make the AI answer more like a human would answer;
    - use this to improve the human model with the same amount of compute you’d use to train the SmartVault AI anyway
    - but this introduces ontology identification (OI)  problems, because the AI might not learn the same ontology as humans and so the reporter might not be able to explain those concepts to us in a way we understand
        - or: the best way to explain the world might not be in a way that is human-legible


## Regularising against bad reporters

1. Penalise complexity
    - human simulators might be more complex than the direct translators (which depend on how complex the SV model is), so if we penalise complexity we make it less likely that the reporter learns this
    - but if it’s the other way around, you incentivise the wrong thing
2. Penalise computation time
    - intuition: simulating humans requires doing inference in a human model; direct translation should just mean looking up the correct answer in the SV AI model
    - but the bigger the SV AI model gets, the more incentivised the reporter is to simulate the human instead
3. Penalise depending on downstream variables
4. Penalise when reporter works with many predictors
    - core problem: what distinguishes the direct translator from the human simulator?
        - well, a reporter that’s robust to changes in the underlying model they should be reporting on are probably optimising for the human rather than the model
    - perturb the SV model and rule out reporters that are robust to those perturbations
    - worst case counterexample: a reporter that just memorises the SV AI model and reports gibberish otherwise
5. Penalise inconsistencies across different inputs



## Why work on ELK?

- worst-case solution to ELK = progress on outer and inner alignment
- it’s crucial but narrower than alignment as a whole, so you can do away with some concepts that are fuzzy/make the solution to alignment harder for the time being
- we have to avoid untruthful powerful AIs anyway
- even if we don’t solve the worst case our strategy might still work decently well in practice

# ELK competition prizes

- multiple strategies that people proposed for solving ELK which were rewarded with cash prizes
1. Train a reporter that’s useful for another AI system
    - this works by disincentivising the reporter from mimicking the human expectations on the original model
    - you still get a good reporter because it is trained to do well on another model
    - you could get steganography failure modes here if the reporter has logic that seems ok to the aux model but is actually modelling the human
2. Require the reporter to be continuous
    - the human simulating reporter only reports tampering if it knows that humans will see it independently (to remain inconspicuous); the direct translating reporter will flag up tampering all the time that it happens, regardless if a human is able to see it directly
        - for example, one would only report tampering at a camera frame that is visible to humans, and the other would report it even between frames
    - but the reporter’s latent space might not be continuous, so it can’t actually report those things
3. Penalise reporters for depending on too many activations from the predictor
    - this proposal is similar to the “penalise depending on downstream variables” thing above, so I still don’t get it
4. Compress the predictor’s state so that it can be used to answer questions but not tell what a human will believe
    - how do you actually do this, though?
5. Use the reporter to define causal interventions on the predictor
    - let the reporter intervene on parts of the internals of the predictor, then rerun its computation
    - if it answers differently, it must be the translator rather than the human simulator, because the latter doesn’t actually care what the predictor does, it only cares what the human wants to hear
    - counterexample: we could be fooled into believing that the reporter made some intervention when it actually didn’t
        - though here it’s unclear to me why this matters. If the reporter fakes making an intervention and still doesn’t change its prediction, then we know it’s not a direct translator, because it didn’t actually try to intervene
6. Train the predictor to use the human model as a subroutine
    -
