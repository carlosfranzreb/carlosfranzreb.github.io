---
title: "Content Leakage in Librispeech"
date: 2026-03-10
layout: post
---

This study shows that Librispeech is not well suited for evaluating privacy, as the distinct audiobooks read by the speakers give away their identities.

## Links

- [GitHub repository](https://github.com/carlosfranzreb/spane) - the results can be found as [a release](https://github.com/carlosfranzreb/spane/releases/tag/paper_results_3)
- [Paper](https://arxiv.org/abs/2601.13107) (accepted to ICASSP 2026)

## Evaluation with phone durations

For this study I implemented the evaluation of [Tomashenko et al.](https://www.isca-archive.org/interspeech_2025/tomashenko25_interspeech.pdf), which replaces the mel-spectrogram with a 2D representation of the phones and their durations. Each vector is a one-hot embedding defining the phone, and the "1" of the embedding may be replaced with the phone's duration.
In their study, they experiment with more evaluation data, combining several utterances, to characterize the durations more reliably.
They also use the transcripts to obtain phonetic alignment, to prevent transcription errors from degrading the attack's performance.

In our work, we want to compare the two privacy evaluations, and therefore assume a more realistic scenario: the training and evaluation data are the same as in the original evaluation with mel-spectrograms, and the phonetic transcript is predicted with a phone recognizer instead of obtained from the ground truth.
We use the phone recognizer from [private kNN-VC](https://carlosfranzreb.github.io/private-knnvc) for predicting the phones based on WavLM vectors, which gives us a phone label for each 20ms of audio.
This leads to a weaker attack, naturally, but still strong enough to show that Librispeech indeed leaks identity solely through their phones.
Furthermore, we show that this leakage does not come from the durations, but from the phones: if we run the evaluation without replacing the "1" with the phone's duration in the one-hot embeddings.

## How to run the evaluation with phone durations

Running this evaluation is straight-forward, if you know how to run the original evaluation with mel-spectrograms (explained [here](https://carlosfranzreb.github.io/spane-guide)).
Instead of using the spkid config `spane/config/components/spkid/ecapa.yaml`, you use `spane/config/components/spkid/ecapa_phone_durations.yaml`.
Everything is the same between these two configs, except the `compute_features` function, defined in the train config (`spane/config/components/spkid/train_ecapa_phone_durations.yaml`).
The feature extractor, defined as ``, can be found [here](https://github.com/carlosfranzreb/spkanon_models/blob/main/knnvc_private/phone_durations.py) in the `spkanon_models` repository.
You have to clone that repo within `spane` to run this evaluation, as it uses the phone recognizer from private kNN-VC.
How to do that is explained in the [getting started guide](https://carlosfranzreb.github.io/spane-guide).

Please reach out to me if you have any questions!
