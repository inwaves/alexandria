---
title: "Synthesizing amplification and debate"
url: "https://www.alignmentforum.org/posts/dJSD5RK6Qoidb3QY5/synthesizing-amplification-and-debate"
created: "2022-06-20"
---

# Synthesizing amplification and debate

!new_mississippi_river_fjdmww.jpg

# Background

One possible way to train an amplification model is to use an auxiliary reinforcement learning objective to help guide the training of the amplification model. This could be done either by training two separate models, an agent and a question-answerer, or a single model trained on a joint objective. For example, from [a comment Paul left](https://www.alignmentforum.org/posts/jYdAxH8BarPT4fqnb/a-dilemma-for-prosaic-ai-alignment#K8fRPa9NWZXdARLYN) on “[A dilemma for prosaic AI alignment](https://www.alignmentforum.org/posts/jYdAxH8BarPT4fqnb/a-dilemma-for-prosaic-ai-alignment):”

>
>
>
> I normally imagine using joint training in these cases, rather than pre-training + fine-tuning. e.g., at every point in time we maintain an agent and a question-answerer, where the question-answerer "knows everything the agent knows." They get better together, with each gradient update affecting both of them, rather than first training a good agent and then adding a good question-answerer.
>

>
>
>
> (Independently of concerns about mesa-optimization, I think the fine-tuning approach would have trouble because you couldn't use statistical regularities from the "main" objective to inform your answers to questions, and therefore your question answers will be dumber than the policy and so you couldn't get a good reward function or specification of catastrophically bad behavior.)
>

In my last post, [I expressed skepticism of such non-imitative amplification approaches](https://www.alignmentforum.org/posts/33EKjmAdKFn3pbKPJ/outer-alignment-and-imitative-amplification), though in this post I want to propose a possible way in which some of my concerns with this style of approach could addressed by integrating ideas from [AI safety via debate](https://openai.com/blog/debate/). I'll start by describing the basic idea in broad terms, then give a more careful, technical description of the sort of training procedure I have in mind.

# The proposal

The basic idea is as follows: debate naturally yields an RL objective, so if you want to add an auxiliary RL objective to amplification, why not use the RL objective from debate? Specifically, the idea is to conduct a debate not between copies of the model M, but between copies of the amplified model Amp(M) (where Amp(M) is a human with access to the model M). That gives you both an RL reward arising from the winner of the debate as well as a supervised loss from the difference between the model's output and the amplified model's output. That's the basic proposal—now I'll try to give a more careful, technical description of how I think it should go.

## Definitions

We will start with some initial definitions.

## Training procedure

Then, consider the following training procedure.

1. Conduct a debate according to the following procedure while building up a history S and starting at t=0.
    1. Append to the history S the contents of argt as well as a trace of what happened in calculating argt, including all the necessary information to use transparency tools to inspect what happened.
2. Train M on the combination of the debate-style RL reward derived from winner (r=1 for the winner and r=−1 for the loser), a [relaxed adversarial training catastrophe-minimization penalty](https://www.alignmentforum.org/posts/9Dy5YRaoCxH9zuJqa/relaxed-adversarial-training-for-inner-alignment) calculated by Amp≈(H,Mtarget), and the supervised loss where d is some natural language distance metric and “”A represents the question posed to the function that computed the answer A.

Ways of combining the RL and supervised losses here include:

# Analysis

The first thing which I want to note about this procedure is that it gives a continuous relaxation between amplification and debate—in fact, there are multiple ways to tune the procedure to limit to either pure amplification or pure debate. First, you can anneal whatever combination of the different losses you are using to eventually become exclusively imitative amplification, exclusively debate, or anything else in between. Second, the fact that this procedure uses Amp(M) to determine whether or not to stop the debate after every argument gives another way in which this procedure gives you a relaxation between amplification and debate: if the debate is always stopped after the first argument, you just get pure imitative amplification, whereas as the debate goes on for longer, you get closer and closer to just pure debate. What's really nice about this is that it means that when pure imitative amplification is giving good results, you'll just get pure amplification—since then continue0 will tend to be false—but when amplification isn't working, you'll get debate—since then continue0 will tend to be true.

As a result, it should be quite possible to enforce that this procedure limit to [HCH](https://ai-alignment.com/strong-hch-bedb0dc08d4e)—either by annealing the losses or by forcing continue0 to tend towards false. Thus, I think this procedure has a good chance of being [outer aligned at optimum](https://www.alignmentforum.org/posts/33EKjmAdKFn3pbKPJ/outer-alignment-and-imitative-amplification)—or at least, a similar chance at it compared to pure imitative amplification. Unlike pure imitative amplification, however, this procedure gets to make use of the capability benefits of having an auxiliary RL objective to help guide training. Furthermore, since the auxiliary RL objective that we're using comes from debate, we get a lot of the benefits of debate as well, including the ability to incentivize the debaters to produce arguments that we wouldn't have necessarily though of ourselves, as well as the ability to train our debaters to use transparency tools against each other to help catch [deception](https://www.alignmentforum.org/posts/zthDPAjh9w6Ytbeks/deceptive-alignment) or other catastrophic behavior. That being said, I do think that whether or not something like this is [inner aligned](https://www.alignmentforum.org/s/r9tYkB2a8Fp4DN8yB/p/FkgsxrGf3QxhfLWHG) is still quite questionable—and is likely to [depend highly on the specific transparency tools you have access to](https://www.alignmentforum.org/posts/9Dy5YRaoCxH9zuJqa/relaxed-adversarial-training-for-inner-alignment)—though I do like the approach described here in general and I think it's definitely worth looking into more.
