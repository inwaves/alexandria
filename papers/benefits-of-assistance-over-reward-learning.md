---
title: "Benefits of Assistance over Reward Learning"
url: "https://drive.google.com/file/d/1Xp9p6RLNjZrgsdEbGIJK61FnV_drDTQf/view"
created: "2021-08-09"
---

# Benefits of Assistance over Reward Learning

1. *What question is this paper trying to answer?*
    - How do assistance-type agents differ from reward learners? Are they better, worse, the same? Are they easier to train? Do they have more obvious failure modes? Do they scale?
2. *Which hypotheses were tested? What was the methodology?*
3. *What were the findings? What did they mean?*

# Abstract

- really, we now have two paradigms within human feedback RL
    1. **Reward learning**: agent learns a reward model through human feedback provided externally from the environment
    2. **Assistance**: the human is modelled as part of the environment, and the true reward function is modelled as a latent variable in the environment
- the difference is that in (1), learning the reward and using it to control behaviour are separate (cf. the two components in Deep Reinforcement Learning
from Human Preferences (the Noodle Backflip paper)), whereas in (2) they are merged - done by the same policy.
- because they are merged, agents can learn about how the actions they take impacts what they learn about the reward
    - they exhibit desirable qualitative behaviours that we don't see in reward learner agents

# Introduction

- traditional CS: instructions on *how* to do something
    - lots of tasks don't lend themselves to this sort of solution: translation, for example

- abstract that away: why not specify *what* to do, but let the machine figure out *how* to do it?
- but, as we approach more and more complex tasks, even specifying becomes difficult
    - specifying the reward manually leads to specification gaming behaviours
    - in lots of complex environments, we have an endless list of "dos and don'ts" which is impossible to specify
- abstract again: create an agent that is uncertain about the objective and infers it from human feedback
    - make agents that optimise *our* objectives, not *theirs*.

!Untitled

- more formally, the goal for the robot *R* is to maximise an unknown goal of a human *H* who is part of its environment.
    - if we know the human's decision function, i.e., to an approximation, how it reasons, then this is a POMDP, and can be solved using existing algorithms
- key insight: single control policy > separate reward learning and control modules, because the action selection can now take into account the reward learning process
    - in plain English: the agent can do things that maximise reward, and *find out more* about the reward at the same time


# Background and Related Work

- POMDP (Partially Observable Markov Decision Process) formalism where the solution is given by a policy $\pi : (O \times A)^* \times O \rarr \Delta(A)$ that maximises the expected sum of rewards [long ass equation I'm **not** typing out]
- two variants of reward learning
    - *non-active reward learning*: the agent must infer the reward by observing human behaviour
    - *active reward learning*: the agent may ask particular questions of H to get specific feedback
- the underlying formalism for reward learning replaces the reward in the POMDP with a parameterised reward space $\langle \Theta, r_{\theta}, P_{\theta} \rangle$, where the agent can learn about $\theta^k$ by observing the human make $k$ different choices $c$ chosen from a set of potential choices.
- it also has access to the human decision function $\pi^H (c | \theta)$ - H for human - (read this as "the human's policy to make a choice $c$ given a reward function parameterised by $\theta$")
- given this formalism, a policy decision function produces a policy $\pi^R$ (R for robot) that maximises the expected reward
- for active reward learning, $\pi^H$  depends on the questions asked
    - which means: ask good questions, get a much better idea about what the human wants
    - what are good questions? well, different measures, like information value
        - but highest information value questions may be hard to compute
- what **assistance** tries to achieve is incentivise helpful behaviours like reward learning by making it such that R does not know the true reward and can only learn it by observing human behaviour.
- assistance game formalism
- an **assistance problem** is $\mathbb{P} = \langle \mathbb{M}, \pi^H \rangle$ where $\pi$ is the human policy for the assistance game $\mathbb{M}$.
- if we consider $\pi^H$ to be part of the environment, we can reduce the assistance problem to a POMDP (Partially Observable Markov Decision Process) $\mathbb{M}'$, they are equivalent
- that means any POMDP solver can be used to find the optimal $\pi^R$, instead of algos particular to reward learners

# Reward Learning as Two-Phase Communicative Assistance

- reward learning, as stated above splits the reward learning and the control into two separate phases
    - humans can only communicate reward information to the robot
- assistance merges them into one phase
    - humans can actually help with the task
- **communicative assistance problem** = the human doesn't change the world state except insofar as it communicates the reward to the robot
    - i.e. there's a communication phase when the robot cannot act and an action phase, where the human cannot communicate and the robot only can act
- reward learning problems are communicative assistance problems and vice versa

# Qualitative Improvements for General Assistance

- if we remove the two-phase restriction typical of reward learning problems, we see two behaviours:
    - **relevance-aware active learning** := only asking questions when they become immediately relevant to the task at hand; this is important because it's not scalable to clarify preferences of *all possible scenarios*
    - **plans conditional on future feedback** := acting in a particular way knowing that at some point in the future there will be feedback that clarifies what should be done (sort of "do the obvious things first, leave the unclear ones for later")
- if we remove the communicative restriction, i.e. the human can act themselves, we get
    - **learning from physical actions** := R can learn about the reward by observing H's behaviour and help reinforce/fulfil/support that behaviour
        - plus, humans can be pedagogic in how they do things: they do them in a more educational, albeit less precise/effective way;

# Limitations and Future Work

- active reward learning algos are more computationally efficient, can they be adapted to assistance problems?
- can we use deep reinforcement learning to solve assistance problems without separating learning and control?
- can we design larger, more realistic environments to help research?
