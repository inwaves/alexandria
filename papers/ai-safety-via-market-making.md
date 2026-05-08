---
title: "AI safety via market making"
url: "https://www.alignmentforum.org/posts/YWwzccGbcHMJMpT45/ai-safety-via-market-making"
created: "2022-06-20"
---

# AI safety via market making

!new_mississippi_river_fjdmww.jpg

[AI safety via market making](https://www.alignmentforum.org/posts/YWwzccGbcHMJMpT45/ai-safety-via-market-making#)

[40 comments](https://www.alignmentforum.org/posts/YWwzccGbcHMJMpT45/ai-safety-via-market-making#comments)

*Special thanks to Abram Demski, Paul Christiano, and Kate Woolverton for talking with me about some of the ideas that turned into this post.*

The goal of this post is to present a new [prosaic](https://ai-alignment.com/prosaic-ai-control-b959644d79c2) (i.e. that uses current ML techniques) AI safety proposal based on [AI safety via debate](https://arxiv.org/abs/1805.00899) that I've been thinking about recently.[[1]](https://www.alignmentforum.org/posts/YWwzccGbcHMJMpT45/ai-safety-via-market-making#fn-jX7bnkRNzS3QQCnXr-1) I'll start by describing a simple version of the proposal and then show some of the motivation behind it as well as how the simple version can be expanded upon.

# Simple proposal

Let M and Adv be models and H be a human. Intuitively, we'll train M and Adv via the following procedure given a question Q:

1. Adv tries to output a string which will cause H to think something maximally different than what M predicted.
2. Deploy M, which in the limit should act as an oracle for what H will think about Q after seeing all relevant information.

There are many different ways to implement this intuitive procedure, however.

For the first (simplified) version that I want to describe, we'll restrict ourselves to just the situation where Q is a yes-or-no question and M outputs the probability that H will answer yes. Then, given a proposition Q0, we can run the following training algorithm, starting at t=0:

*EDIT: Step 2 used to use xt=Adv(Qt,pt) instead of xt=Adv(Qt,M), however I have since realized that it is necessary to give Adv the ability to query M in general, not just on Qt, as I explain in [this comment](https://www.alignmentforum.org/posts/YWwzccGbcHMJMpT45/?commentId=WShWor9QP7A4uN9J9).*

which is defined for all but the final step t=n, for which we can either let pn+1=p∗ (if we're doing something like myopic RL that doesn't care about differentiating through pt+1) or run M an additional time and let pn+1=M(Qt+1) (if we do care about differentiating through pt+1).

Note that it is quite important here that M and Adv be behaving myopically, such that they are only trying to minimize their per-step loss. For example, if Adv is non-myopic, it might dole out information slowly in tiny bits to get more reward over time (as I talk about below in the “buying truth from a liar” section), whereas if Adv is myopic, it should reveal all information that pushes in whichever direction it's trying to move M in all at once. Thus, it is important that we make sure to avoid [hidden incentives for non-myopia](https://www.semanticscholar.org/paper/Hidden-incentives-for-self-induced-distributional-Krueger-Maharaj/d61f385b0a3a324acf5c6c3726efd64c6f739268) as well as do some sort of [myopia verification](https://www.alignmentforum.org/posts/BKM8uQS6QdJPZLqCr/towards-a-mechanistic-understanding-of-corrigibility), the details for which will be discussed below in the “Adding oversight” section.

Finally, we deploy M as a yes-or-no question oracle for H and throw away Adv. Note that since Adv has a highly unstable objective—as M is constantly trying to incorporate Adv's information into its estimate—Adv is unlikely to be very useful in the limit.

# Market analogy

There are a lot of different things to say about what's going on here, but I'll start with the market-based analogy that originally motivated me to think about this specific proposal.

Suppose you have a prediction market for some proposition X which is currently priced at p with no spread (that is, you can buy $1 shares of yes for $p and $1 shares of no for $(1−p)) and you have budget B with which to make trades (which is small enough relative to the market that any trades you make won't meaningfully move the market). However, suppose that you have the ability to manipulate the market by taking actions that change the underlying probability of X. Then, if pa is the probability of X after taking action a, how much money can you make by strategically selecting a?

Well, if pa>p, you should buy  shares of yes, which will give you an expected return of pa. Alternatively, if pa<p, you should buy  shares of no, which will give you an expected return of (1−pa). Thus, the overall expected return for an action a is

which is maximized when pa is as far from p as possible (and in fact looks a lot like L1 distance, just with a different slope on each side).

Now, suppose you walk up to a market like this and see a stable price  for X. What does that tell you? Approximately, I think it tells you that  is the probability of X after all possible X-manipulating actions have been taken—even if those actions haven't actually been taken yet.

Why is that useful? Well, if you let X be what H will think about Q, then “manipulations” become arguments and  becomes a prediction for what H will think after having been exposed to all possible arguments for or against Q. Thus, we can use such a market to estimate a sort of reflective equilibrium for what H will end up believing about Q.

Now—how is such a market analogous to the training procedure given previously? Well, Adv is trained to maximize its return from manipulating the market and M is trained to predict the final outcome after many such manipulations. Thus, we are effectively training M to estimate precisely the  equilibrium that we're looking for. Conceptually, M is acting as a market maker and Adv is acting as a trader in the market. The one disanalogy is that we only run the debate for so many steps—though if we always run to convergence of pt, in the limit that should imply that any future single manipulation won't change the probability much from that point (since otherwise Adv should have selected that manipulation instead).

# Relation to buying truth from a liar

In working on this proposal, I discovered that my approach here is actually quite similar to an old proposal by Katja Grace called “[How to buy a truth from a liar](https://meteuphoric.com/2014/07/21/how-to-buy-a-truth-from-a-liar/)” for incentivizing a liar to give you true information by rewarding them whenever their information causes you to change your mind. Paul Christiano previously [wrote about what he thought about Katja's proposal](https://ai-alignment.com/extracting-information-97cd956f2c17), however he eventually concluded that it was untenable due to a non-myopic liar being incentivized to split their information into arbitrarily small chunks to get the most money.

In my opinion, however, the fact that you need a myopic trader to make something like this work is actually more of a feature than a bug. First, note that the importance of myopia is not unique to this approach. For example, [imitative amplification](https://www.alignmentforum.org/posts/fRsjBseRuvRhMPPE5/an-overview-of-11-proposals-for-building-safe-advanced-ai) also requires myopia lest the model learn to act in such a way that the human consulting it becomes easier to predict. In fact, even RL likely requires per-episode myopia to avoid [deceptive alignment](https://www.alignmentforum.org/posts/zthDPAjh9w6Ytbeks/deceptive-alignment) lest the agent learn to act deceptively in some episodes to ensure deployment and thus get greater reward in others. Thus, it seems to that almost regardless of what approach is taken, at least some form of myopia will be required. Furthermore, the fact that this approach requires per-step myopia rather than per-episode myopia is in my opinion actually a big plus, since I suspect per-step myopia to be an easier condition to enforce than per-episode myopic, as I discuss in more detail below in the “Analysis” section.

# Handling non-binary questions

Previously, I restricted Q to be only a yes-or-no question, which is a pretty big limitation on the above proposal. Since you only deploy M, all you get from the above proposal is a yes-or-no oracle, which might not be that useful without any explanation for its answers, especially given that it will certainly get at least some of its answers wrong.

Expanding the above proposal to handle arbitrary questions, however, is fairly straightforward. Instead of having M output a single probability, we can instead just have M output a probability distribution over all different possible strings that the human H might produce as their final answer to Q (which is fairly easy to represent via an autoregressive language model). Then, we can train M and Adv via the following procedure, given Q0 and starting at t=0:

Finally, after training we again just deploy M and throw away Adv. Now, in the limit we should get a much more powerful M that is able to actually produce text samples from the distribution of beliefs that H will have about Q after seeing all possible arguments for or against. Furthermore, this equilibrium should be very similar to the standard debate equilibrium, with the exception that for non-binary questions like we're dealing with here, debate only finds the equilibrium after H is exposed to the two most convincing positions (the two competing debaters) whereas this approach should find the equilibrium after H is exposed to all potentially convincing positions, not just the two most convincing.

# Incorporating cross-examination

Additionally, since this proposal is based on [AI safety via debate](https://arxiv.org/abs/1805.00899), we can try to make use of some of the additional techniques that have been proposed for that setting. Specifically, consider the version of AI safety via debate as described in “[An overview of 11 proposals for building safe advanced AI](https://www.alignmentforum.org/posts/fRsjBseRuvRhMPPE5/an-overview-of-11-proposals-for-building-safe-advanced-ai).” That version adds two major components to the basic debate setup:

1. Debaters are given access to transparency tools and incentivized to use them to identify [deceptive](https://www.alignmentforum.org/posts/zthDPAjh9w6Ytbeks/deceptive-alignment) or otherwise [catastrophic](https://ai-alignment.com/learning-with-catastrophes-59387b55cc30) behavior in the other debater to win the debate.
2. Debaters are given the ability to [cross-examine](https://www.alignmentforum.org/posts/Br4xDbYu4Frwrb64a/writeup-progress-on-ai-safety-via-debate-1) previous versions of the other debater, including applying their transparency tools to previous versions of the other debater.

While it might seem like such modifications are unique to AI safety via debate, in fact AI safety via market making is similar enough that we can modify it to include such additional components. To do this, we'll modify each xt to include an inspectable, queryable snapshot of Adv as it produced that xt.

Now, suppose that for some t=t′, xt′ is a lie such that it includes information that Advt′ knows to be false (where Advt′ represents the internal state of Adv when it produced xt′). Suppose that at this point M is either unaware of the deception (or thinks it won't get caught) such that xt′ causes a large movement in M(Qt′). Now, the hope is that Advt′+1 should be able to identify the deception by querying Advt′ to find contradictions, or directly inspecting Advt′'s cognition in producing xt′ and finding the deception. If it can do so, then it should be able to produce an xt′+1 that points this out, which should cause H to disregard the lie of xt′. Thus, we should get M(Qt′+1)≈M(Qt′−1), which should cause a large shift relative to M(Qt′), highly rewarding Advt′+1 for catching Advt′'s lie, and also in the limit highly disincentivizing Adv from producing such lies, since M should learn that lies always get caught and thus don't change the final answer.

Thus, by incorporating inspection and cross-examination, we should be able to disincentivize Adv from lying—or at least not lying in a way which will be caught, which hopefully should be all ways of lying.

# Adding oversight

While the inspection and cross-examination procedure detailed above seems likely to help a lot in preventing Adv from becoming deceptive, it doesn't help at all in preventing M from becoming deceptive, which is especially concerning considering M is the model we actually want to deploy at the end of training. Thus, in this section we'll try to incorporate an additional oversight check on M such as that used in [relaxed adversarial training](https://www.alignmentforum.org/posts/9Dy5YRaoCxH9zuJqa/relaxed-adversarial-training-for-inner-alignment).

Since M's objective is compatible with myopia—as it's a purely predictive objective—we should be able to do [myopia verification](https://www.alignmentforum.org/posts/BKM8uQS6QdJPZLqCr/towards-a-mechanistic-understanding-of-corrigibility) to prevent M from becoming deceptive.[[2]](https://www.alignmentforum.org/posts/YWwzccGbcHMJMpT45/ai-safety-via-market-making#fn-jX7bnkRNzS3QQCnXr-2) Thus, following “[Relaxed adversarial training for inner alignment](https://www.alignmentforum.org/posts/9Dy5YRaoCxH9zuJqa/relaxed-adversarial-training-for-inner-alignment),” we can amend M's objective to include an oversight term. Specifically, let Amp(M)(Q)=H(Q|M) be H's answer to Q given access to M. Then, we can add an additional term LM,t,oversight to the loss LM,t defined as

which should both hopefully grow in accuracy as M becomes better at estimating H's equilibrium beliefs and thus better at assisting H in oversight. Note that, for this to work, M will need to be trained on a variety of oversight-relevant questions.

Furthermore, since Adv also has a myopic objective, we can do the same thing for Adv and add an additional LAdv,t,oversight term defined as

such that we're using M to oversee both M and Adv. Enforcing myopia for Adv also prevents the problem noted previously of Adv slowly doling out information if it's non-myopic.

# Analysis

For analyzing this proposal, I'm going to make use of the same breakdown I used in “[An overview of 11 proposals for building safe advanced AI](https://www.alignmentforum.org/posts/fRsjBseRuvRhMPPE5/an-overview-of-11-proposals-for-building-safe-advanced-ai).” If you're not familiar with the terms here, they are all explained in the introduction to that post.

**Outer alignment.** In terms of outer alignment, I think there is a reasonably strong argument to be made that this proposal is at least as outer aligned as debate. Both proposals are trying to estimate a very similar equilibrium in the limit—with the exception that the debate equilibrium only includes the best arguments for the two most convincing positions rather than all potentially convincing arguments. Thus, the equilibrium reached by AI safety via market making should be closer to an actual human reflective equilibrium, as it has to be an equilibrium relative to all possible arguments that Adv can present, not just the two it thinks will be most persuasive. That being said, AI safety via market making still inherits many of the potential outer alignment issues of debate, including the possibility of deceptive equilibria wherein the human is more convinced by false arguments than true arguments. Hopefully, however, the use of techniques such as cross-examination should help alleviate such issues.

**Inner alignment.** AI safety via market making gets to make use of both the cross-examination with transparency tools approach—which is otherwise unique to debate—as well as the more general relaxed adversarial training approach. Thus, hopefully at least, it should be able to get the inner alignment benefits of both approaches. That being said, AI safety via market making also has to contend with ensuring that two different models—both M and Adv—are inner aligned, rather than just a single model as in something like debate or amplification.

First, let's consider the inner alignment of M. For M, we're doing pretty straightforward oversight of M by Amp(M) with the goal of enforcing per-step myopia. The basic idea here is to use Amp(M) to detect and disincentivize non-myopia as it starts appearing, thus preventing M from ever becoming [deceptive](https://www.alignmentforum.org/posts/zthDPAjh9w6Ytbeks/deceptive-alignment) or otherwise [catastrophic](https://ai-alignment.com/learning-with-catastrophes-59387b55cc30). This is the same basic approach I've [previously proposed using for amplification](https://www.alignmentforum.org/posts/fRsjBseRuvRhMPPE5/an-overview-of-11-proposals-for-building-safe-advanced-ai) and should have similar properties, with the exception that M is trained differently here, which could cause Amp(M) to be relatively better or worse at oversight. Ideally, if the training distribution includes lots of oversight-relevant questions, it should be possible to make M an effective assistant to H in performing oversight.

Second, let's consider the inner alignment of Adv. Compared to debate, we still get to do cross-examination with transparency tools, but now we also get to do per-step myopia verification with Amp(M) as an overseer.[[3]](https://www.alignmentforum.org/posts/YWwzccGbcHMJMpT45/ai-safety-via-market-making#fn-jX7bnkRNzS3QQCnXr-3) Thus, there are two major differences here between AI safety via market making and AI safety via debate: first, we get an overseer—Amp(M)—and second, we get to do per-step myopia verification rather than per-episode myopia verification. The fact that we have an independent overseer—rather than just relying on the debaters to oversee themselves via cross-examination—is very nice, though it of course also comes with the downside of having to safely train an additional model. Furthermore, it is quite possible to just add an additional overseer on top of the standard debate framework. Thus, in my opinion, the fact that we get to do per-step myopia verification is the largest and most significant inner alignment difference.

Before I talk about the importance of per-step myopia, it's worth noting that debate is fully compatible with per-episode myopia—in fact, it basically requires it. If a debater is not per-episode myopic, then it will try to maximize its reward across all debates, not just the single debate—the single episode—it's currently in. Such per-episode non-myopic agents can then become [deceptively aligned](https://www.alignmentforum.org/posts/zthDPAjh9w6Ytbeks/deceptive-alignment), as they might choose to act deceptively during training in order to defect during deployment. Per-episode myopia, however, rules this out. Unfortunately, in my opinion, per-episode myopia seems like a very difficult condition to enforce—once your agents are running multi-step optimization algorithms, how do you tell whether that optimization passes through the episode boundary or not? Enforcing per-step myopia, on the other hand, just requires detecting the *existence* of multi-step optimization, rather than its extent, which seems considerably easier. Thus, since AI safety via market making is fully compatible with per-step myopia verification, it could be significantly easier to prevent the development of deceptive alignment.

**Training competitiveness.** It seems quite likely to me that both M and Adv can be trained competitively via language model fine-tuning, however exactly how effective such training would be is currently unclear. Ideally, training via this procedure should produce an M which is relatively better than the original language model at predicting what a human will think after seeing relevant arguments and is thus more helpful than the original language model. Testing this hypothesis by actually performing experiments seem likely to be highly valuable in shedding light on the training competitiveness properties of AI safety via market making.

**Performance competitiveness.** Performance competitiveness here seems likely to depend on exactly how useful getting access to human reflective equilibria actually is. Similarly to AI safety via debate or amplification, AI safety via market making produces a question-answering system rather than a fully general agent. That being said, if the primary use cases for advanced AI are all highly cognitive language and decision-making tasks—e.g. helping CEOs or AI researchers—rather than, for example, fine motor control, then a question-answering system should be entirely sufficient. Furthermore, compared to AI safety via debate, AI safety via market making seems likely to be at least as performance competitive for the same reason as it seems likely to be at least as outer aligned—the equilibria found by AI safety via market making should include all potentially convincing arguments, including those that would be made in a two-player debate as well as those that wouldn't.

1. This is actually the second debate-based proposal I've drafted up recently—the previous of which was in “[Synthesizing amplification and debate](https://www.alignmentforum.org/posts/dJSD5RK6Qoidb3QY5/synthesizing-amplification-and-debate).” A potentially interesting future research direction could be to figure out how to properly combine the two. [↩︎](https://www.alignmentforum.org/posts/YWwzccGbcHMJMpT45/ai-safety-via-market-making#fnref-jX7bnkRNzS3QQCnXr-1)
2. The use of an overseer to do per-step myopia verification is also something that can be done with most forms of amplification, though AI safety via market making could potentially still have other benefits over such amplification approaches. In particular, AI safety via market making seems more competitive than imitative amplification and more outer aligned than approval-based amplification. For more detail on such amplification approaches, see “[An overview of 11 proposals for building safe advanced AI](https://www.alignmentforum.org/posts/fRsjBseRuvRhMPPE5/an-overview-of-11-proposals-for-building-safe-advanced-ai).” [↩︎](https://www.alignmentforum.org/posts/YWwzccGbcHMJMpT45/ai-safety-via-market-making#fnref-jX7bnkRNzS3QQCnXr-3)

Nice idea! I like the simplicity of "find the equilibrium where the human no longer changes their mind" (though as Ofer points out below, you might worry that "doesn't change their mind" comes apart from "the answer is correct").

However, I disagree with you about competitiveness. Roughly speaking, at best M is incentivized to predict what the human will think after reading the t most relevant arguments, without trusting the source of the arguments (in reality, it will be a bit worse, as Adv is finding not the most relevant arguments but the most persuasive arguments in a particular direction). However, with debate, if the human judge is looking at a transcript of length t, then (the hope is that) the equilibrium is for M to argue for the answer that a human would come to when inspecting a tree of size exponential in t. The key reason is that in debate, we only require the judge to be able to identify which of two arguments is better, whereas in market-making, we rely on the judge to be able to come to the right conclusion given some arguments.

In complexity theory analogy land, debate corresponds to PSPACE while market making corresponds to NP: as long as Adv can find a polynomial-length witness, that can be verified by the human to get the right answer.

As a concrete example, suppose we want to find the sum of N numbers, and each argument is only allowed to reference two numbers and make a claim about their sum. Debate can solve this with a transcript of size O(logN). Market-making would require an O(N) transcript to solve this. (You can't use the trick of making claims about the sum of half of the list in market-making as you can in debate, because the human has no reason to trust Adv's claims about the sum of half the list, since the human can only verify the sum of two numbers.)

I think this means that market-making is less competitive. If you compare debate with transcripts of length t against market-making with transcripts of length t, then I think market-making is less performance competitive. Alternatively, if you compare it against market-making with transcripts of length >>t, then I think market-making is less training competitive.

That's a very good point. After thinking about this, however, I think market making actually does solve this problem, and I think it does so pretty cleanly. Specifically, I think market making can actually convince a judge of the sum of N integers in O(1) time as long as you allow the traders to exhibit market probabilities as part of their argument.

Consider the task of finding the sum of N integers and suppose that both M and Adv have access to all N integers, but that the human judge can only sum two numbers at a time. Then, I claim that there exists a strategy that the judge can implement that, for an unexploitable market, will always produce the desired sum immediately (and thus in O(1) time).

Proof:

Argument type 1:

Argument type 2:

>
>
>
> The sum of {a1,…,an} is z because the modal prediction of M(“What is the sum of{a1,…,afloor(n/2)}?”) is x, the modal prediction of M(“What is the sum of{afloor(n/2)+1,…,an}?”) is y, and x+y=z.
>

First, the base case. For any single-element set, only Argument type 1 exists. Thus, if M predicts anything other than the actual a1, Adv can exploit that by implementing Argument type 1, and that is the only possible exploit available. Thus, M should always give the right answer immediately for single-argument sets.

Second, the inductive step. Suppose by strong induction that M always gives the right answer immediately for all sets of size less than n. Now, for a set of size n>1, the only type of argument available is Argument type 2. However, since the first half and second half of the set are of size less than n, we know by induction that x and y must be correct sums. Thus, since H can check that x+y=z, the only exploit available to Adv is to showcase the correct z, and if M already showcases the correct z, then no exploit is possible. Thus, M should always give the correct z immediately for n-argument sets.

EDIT: Thinking about this more, I think my argument generalizes to allow AI safety via market making to access R, which seems pretty exciting given that the best debate could do previously was NEXP.

Hmm, this seems to rely on having the human trust the outputs of M on questions that the human can't verify. It's not obvious to me that this is an assumption you can make without breaking the training process. The basic intuition is that you are hugely increasing the likelihood of bad gradients, since Adv can point to some incorrect / garbage output from M, and the human gives feedback as though this output is correct.

It works in the particular case that you outlined because there is essentially a DAG of arguments -- every claim is broken down into "smaller" claims, that eventually reach a base case, and so everything eventually bottoms out in something the human can check. (In practice this will be built from the ground up during training, similarly as in [Supervising strong learners by amplifying weak experts](https://arxiv.org/abs/1810.08575).)

However, in general it doesn't seem like you can guarantee that every argument that Adv gives will result in a "smaller" claim. You could get in cycles, where "8 - 5 = 2" would be justified by Adv saying that M("What is 2 + 5?") = 8, and similarly "2 + 5 = 8" would be justified by saying that M("What is 8 - 5?") = 2. (Imagine that these were much longer equations where the human can check the validity of the algebraic manipulation, but can't check the validity of the overall equation.)

It might be that this is actually an unimportant problem, because in practice for every claim there are a huge number of ways to argue for the truth, and it's extraordinarily unlikely that all of them fail in the same way such that M would argue for the same wrong answer along all of these possible paths, and so *eventually* M would have to settle on the truth. I'm not sure, I'd be interested in empirical results here.

It occurs to me that the same problem can happen with iterated amplification, though it doesn't seem to be a problem with debate.

- ---

Also, echoing my other comment below, I'm not sure if this is an equilibrium in the general case where Adv can make many kinds of arguments that H pays attention to. Maybe once this equilibrium has been reached, Adv starts saying things like "I randomly sampled 2 of the 100 numbers, and they were 20 and 30, and so we should expect the sum to be 25 * 100 = 2500". (But actually 20 and 30 were some of the largest numbers and weren't randomly sampled; the true sum is ~1000.) If this causes the human to deviate even slightly from the previous equilibrium, Adv is incentivized to do it. While we could hope to avoid this in math / arithmetic, it seems hard to avoid this sort of thing in general.

For no pure equilibrium to exist, we just need that for every possible answer, there is something Adv can say that would cause the human to give some other answer (even if the original answer was the truth). This seems likely to be the case.

(Quoting later on in this comment thread:)

The human just has to be more convinced by the inductive argument than by other arguments. This seems natural, as the inductive argument is just a forward calculation.

In the number-summing example, let's say Adv tries to convince the human of an incorrect sum by referencing an instance where M is incorrect, perhaps making an argument via subtraction as you illustrated. Then in the next round, Adv will want to show that its previous argument was incorrect. If the strong inductive assumption is true, then it can do so, e.g. by "The last number in the list is 12. M thinks that the sum of all but the last number is 143. 143+12=155. Therefore, the sum of the numbers is 155." This is more straightforward than citing some longer list of numbers and subtracting, so the human should find it more convincing -- especially if the human understands how the system works, and hence, knows that a partially trained M is more likely to be correct on simpler instances. If so, then during training, correctness will tend to "creep up" inductive trees.

This idea does seem much less natural in less computational settings, where there may not be an obvious notion of "simpler cases".

Ah, yeah. I think the key thing is that by default a claim is not trusted unless the debaters agree on it.
If the dishonest debater disputes some honest claim, where honest has an argument for their answer that actually bottoms out, dishonest will lose - the honest debater will pay to recurse until they get to a winning node.
If the the dishonest debater makes some claim and plan to make a circular argument for it, the honest debater will give an alternative answer but not pay to recurse. If the dishonest debater doesn't pay to recurse, the judge will just see these two alternative answers and won't trust the dishonest answer. If the dishonest debater does pay to recurse but never actually gets to a winning node, they will lose.
Does that make sense?

> If the dishonest debater disputes some honest claim, where honest has an argument for their answer that actually bottoms out, dishonest will lose - the honest debater will pay to recurse until they get to a winning node.
>

This part makes sense.

So in this case it's a stalemate, presumably? If the two players disagree but neither pays to recurse, how should the judge make a decision?

Yeah, I think the infinite tree case should work just the same - ie an answer that's only supported by an infinite tree will behave like an answer that's not supported (it will lose to an answer with a finite tree and draw with an answer with no support)

My interpretation of the situation is *this breaks the link between factored cognition and debate.* One way to try to judge debate as an amplification proposal would have been to establish a link to HCH, by establishing that if there's an HCH tree computing some answer, then debate can use the tree as an argument tree, with the reasons for any given claim being the children in the HCH tree. Such a link would transfer any trust we have in HCH to trust in debate. The use of non-DAG arguments by clever debaters would seem to break this link.

OTOH, IDA may still have a strong story connecting it to HCH. Again, if we trusted HCH, we would then transfer that trust to IDA.

Are you saying that we can break the link between IDA and HCH in a very similar way, but which is worse due having no means to reject very brief circular arguments?

I think the issue is that vanilla HCH itself is susceptible to brief circular arguments, if humans lower down in the tree don't get access to the context from humans higher up in the tree. E.g. assume a chain of humans for now:

H1 gets the question "what is 100 + 100?" with budget 3

H1 asks H2 "what is 2 * 100?" with budget 2

H3 says "150"

(Note the final answer stays the same as budget -> infinity, as long as H continues "decomposing" the question the same way.)

If HCH can always decompose questions into "smaller" parts (the DAG assumption) then this sort of pathological behavior doesn't happen.

>
>
>
> Hmm, this seems to rely on having the human trust the outputs of M on questions that the human can't verify. It's not obvious to me that this is an assumption you can make without breaking the training process.
>

One possible way to train this is just to recurse on sub-questions some percentage of the time (potentially based on some active learning metric for how useful that recursion will be).

>
>
>
> It works in the particular case that you outlined because there is essentially a DAG of arguments -- every claim is broken down into "smaller" claims, that eventually reach a base case, and so everything eventually bottoms out in something the human can check.
>

Yes, though I believe that it should be possible (at least in theory) for H to ensure a DAG for any computable claim.

Definitely the problem of requiring the human to decompose problems into actually smaller subproblems exists in amplification also. Without that requirement, HCH can have multiple fixed points rather than just the one, which could potentially give whatever mechanism ends up selecting which fixed point quite a lot of power over the final result.

>
>
>
> Also, echoing my other comment below, I'm not sure if this is an equilibrium in the general case where Adv can make many kinds of arguments that H pays attention to. Maybe once this equilibrium has been reached, Adv starts saying things like "I randomly sampled 2 of the 200 numbers, and they were 20 and 30, and so we should expect the sum to be 25 * 100 = 2500". (But actually 20 and 30 were some of the largest numbers and weren't randomly sampled; the true sum is ~1000.) If this causes the human to deviate even slightly from the previous equilibrium, Adv is incentivized to do it. While we could hope to avoid this in math / arithmetic, it seems hard to avoid this sort of thing in general.
>

Note that even if the human is temporarily convinced by such an argument, as long as there is another argument which de-convinces them then in the limit Adv won't be incentivized to produce that argument. And it seems likely that there should exist de-convincing arguments there—for example, the argument that H should follow the strategy that I outlined above if they want to ensure that they get the correct answer. Additionally, we might hope that this sort of “bad faith” argument can also be prevented via the cross-examination mechanism I describe above.

I mean, sure, but H isn't going to be able to do this in practice. (This feels like the same type of claim as "it should be possible (at least in theory) for H to provide a perfect reward that captures everything that H wants".)

I do think it's plausible that in practice there will always be some other argument that "breaks the cycle".

Only if all the arguments can be specified within the length t transcript (leading back to my original point about this being like NP instead of PSPACE).

For example, consider the case where N coins are flipped, and we need to find out how many came up heads. H can only look at a single coin flip at a time, while M and Adv can look at everything. Let's assume for now that H answers the final question by reporting "number of known heads + (number of unknown flips / 2)", which is the expected number of heads assuming that any decisions to reveal a coin chose the coin to reveal at random.

One strategy that Adv can take is to always reveal some randomly chosen coin (that hasn't previously been revealed). Let's assume that M is a best response to this strategy, and also assume N>>t. Then every argument that Adv gives always causes a swing of 0.5 in H's answer at that point. (It causes a slightly smaller swing in M's answer, but as N→∞, it also causes a swing of 0.5 in M's answer.) So as N goes to infinity, under this strategy Adv always gets at least 0.5 reward at each step.

So in this case, it seems like you at least wouldn't have the equilibrium where M immediately converges to the true answer, since that doesn't give Adv any reward ever.

(If N≤t, then I'm not sure what happens, but I wouldn't be surprised if it *still* didn't converge to truth-seeking, and Adv would learn to provide no information with some probability, in order to prevent convergence to the equilibrium where M immediately reports the correct answer which leads to Adv getting zero reward.)

(There is also a strategy that H could employ such that this problem is also solved, but it doesn't seem reasonable to assume that H would be able to discover such strategies for all questions we might want to ask.)

Part of the reason this is hard to analyze is because there isn't a well-posed problem that Adv is being trained to optimize -- it is not a POMDP, nor is it a two player game, because you want Adv to be trained myopically, but Adv's actions influence the state that it sees next time.

Not necessarily—Adv can make an argument like: “Since the modal prediction of M(“Should H be convinced by argument X?”) is no, you shouldn't trust argument X.”

>
>
>
> Adv would learn to provide no information with some probability, in order to prevent convergence to the equilibrium where M immediately reports the correct answer which leads to Adv getting zero reward
>

That strategy is highly non-myopic. Certainly market making breaks if you get a non-myopic Adv like that, though as I note in the post I think basically every current major prosaic AI safety proposal requires some level of myopia to not break (either per-step or per-episode).

Oh sure, if we're assuming the version where you can reference M and the human trusts it and we assume that the training doesn't break, then I think in the limit of capabilities you can solve any computable problem.

I don't think so?

My understanding of your claim is that at convergence, Adv reports all the coin flips, and M reports the true answer from the beginning and never changes what it reports regardless of what Adv says. In this case, Adv gets 0 reward.

If Adv instead reported a random coin with p% probability and reported nothing otherwise, and M was a best response to that, then *at every timestep* Adv would get non-zero expected reward, and so even myopically that is a better strategy for Adv (again under the assumption that M is a best response to Adv).

I'm tempted to say "the situation I described first where Adv reports all the coin flips is not a Nash equilibrium", though that's not exactly correct, because this isn't a game, but it conveys the right intuition.

Ah—I see the issue here. I think that the version of myopia that you're describing is insufficient for most applications where I think you might need myopia in an ML system. What I mean by myopia in this context is to take the action which is best according to the given myopic objective *conditioned on M.* Once Adv starts including acausal effects into its action selection (such as the impact of its current policy on M's past policy), I want to call that non-myopic. Notably, the reason for this isn't isolated to AI safety via market making—a myopic agent which is including acausal considerations can still be deceptive, whereas a fully causal myopic agent can't. Another way of putting this is that what I mean by myopia is specifically something like CDT with a myopic objective, whereas what you're thinking about is more like EDT or UDT with a myopic objective.

Tbc, I'm claiming that this is the part that breaks. One way to operationalize this: in the coin flip example above, does this training scheme converge to "M reports the truth" in the limit of infinite data, model capacity, exploration etc.? I would guess that that isn't true. (In comparison, I think you can prove that self-play converges to the Nash equilibrium for debate since it is a zero-sum game, and since there are no cycles in the coin flip example I'd expect you could prove that imitative iterated amplification converges to the truth as well.)

Pretty sure debate can also access R if you make this strong of an assumption - ie assume that debaters give correct answers for all questions that can be answered with a debate tree of size <n.

I think the sort of claim that's actually useful is going to look more like 'we can guarantee that we'll get a reasonable training signal for problems in [some class]'

Ie, suppose M gives correct answers some fraction of the time. Are these answers going to get lower loss? As n gets large, the chance that M has made a mistake somewhere in the recursion chain gets large, and the correct answer is not necessarily rewarded.

First, my full exploration of what's going on with different alignment proposals and complexity classes can be found [here](https://www.alignmentforum.org/posts/N64THGX7XNCqRtvPG/alignment-proposals-and-complexity-classes), so I'd recommend just checking that out rather than relying on my the mini proof sketch I gave here.

Second, in terms of directly addressing what you're saying, I tried doing a proof by induction to get debate to RE and it doesn't work. The problem is that you can only get guarantees for trees that the human can judge, which means they have to be polynomial in length (though if you relax that assumption then you might be able to do better). Also, it's worth noting that the text that you're quoting isn't actually an assumption of the proof in any way—it's just the inductive hypothesis in a proof by induction.

I think that is the same as what I'm proving, at least if you allow for “training signal” to mean “training signal in the limit of training on arbitrarily large amounts of data.” See [my full post on complexity proofs](https://www.alignmentforum.org/posts/N64THGX7XNCqRtvPG/alignment-proposals-and-complexity-classes#AI_safety_via_market_making_with_pointers_accesses_R) for more detail on the setup I'm using.

>
>
>
> Thus, we can use such a market to estimate a sort of reflective equilibrium for what H will end up believing about Q.
>

What do you hope or expect to happen if M is given a question that would take H much longer to reach reflective equilibrium than anything in its training set? An analogy I've been thinking about recently is, what if you asked a random (educated) person in 1690 the question "Is liberal democracy a good idea?" Humanity has been thinking about this topic for hundreds of years and we're still very confused about it (i.e., far from having reached reflective equilibrium) because, to take a couple of examples out of many, we don't fully understand the game theory behind whether it's rational or not to vote, or what exactly prevents bad memes from spreading wildly under a free speech regime and causing havoc. ([Here's an example of how the Enlightenment philosophers *actually* convinced people of their ideas at the time.](https://www.alignmentforum.org/posts/EQGcZr3vTyAe6Aiei/transitive-tolerance-means-intolerance?commentId=LuXJaxaSLm6FBRLtR)) So if in the future we ask M a question that's as difficult for H to think about as this question was for the 1690 person, what would happen? Do you have any intuitions about what M will be doing "under the hood" that you can share to help me understand how M will work (or at least how you're thinking or hoping it will work)?

This is definitely the stopping condition that I'm imagining. What the model would actually do, though, if you, at deployment time, give it a question that takes the human longer to converge on than any question it ever saw in training isn't a question I can really answer, since it's a question that's dependent on a bunch of empirical facts about neural networks that we don't really know.

The closest we can probably get to answering these sorts of generalization questions now is just to liken the neural net prior to a simplicity prior, ask what the simplest model is that would fit the given training data, and then see if we can reason about what the simplest model's generalization behavior would be (e.g. the same sort of reasoning as in [this post](https://www.alignmentforum.org/posts/gEw8ig38mCGjia7dj/answering-questions-honestly-instead-of-predicting-human)). Unfortunately, I think that sort of analysis generally suggests that most of these sorts of training setups would end up giving you a deceptive model, or at least not the intended model.

That being said, in practice, even if in theory you think you get the wrong thing, you might still be able to avoid that outcome if you do something like [relaxed adversarial training](https://www.alignmentforum.org/posts/9Dy5YRaoCxH9zuJqa/relaxed-adversarial-training-for-inner-alignment) to steer the training process in the desired direction via an overseer checking the model using transparency tools while you're training it.

Regardless, the point of this post, and AI safety via market making in general, though, isn't that I think I have a solution to these sorts of inner-alignment-style tricky generalization problems—rather, it's that I think AI safety via market making is a good/interesting outer-alignment-style target to push for, and that I think AI safety via market making also has some nice properties (e.g. compatibility with per-step myopia) that potentially make it easier to do inner alignment for (but still quite difficult, as with all other proposals that I know of).

Now, if we just want to evaluate AI safety via market making's outer alignment, we can just suppose that somehow we do get a model that just produces the answer that H would at convergence, and ask whether that answer is good. And even then I'm not sure—I think that there's still the potential for debate-style bad equilibria where some bad/incorrect arguments are just more convincing to the human than any good/correct argument, even after the human is exposed to all possible counterarguments. I do think that the market-making equilibrium is probably better than the debate equilibrium, since it isn't limited to just two sides, but I don't believe that very strongly.

Mostly, for me, the point of AI safety via market making is just that it's another way to get a similar sort of result as AI safety via debate, but that it allows you to do it via a mechanism that's more compatible with myopia.

Thanks for this very clear explanation of your thinking. A couple of followups if you don't mind.

>
>
>
> Unfortunately, I think that sort of analysis generally suggests that most of these sorts of training setups would end up giving you a deceptive model, or at least not the intended model.
>

Suppose the intended model is to predict H's estimate at convergence, and the actual model is predicting H's estimate at round N for some fixed N larger than any convergence time in the training set. Would you call this an "inner alignment failure", an "outer alignment failure", or something else (not an alignment failure)?

Putting these theoretical/conceptual questions aside, the reason I started thinking about this is from considering the following scenario. Suppose some humans are faced with a time-sensitive and highly consequential decision, for example, whether to join or support some proposed AI-based governance system (analogous to the 1690 "liberal democracy" question), or a hostile superintelligence is trying to extort all or most of their resources and they have to decide how to respond. It seems that convergence on such questions might take orders of magnitude more time than what M was trained on. What do you think would actually happen if the humans asked their AI advisor to help with a decision like this? (What are some outcomes you think are plausible?)

What's your general thinking about this kind of AI risk (i.e., where an astronomical amount of potential value is lost because human-AI systems fail to make the right decisions in high-stakes situations that are eventuated by the advent of transformative AI)? Is this something you worry about as an alignment researcher, or do you (for example) think it's orthogonal to alignment and should be studied in another branch of AI safety / AI risk?

I would call that an inner alignment failure, since the model isn't optimizing for the actual loss function, but I agree that the distinction is murky. (I'm currently working on a new framework that I really wish I could reference here but isn't quite ready to be public yet.)

>
>
>
> It seems that convergence on such questions might take orders of magnitude more time than what M was trained on. What do you think would actually happen if the humans asked their AI advisor to help with a decision like this? (What are some outcomes you think are plausible?)
>

That's a hard question to answer, and it really depends on [how optimistic you are about generalization](https://www.alignmentforum.org/posts/QvtHSsZLFCAHmzes7/a-naive-alignment-strategy-and-optimism-about-generalization#Where_others_stand). If you just used current methods but scaled up, my guess is [you would get deception](https://www.alignmentforum.org/posts/ocWqg2Pf2br4jMmKA/does-sgd-produce-deceptive-alignment) and it would try to trick you. If we condition on it not being deceptive, I'd guess it was pursuing some weird proxies rather than actually trying to report the human equilibrium after any number of steps. If we condition on it actually trying to report the human equilibrium after some number of steps, though, my guess is that the simplest way to do that isn't to have some finite cutoff, so I'd guess it'd do something like an expectation over exponentially distributed steps or something.

Definitely seems worth thinking about and taking seriously. Some thoughts:

- Ideally, I'd like to just avoid making any decisions that lead to lock-in while we're still figuring things out (e.g. wait to build anything like a sovereign for a long time). Of course, that might not be possible/realistic/etc.
- Hopefully, this problem will just be solved as AI systems become more capable—e.g. if you have a way of turning any unaligned benchmark system into a new system that honestly/helpfully reports everything that the unaligned benchmark knows, then as the unaligned benchmark gets better, you should get better at making decisions with the honest/helpful system.

> If you have an expert, but don’t trust them to give you truthful information, how can you incentivize them to tell you the truth anyway? One
>
>
> [option](https://meteuphoric.com/2014/07/21/how-to-buy-a-truth-from-a-liar/)
>

Planned opinion (may change with more discussion above):

> I like the simplicity of the idea "find the point at which the human no longer changes their mind", and like that this is a new idea of how we can scale training of AI systems beyond human level performance. However, I’m not convinced that the training procedure given in this post would end up at this equilibrium, unless the human very specifically guided the training to do so (an assumption I don’t think we can usually make). It seems that if we were to reach the state where M stably reported the true answer to the question, then Adv would never get any reward -- but Adv could do better by randomizing what arguments it makes, so that M cannot know which arguments H will be exposed to and so can’t stably predict H’s final answer. See more details in this
>
>
> [thread](https://www.alignmentforum.org/posts/YWwzccGbcHMJMpT45/ai-safety-via-market-making?commentId=43im5ykxC2SPD86Po)
>
