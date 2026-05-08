---
title: "AI Safety via Conditioning Predictive Models"
url: "https://docs.google.com/document/d/1CE1fFz3vheWkZ08jbV7bN2F5Gkp-AaeDhjOsFiEc568/edit#heading=h.2aunyzdsuoez"
created: "2022-11-21"
---

# AI Safety via Conditioning Predictive Models

# LMs as predictors

- if LLMs are predictive models of the world, why don’t we use them to predict AI safety research from possible futures?
    - raises some potentially fatal safety problems
- “Due to the simplicity of the prediction objective and the power of predicting the future, we think that conditioning approaches for predictive models represent the safest known way of eliciting human-level and slightly superhuman capabilities from large language models and other similar future models.”
    - there’s a lot to unpack here, but I’d be particularly interested in “the simplicity of the prediction objective.” I think they mean next-token prediction is simple relative to other things you could try and do with AI, but I’m not sure how well “predicts the next token well” translates into “predicts the future”
        - to predict the next token, you need to understand how the world influences the distribution of that token
        - there are lots of small, complex interactions that influence your token, so you should account for those when you make your prediction
        - therefore, you should have a really good world model, even if your task is somewhat trivial

### LMs as predictors

- what’s in an LLM?
    - heuristics?
    - a simulator?
    - a deceptive agent?
    - a predictive model of the world?
- prediction objectives are simple, and they may be easier to align to than other objectives
- the setting assuming a predictive model that is multimodal: it can be conditioned on and output images, audio, video, and text
- Bayes nets? how do they work, what’s the point of them?
- conditioning is a form of back-inference: “what are the hidden states most likely to have produced the given observations?”
- pre-training a LLM is like getting it to predict the data collection procedure used to produce its training data

### LMs have to be able to simulate the world

- maybe LMs don’t simulate the world in the same amount of fidelity across the board;
    - the immediate environment of the agents whose text output is important is modelled at higher fidelity than everything else
- this document sees LMs are predictors: they have a model of how the world works, and they use that to predict what their outputs should show

### The power of conditioning

- observation conditionals = conditioning on an observation, a thing which passes through the sensors/inputs of the model, rather than an actual state of the world

### The basic training story

- **training goal**: we want to build purely predictive models, no deceptive agents
- **training rationale**: using pre-training seems pretty safe in terms of producing deceptive agents, and we can “fill in the rest of the gap” using interpretability

# Outer alignment via careful conditioning

- ok, if we have a really good predictive model of the world, what do we actually do with it?
    - we don’t want predictive models to model AI – that’s dangerous
    - we want it to predict the most useful possible human output

### Minor challenges

- some problems are solvable by “getting more cameras” = conditioning on more facts to really pin down what we want e.g.
    - make sure that you condition on reality, rather than fiction
    - use metadata to properly condition on future things (e.g. articles), rather than beliefs about future things
- problem: models don’t actually simulate the future when we condition on things from the future; they just simulate a counterfactual present where those conditions hold
- other issues
    - it’s possible that for really unlikely observations, the model concludes it’s looking at a prompt rather than the actual observation, because it’s much more likely for that to be the case.
    - or it might think that it’s predicting its own output

## Major challenge 1: predicting other (potentially superintelligent) AI systems in the world

- example: simulating an exceptionally strong chess game in 1990 (= played by humans) vs. today (= most likely played by AIs)
- why is it a big issue?
    - your predictive model might be predicting the output of powerful misaligned systems
- “conditioning on strange out-of-distribution observations we may get strange out of distribution worlds in response”

- solutions to this issue
    - machine-checkable proofs
    - conditioning on worlds where superintelligent AIs are less likely
        - there’s a key issue here that I don’t quite get related to ~“if the conditional is unlikely in the world we’re in right now, and we enforce it to be true, the model predicts that the way it would be true is if a maligned superintelligence did something to make it true”
            - I think the gist here is that a conditional might be less likely to be true because it literally happened in the world than because a deceptive agent in the future influenced it to appear true
    - predicting the past
    - condition on worlds where aligned AIs are more likely
    - just ask the model itself what to do
    - …

## Major challenge 2: self-fulfilling prophecies

- worlds are easy to predict if you can just make your prediction happen
    - simpler worlds are easy to predict, this is probably bad for humans
- you can’t just ask an AI to ignore the consequences of its own predictions, because it needs to be able to model what other AIs do, and those AIs would model the original AI
    - so you could condition on worlds where there are no powerful AIs
- this might also be tough, because there is already some evidence that there are AIs: the model itself exists, so it will make predictions that are consistent with it existing
- why would conditioning help here? wouldn’t those counterfactual worlds still exist? how is this essentially isomorphic, though?

    > Another potential difficulty in both cases is if the model exploits acausal correlations to cause self-fulfilling prophecies. For example, even in a world where the model itself doesn’t exist, if models trained in similar ways exist then it could reason that its predictions will likely be similar to those models’ predictions. Such a situation where it is treating its output and that of other AIs as highly correlated is essentially isomorphic to the original self-fulfilling prophecies case. This is another reason that we think it will likely be necessary to Icondition on worlds where there are no powerful AIs at all, rather than just conditioning out our AI alone.
    >


## Major challenge 3: anthropic capture

- I don’t quite understand this part

## Pivotal acts

that can be done with a good predictive model

- use a predictive model to create STEM AI and make progress on whole brain emulation (WBE) or nanotechnology
- make money by predicting technological developments in other fields, use that money to accelerate alignment
- use it to predict short-term consequences and take advantage of those to progress alignment

- paraphrasing: “to get our model to do more, we condition on things that are less likely, so it opens us up to simulation risk” (i.e. the risk that we end up predicting a manipulative malign superintelligence)

# Open problems

- “Understanding whether pre-trained LLMs currently attempt to predict the future or else write fiction about the future when prompted with future dates.”
    - how would you even go about this?
-
