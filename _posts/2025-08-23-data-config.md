---
title: "Optimizing the Dataset for the Privacy Evaluation of Speaker Anonymizers"
date: 2025-08-23
layout: post
---

This study investigates how the configuration of the Librispeech data used to evaluate anonymizers affects the reliability of the results, as well as its runtime.

## Links

- [GitHub repository](https://github.com/carlosfranzreb/spane) - the results can be found as [a release](https://github.com/carlosfranzreb/spane/releases/tag/paper_results)
- [Paper](#) (will be uploaded soon)

## Insights

The **evaluation's reliability** is determined by the evaluation dataset.
Our results suggest that using 20 enrollment utterances per speaker is enough to characterize them; using more does not improve the attack further.
Contrary to prior experiments, our results suggest that adding more speakers to the evaluation does not make it more challenging.
The similarity among speakers is more important than the amount
Experiments with other datasets should shed more light on this topic.

Regarding the **evaluation runtime**, we look at different strategies for reducing the size of the training data.
Anonymizing the training data and training the speaker recognizer with it takes up most of the evaluation runtime.
According to our results, 20% of the training data can be removed with a max. EER increase of 1.4%
Even more can be removed for development efforts
