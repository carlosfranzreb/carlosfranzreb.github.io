---
title: "Private kNN-VC"
date: 2020-03-18
layout: post
---

Private kNN-VC is an anonymizer for speech.
Given a speech sample and a target speaker, it outputs speech that preserves the content of the input speech but sounds like the target speaker.
To enhance privacy, the duration and variation of the phones are anonymized, as they contain speaker information.

## Examples

{% assign release_url = "https://github.com/carlosfranzreb/carlosfranzreb.github.io/releases/download/v0.1.0/" %}
{% assign librispeech_id = "1089-134686-0000" %} {# Assuming this ID is fixed for this table #}
{% assign target_speaker_ids = "0,1,2,3" | split: "," %}
{% assign initial_target_speaker_id = target_speaker_ids[0] %}
{% assign duration_values = "0,7,10" | split: "," %} {# Corresponds to 'w' in your table, and first part of config in filename #}
{% assign variation_values = "0,8,32" | split: "," %} {# Corresponds to 'c' in your table, and second part of config in filename #}

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
        width: 100%; /* Your existing style */
        min-width: 180px; /* Ensure player controls are visible */
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
        padding: 5px;
        border-radius: 4px;
    }
</style>

<div class="controls-container">
    <label for="targetSpeakerSelect">Target Speaker:</label>
    <select id="targetSpeakerSelect">
        {% for speaker_id in target_speaker_ids %}
            <option value="{{ speaker_id }}" {% if speaker_id == initial_target_speaker_id %}selected{% endif %}>Speaker {{ speaker_id }}</option>
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
                        <audio controls preload="metadata" style="width:100%;">
                            <source src="{{ release_url }}{{ dur_val }}-{{ var_val }}_{{ librispeech_id }}_{{ initial_target_speaker_id }}.flac" type="audio/flac">
                            Your browser does not support the audio element.
                        </audio>
                    </td>
                {% endfor %}
            </tr>
        {% endfor %}
    </tbody>
</table>

<script>
    document.addEventListener('DOMContentLoaded', function () {
        const targetSpeakerSelect = document.getElementById('targetSpeakerSelect');
        const audioCells = document.querySelectorAll('td.audio-cell[data-dur][data-var]');
        const releaseUrl = "{{ release_url }}";
        const librispeechId = "{{ librispeech_id }}";

        targetSpeakerSelect.addEventListener('change', function () {
            const selectedTargetSpeakerId = this.value;

            audioCells.forEach(cell => {
                const durVal = cell.dataset.dur;
                const varVal = cell.dataset.var;
                const audioElement = cell.querySelector('audio');
                const sourceElement = audioElement.querySelector('source');
                const newSrc = `${releaseUrl}${durVal}-${varVal}_${librispeechId}_${selectedTargetSpeakerId}.flac`;
                sourceElement.setAttribute('src', newSrc);
                audioElement.load();
            });
        });
    });
</script>