---
title: "Measuring Progress on Scalable Oversight for Large Language Models"
url: "https://arxiv.org/abs/2211.03540"
created: "2023-06-19"
---

# Measuring Progress on Scalable Oversight for Large Language Models

Good paper overall, it seems like an experiment that we should’ve done by now that is now done.

What they did: show that sandwiching is possible

- “sandwiching” technique: a model outperforms naive humans, but is outperformed by the human + model pair; experts are still better than human + model, so they can evaluate how “aligned” the pair is
    - two relaxations: no experts, just ground truth labels on MMLU and QuALITY; models are only prompted, not fine-tuned or any similar technique
- found that yeah, this holds: human-model pairs are better than the models or the humans in isolation
- why is this relevant?
    - well, for scalable oversight, we’ll want to extract useful, actionable information from an untrustworthy model
        - to some extent, this is what’s happening here, although they do mention that sometimes the model leads the person astray
- limitations
    - questions are about things we know — scalable oversight most important when we don’t know the answers
- interesting tidbits
    - kadavath et al 2022: pretrained models better calibrated on multiple-choice questions than RLHF’d models
