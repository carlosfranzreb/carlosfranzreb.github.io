---
title: "Private kNN-VC"
date: 2025-05-23
layout: post
---

Private kNN-VC is an anonymizer for speech.
Given a speech sample and a target speaker, it outputs speech that preserves the content of the input speech but sounds like the target speaker.
To enhance privacy, the duration and variation of the phones are anonymized, as they contain speaker information.

## Links

- [GitHub repository](https://github.com/carlosfranzreb/private_knnvc)
- [Pre-print](https://arxiv.org/pdf/2505.17584)

## Examples

Phone variation is restricted by clustering the target features.
In the table below, each row represents a different number of clusters.
More clusters mean that there are more available features for the kNN conversion, i.e. more variability.
The resulting audio sounds more expressive.
0 clusters means that no clustering was performed, i.e. all target features of each phone are candidates.

Phone duration is anonymized by interpolating the actual durations with a different set of phone durations predicted by a model that was developed for text-to-speech.
Each column in the table represents a different degree of interpolation.
w=0 means that durations were not anonymized; w=7 means that the predicted durations were multiplied with 0.7 and added with the actual durations, which were multiplied with 0.3; w=10 means that the predicted durations were used.

{% assign release_url = "https://github.com/carlosfranzreb/carlosfranzreb.github.io/releases/download/v0.1.0/" %}
{% assign audio_files = "1089-134686-0000,1580-141083-0000,1284-1180-0000,121-121726-0000" | split: "," %}
{% assign target_speaker_ids = "0,1,2,3" | split: "," %}
{% assign duration_values = "0,7,10" | split: "," %}
{% assign variation_values = "0,8,32" | split: "," %}
{% assign valid_combinations = "0-0,0-8,7-32,10-0,10-8" | split: "," %}

<style>
    table {
        border-collapse: collapse;
        width: 80%;
        margin: 20px auto;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: center;
    }
    th {
        background-color: #f2f2f2;
    }
    audio {
        width: 100%;
        min-width: 180px;
    }
    .controls-container {
        margin: 20px auto;
        width: 80%;
        text-align: center;
        padding: 10px;
    }
    .controls-container label {
        margin-right: 10px;
        font-weight: bold;
    }
    .controls-container select {
        padding: 10px;
        border-radius: 4px;
    }
</style>

<div class="controls-container">
    <label for="targetSpeakerSelect">Target Speaker:</label>
    <select id="targetSpeakerSelect">
        {% for speaker_id in target_speaker_ids %}
            <option value="{{ speaker_id }}" {% if speaker_id == target_speaker_ids[0] %}selected{% endif %}>Speaker {{ speaker_id }}</option>
        {% endfor %}
    </select>

    <label for="audioFileSelect">Audio file:</label>
    <select id="audioFileSelect">
        {% for audio_file in audio_files %}
            <option value="{{ audio_file }}" {% if audio_file == audio_files[0] %}selected{% endif %}>{{ audio_file }}</option>
        {% endfor %}
    </select>
</div>

<table>
    <thead>
        <tr>
            <th></th>
            {% for dur_val in duration_values %}
                <th>w={{ dur_val }}</th>
            {% endfor %}
        </tr>
    </thead>
    <tbody>
        {% for var_val in variation_values %}
            <tr>
                <td><b>c={{ var_val }}</b></td>
                {% for dur_val in duration_values %}
                    <td class="audio-cell" data-dur="{{ dur_val }}" data-var="{{ var_val }}">
                        {% capture config %}{{ dur_val }}-{{ var_val }}{% endcapture %}
                        {% if valid_combinations contains config %}
                            <audio controls preload="metadata">
                                <source src="{{ release_url }}{{ dur_val }}-{{ var_val }}_{{ audio_files[0] }}_{{ target_speaker_ids[0] }}.flac" type="audio/flac">
                                Your browser does not support the audio element.
                            </audio>
                        {% endif %}
                    </td>
                {% endfor %}
            </tr>
        {% endfor %}
    </tbody>
</table>

<script>
    document.addEventListener('DOMContentLoaded', function () {
        const audioFileSelect = document.getElementById('audioFileSelect');
        const targetSpeakerSelect = document.getElementById('targetSpeakerSelect');
        const audioCells = document.querySelectorAll('td.audio-cell[data-dur][data-var]');
        const releaseUrl = "{{ release_url }}";

        function updateCells() {
            const audioFile = audioFileSelect.value;
            const targetSpeaker = targetSpeakerSelect.value;

            audioCells.forEach(cell => {
                const durVal = cell.dataset.dur;
                const varVal = cell.dataset.var;
                const audioElement = cell.querySelector('audio');
                if (!audioElement)
                    return;

                const sourceElement = audioElement.querySelector('source');
                const newSrc = `${releaseUrl}${durVal}-${varVal}_${audioFile}_${targetSpeaker}.flac`;
                sourceElement.setAttribute('src', newSrc);
                audioElement.load();
            });
        }

        targetSpeakerSelect.addEventListener('change', updateCells);
        audioFileSelect.addEventListener('change', updateCells);
    });
</script>