---
title: "Getting Started with SpAnE"
date: 2025-08-13
layout: post
---

[SpAnE](https://github.com/carlosfranzreb/spane) is an open-source framework for running and evaluating speaker anonymizers.
This post shows how to setup and run the framework with [private kNN-VC](https://carlosfranzreb.github.io/private-knnvc.html).
You will need access to a GPU to run the anonymizer, as we will run the proper evaluation with all the data, not just a mock test.

If anything is unclear or doesn't work, please let me know!
You can [write me an e-mail](mailto:carlos.franzreb@dfki.de) or [open an issue](https://github.com/carlosfranzreb/spane/issues/new).

## Index

1. [Installing SpAnE](#installing-spane)
2. [Installing the anonymizer](#installing-the-anonymizer)
3. [Running the experiment](#running-the-experiment)
4. [Interpreting the results](#interpreting-the-results)
5. [Privacy evaluation](#privacy-evaluation)
6. [Utility evaluation](#utility-evaluation)
7. [What's next?](#whats-next)

## Installing SpAnE

First you need to install the framework inside a directory where you implement your anonymizers and run the experiments, as shown below.

```linux
spkanon/
  venv/
  logs/
  checkpoints/
  spkanon_eval/
    spkanon_eval/
    tests/
    spkanon_models
    NISQA/
    ...
```

I use `spkanon` as the parent directory.
Replace it with your choice in the snippet below and run it to create the directory and install SpAnE inside it.
It will take some time, as it will run the tests as well to check that everything works.
If it doesn't, please contact me or open an issue on GitHub!

```linux
mkdir spkanon
cd spkanon
git clone https://github.com/carlosfranzreb/spane.git
bash spane/build/framework.sh
```

## Installing the anonymizer

The anonymizers are implemented in a separate repository, called [spkanon_models](https://github.com/carlosfranzreb/private_spkanon_models).
It should be installed inside SpAnE, for the framework to access the models.
If you have not moved after running the previous snippet, the following snippet installs it in the correct place.

```linux
cd spane
git clone https://github.com/carlosfranzreb/spkanon_models.git
```

Some of the anonymizers require additional Python packages or weights that have to be downloaded manually.
This is not done automatically; the requirements for each anonymizers are stated in its corresponding documentation.
They are also contained in scripts inside the `build` directory of the repository.
The scripts should be run outside of SpAnE, in the parent directory (`spkanon` in my case), so that the checkpoints are not tracked by SpAnE's git.
This is the case for private kNN-VC: to install it, run the following snippet (assuming you haven't moved since the last one).

```linux
cd ..
bash spane/spkanon_models/build/knnvc_private.sh
```

## Running the experiment

Before running the experiment, you need to change the root folder in the data configuration (file `./spane/config/datasets/config.yaml`).
The root folder is the path to the folder where you store your datasets.
It will be used to replace the `{root}` placeholders in the datafiles.

Once that's done, you can run the experiment with the following command:

```bash
python spane/run.py spane/config/config.yaml
```

The experiment will take a while.
You can check how it's going in the log file.
Open `logs/knnvc_private`, which is the logging directory defined in the config, and you will find the experiment folder under a timestamp.
Timestamps are added to the logging folder to avoid duplicates when running batches of experiments.
The log file is called `progress.log`.

## Interpreting the results

Once the experiment finishes, you can also check how long each step took in the `progress.log` file:

1. Computing target features: 10 min.
2. Anonymizing evaluation dataset: 3 min.
3. Privacy evaluation:
  a. Anonymizing training dataset: 1 hour and 42 min.
  b. Training the speaker recognizer: 2 hours and 7 min.
  c. Evaluation: 8 min.
4. Intelligibility evaluation (whisper-small): 7 min.
5. Intelligibility evaluation (whisper-large): 27 min.
6. Naturalness evaluation: 5 min.
7. Performance evaluation: 2 min.

The privacy evaluation is by far the slowest step in the whole experiment.
Since first releasing SpAnE, we have improved the runtime by sorting the datafiles by duration and estimating the optimal batch size for different durations, to optimize the GPU usage.
You can check how this is done in the file `spane/spkanon_eval/datamodules/batch_size_calculator`.

The evaluation results are in the `eval` folder, under the experiment folder.
We will discuss them in the remainder of this section.

## Privacy evaluation

We have run the semi-informed privacy evaluation, which is the strongest attack scenario.
The speaker recognizer is trained with anonymized data, and the enrollment utterances are anonymized as well.
The results can be found in the folder `asv-cos/semi-informed`.

The training log of the recognizer (`train/spkid/train_log.txt`) shows how the training went:

```log
epoch: 1, lr: 2.46e-05, tgt_weight: 0.00e+00 - train loss: 12.36 - valid loss: 11.60, valid error_rate_src: 9.98e-01, valid error_rate_tgt: 9.72e-01
epoch: 2, lr: 4.81e-05, tgt_weight: 0.00e+00 - train loss: 11.46 - valid loss: 11.38, valid error_rate_src: 9.96e-01, valid error_rate_tgt: 9.31e-01
epoch: 3, lr: 7.17e-05, tgt_weight: 0.00e+00 - train loss: 11.16 - valid loss: 11.06, valid error_rate_src: 9.93e-01, valid error_rate_tgt: 8.05e-01
epoch: 4, lr: 9.53e-05, tgt_weight: 0.00e+00 - train loss: 10.63 - valid loss: 10.48, valid error_rate_src: 9.81e-01, valid error_rate_tgt: 5.61e-01
epoch: 5, lr: 1.19e-04, tgt_weight: 0.00e+00 - train loss: 9.87 - valid loss: 9.75, valid error_rate_src: 9.67e-01, valid error_rate_tgt: 2.76e-01
epoch: 6, lr: 1.42e-04, tgt_weight: 0.00e+00 - train loss: 8.99 - valid loss: 9.07, valid error_rate_src: 9.53e-01, valid error_rate_tgt: 1.38e-01
epoch: 7, lr: 1.66e-04, tgt_weight: 0.00e+00 - train loss: 8.17 - valid loss: 8.48, valid error_rate_src: 9.40e-01, valid error_rate_tgt: 7.16e-02
epoch: 8, lr: 1.90e-04, tgt_weight: 0.00e+00 - train loss: 7.55 - valid loss: 8.09, valid error_rate_src: 9.26e-01, valid error_rate_tgt: 4.38e-02
epoch: 9, lr: 2.13e-04, tgt_weight: 0.00e+00 - train loss: 7.11 - valid loss: 7.90, valid error_rate_src: 9.15e-01, valid error_rate_tgt: 3.96e-02
epoch: 10, lr: 2.37e-04, tgt_weight: 0.00e+00 - train loss: 6.82 - valid loss: 7.87, valid error_rate_src: 9.06e-01, valid error_rate_tgt: 5.01e-02
```

For each epoch you can see:

- The learning rate, which is scheduled with Speechbrain's cyclic scheduler.
- The weight of the target classifier (explained below).
- The train and validation losses. 10% of each speaker's utterances are used for validation.
- The error rates for the source and target speakers on the validation set.

You can see that the recognizer's output encodes a lot of information about the target speakers (5% in the last epoch), although it is not informed about targets in any way.
In this [pre-print](https://www.arxiv.org/pdf/2508.09803), we train the recognizer adversarially with the target classifier to remove this information.
The target weight is used to determine the influence of the target classifier in the recognizer's training.
You can read more about this in the [corresponding release](https://github.com/carlosfranzreb/spane/releases/tag/paper_results_2).

The final validation error rate for the source speakers, which is what we ultimately care about, is 90.6%, meaning that we could protect their identity pretty well.
The evaluation is performed with unseen speakers, measuring the generalizability of the trained recognizer.
The results are in the folder `asv-cos/semi-informed/results`.
Here, you can find the equal error rate (EER) for the whole dataset under `eer.txt`.
The number of pairs should be 31,640 as we have 791 trial utterances and 40 enrollment speakers.
I get an EER of 32.4%; keep in mind that these values vary with a standard deviation of 0.5%, so it is best if you run the experiment several times to make sure your results are reliable.

### Utility evaluation

We ran three utility evaluations in this experiment: speech recognition, naturalness estimation and performance.
The overall results can be found in the files `all.txt`.
You can also find averages for the different population segments, which are defined as attributes in the evaluation datafile.
For Librispeech, it's only the gender.
There is also a file showing the average results for each target speaker.

#### Speech recognition

Ran with whisper-small and whisper-large, you can see word error rates (WERs) for the whole evaluation dataset in the files `all.txt`.
I get WER=0.06 for whisper-large and WER=0.09 for whisper-small.
In the file `target.txt`, you can see the avg. WER for each target speaker.
For whisper-small, I get pretty consistent results, ranging from 0.08 to 0.10.

### Naturalness

Naturalness is estimated with the NISQA model, and the results are stored in the folder `naturalness-nisqa`.
The overall mean opinion score (MOS) is 2.98 out of 5.
Looking at the genders, the anonymizer achieves a slightly higher naturalness on average for male source speakers: 3.01 versus 2.96 for female source speakers.

### Performance

The performance evaluation has files describing the CPU and GPU hardware (`cpu_specs.txt` and `gpu_specs.txt`).
My GPU is the *A100-SXM4-40GB*.
The GPU inference speed is stored in the file `cuda_inference.txt`.
For this GPU, it takes 0.06 seconds on average to anonymize an utterance that lasts 20 seconds.
On CPU, the avg. inference speed for the same input is 4.4 seconds (see `cpu_inference.txt`).

## What's next?

Here are some ideas for what to try out next.
Note that you can modify the config with flags when running an experiment, which is a useful feature for hyperparameter tuning or other batches of experiments.
This functionality is implemented in `spane/run.py`, in the function `override_with_args`.
It understands dots, if you want to change a config variable that is nested inside another one.
It cannot be used to override subconfigs yet (config variables that end with `_cfg`).

### Run the emotion evaluation

To evaluate emotion preservation, we compare the outcome of a [pre-trained emotion recognizer](https://huggingface.co/papers/2203.07378) for original and anonymized speech on two emotional datasets.
The datasets are [MSP-podcast](https://ieeexplore.ieee.org/document/8003425), which the recognizer was trained on, and [RAVDESS](https://www.kaggle.com/datasets/uwrfkaggler/ravdess-emotional-speech-audio), and out-of-domain dataset to check the generalizability of the results.
Given that these two datasets are only interesting for evaluating emotion preservation, they should be anonymized in a separate experiment.

To evaluate the emotion preservation, we need to change two parameters in the config file:

1. `datasets_cfg` has to be set to `spane/config/datasets/emotion.yaml`.
2. In `eval.components`, only the emotion evaluation should be present: `ser_cfg: spane/config/components/ser/audeering_w2v.yaml`.

Then you can run it like before!

Note that the `_cfg` suffixes are our way of defining paths to subconfigs, which are loaded on runtime in the function `load_subconfigs` of the `spane/run.py` file.

### Evaluate another anonymizer

The repository `spkanon_models`, which we cloned to run private kNN-VC, comprises other anonymizers.
For example, you can try out ASR-BN, which doesn't have any additional dependencies, and you don't have to download the weights manually.

To run ASR-BN, copy the content of the data config (`spane/config/datasets/librispeech.yaml`) onto the experiment config, as we need to change the target datafile, and change the following config variables

1. Set `pipeline_cfg` to `spane/spkanon_models/asrbn/config.yaml`.
2. Set `data.datasets.targets` to `spane/data/libritts/tts-train-clean-100.txt`.

Then you can run it like before with

```bash
python spane/run.py spane/config/config.yaml
```
