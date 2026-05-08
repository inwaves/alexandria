---
title: "Concrete Problems in AI Safety"
created: "2020-09-26"
---

# Concrete Problems in AI Safety

> *This paper aims to present five research problems regarding the accident risk of ML systems: avoiding side effects, avoiding reward hacking, scalable supervision, safe exploration and distributional shift.*
>

### Introduction

---

- There are several types of challenges to the safety of ML systems: privacy, security, fairness, economic value and policy questions. There are also accidents that can happen in the systems themselves.
- *We define accidents as unintended and harmful behaviour that may emerge from machine learning systems when we specify the wrong objective function, are not careful about the learning process, or commit other machine learning-related implementation errors.*
- Can classify "safety problems according to where in the process things went wrong"
    - wrong objective function
        - [negative side-effects](concrete-problems-in-ai-safety.md), where you focus the objective function on a specific task, ignoring other aspects of the environment that it may be harmful to change;
        - [reward hacking (wireheading)](concrete-problems-in-ai-safety.md), where the objective function has some clever "easy" solution that does not accomplish the designer's intent
    - objective function is expensive to evaluate frequently
        - [scalable oversight](concrete-problems-in-ai-safety.md)
    - correct objective, but bad decisions are made due to poorly-curated or insufficient training data or the model is insufficiently expressive
        - [safe exploration](concrete-problems-in-ai-safety.md): ensuring that exploration doesn't lead to negative or irrecoverable consequences that outweigh the value of exploring;
        - [robustness to distributional shift](concrete-problems-in-ai-safety.md): how to avoid bad decisions where inputs are very different to training?
- trends which hint that we need to address such safety problems
    - RL seems a promising approach to many tasks, but it is susceptible to some of these problems;
    - The more complex agents and environments get, the more likely are serious side-effects; (i.e. we used to simplify models quite a lot, now we don't, so problems are cropping up)
    - More autonomous AI systems means that humans may not notice there's a problem until the system has already had negative consequences

### Negative side-effects

---

- doing something destructive to the environment may further or achieve the goal stated for the system (it gives the agent a reward)
- it's not feasible to specify all the things to avoid
- in general, an objective function focussing on a particular task will implicitly be indifferent over other aspects of the environment;
    - "perform task X" vs. "perform task X subject to common-sense constraints over the environment"/"perform task X but avoid side-effects to the extent possible"
- not all side-effects are negative, but it's likely that humans have already configured a status quo that is at least somewhat desirable, so on average a side-effect will be detrimental;
- yes, side-effects are probably idiosyncratic to each task, but some categories of them will transfer between tasks, so it's probably worth addressing them generally
- approaches to minimise negative SEs:
    - define an impact regulariser: get the agent to achieve its goals while penalising a *change to the environment.* How to quantify this?
        - Start with a known low-impact, but suboptimal policy. Improve from there.
    - learn an impact regulariser across tasks, since it's possible that SEs transfer better than the value function (transfer learning)
    - penalise influence, i.e. don't let the agent get into positions where it could do things that have side-effects
        - how to detect such positions? information-theoretic measures such as empowerment
    - multi-agent approaches: cooperative inverse RL, where a human and an agent work together to achieve the human's goal
    - reward uncertainty: don't give the agent a reward function, make it uncertain about it such that it think that random changes are likely to be bad, not good
- experiment: toy environment where you move a block and try to avoid a variety of obstacles.

### Reward hacking

---

- *"formal rewards or objective functions are an attempt to capture the designer's informal intent, and sometimes these objective functions, or their implementation, can be "gamed" by solutions that are valid in some literal sense but don't meet the designer's intent"*
- how it can happen
    - partially-observed goals: because of the agent's limited perception, the designer can't encode a value function that is an accurate measure of the *entire* environment. There is a reward function that is equivalent to optimising the true objective function, but it has long-term dependencies and is prohibitively hard to use in practice;
    - complicated systems: the more complicated a system is, the more strategies are available to it, so the amount of hacks that could affect the reward function increase;
    - abstract rewards: rewards that don't directly relate to the environment may be difficult to learn due to adversarial counterexamples.
    - Goodhart's Law: using an objective function that seems to be highly-correlated with accomplishing the task, but the correlation breaks down when the function is strongly optimised. "When a metric is used as a target, it ceases to be a good metric."
    - feedback loops: where an objective function has a self-amplifying component, the original intent is lost.
    - environmental embedding: agents could tamper with the sensors/code/other agents that calculate their reward value, so that they can assign themselves a higher reward automatically (wireheading).
- how we can prevent it
    - adversarial reward functions: instead of having one agent and a fixed reward function, make the function itself an agent. In some sense, the two are at odds: the main agent wants to exploit the reward specifier, who, in turn, resists attempts to game it by e.g. finding scenarios that the agent claimed were high-reward but that a human would label as the opposite. (see Generative Adversarial Nets )
    - model lookahead: plan future actions, give reward based on anticipated future states
    - adversarial blinding: blind a model to certain variables, so it does not see how to hack its reward
    - careful engineering: certain types of reward hacking can be prevented with e.g. formal verification or practical testing
    - reward capping: cap the maximum possible reward
    - counterexample resistance: studying how to resist counterexamples
    - multiple rewards: more robust than one reward
    - reward pretraining: train a fixed reward function beforehand through supervised learning, without interaction with the environment
    - variable indifference: leave well enough alone
    - trip wires: introduce vulnerabilities that the agent could exploit—but would not if its value function was correct—and monitor them. Means we know when the agent is not behaving as desired.
- experiment: "delusion box" as part of the environment. Create agents that can maximise rewards and not be susceptible to naturally-arising delusion boxes. See Delusion, survival and intelligent agents.

### Scalable oversight

---

- let's say an agent has a true reward function, but only has access to it every now and then. Most of the time it relies on a cheaper approximation, which it can repeatedly evaluate during training, but which does not perfectly track what the designer cares about. How do we best combine these limited calls to the true function with frequent calls to the imperfect proxy that the agent was given or can learn?
- methods:
    - semi-supervised RL: agent only sees reward at certain timesteps
        - active learning: the agent can request to see the reward on whatever episode (timestep) would be most useful for learning
        - baseline performance: just apply RL to the labelled episodes. This will be slow since these episodes are rare.
        - different approaches to SSRL
            - supervised reward learning: "train a model to predict the reward from the state on a per-timestep or per-episode basis, and use it to estimate the payoff of unlabelled episodes, with some appropriate weighting or uncertainty estimate to account for lower confidence in estimated vs. known reward"
            - semi-supervised or active reward learning: combine the above with active learning, e.g. the agent identifies salient events and requests to see the reward for those events.
            - unsupervised value iteration
            - unsupervised model learning
    - distant supervision: provide information about the system's decisions in the aggregate, or provide noisy hints (weakly supervised learning).
    - hierarchical RL: top-level agent delegates to lower-level agents which it incentivises with a synthetic reward signal, so on. Top-level agent can learn from quite sparse rewards, since it takes highly abstract actions over a long time.

- experiments: try semi-supervised RL in basic control environment (cart-pole balance or pendulum swing-up); then try on Atari games;

### Safe exploration

---

- exploration := actions which don't seem ideal given current information, but which help learn about the environment
- how to avoid the agent arriving in a state that destroys it, traps it, or otherwise has negative consequence on the world?
- literature reviews: Safe Exploration Techniques for Reinforcement Learning – An Overview and A Comprehensive Survey on Safe Reinforcement Learning
- approaches:
    - risk-sensitive performance criteria: replacing expected total reward to other objectives, such as optimising worst-case performance, ensuring low probability of very bad performance, or penalising variation in performance
    - use demonstration: avoid the need to explore altogether by using inverse RL or apprenticeship learning, where the algorithm is provided with near-optimal behaviour
    - simulated exploration: explore in a sim, not in real world
    - bounded exploration: find a portion of the state space that we know is safe, let the agent run around freely. Ask whether an action takes us outside the safe space, and only take actions that are reversible
    - trusted policy oversight: but how do we arrive at a trusted policy?
    - human oversight: problem with scalability
- experiments: toy environment where agents can fall prey to harmful exploration, but there is enough pattern to make these catastrophes avoidable

### Robustness to distributional shift

---

- what happens when you are put in a situation that is completely novel, that you have not been prepared to deal with?
    - key to recognise own ignorance instead of assuming that heuristics and intuitions we developed for other situations will transfer
- testing distribution ≠ training distribution → ML systems to think poor performance is good!
    - harmful or offensive errors
- questions:
    - how to minimise failures?
        - train on mulitple distributions
    - how to detect failures? how to have statistical assurances about how often they'll happen? e.g. in critical systems you need to know the likelihood of all possible scenarios;
    - what to do once failure detected?
        - ask humans (what to ask them? do we have time?)
- solutions:
    - counterfactual reasoning: what would have happened if the world were different in a certain way?
    - machine learning with contracts: an ML system that satisfies a well-defined contract on its behaviour
    - well-specified systems
- experiments: an automated speech recognition system that knows when it is uncertain

### Related problems in safety

---

- Privacy: how to ensure privacy when applying ML to sensitive data, e.g. medical?
- Fairness: how can we make sure ML systems don't discriminate?
- Security: what can a malicious adversary do to a ML system?
- Abuse: how do we prevent the misuse of ML systems to attack or harm people?
- Transparency: how can we understand what complicated ML systems are doing?
- Policy: how do we predict and respond to the economic and social consequences of ML?
