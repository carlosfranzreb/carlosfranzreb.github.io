---
title: "Private kNN-VC"
date: 2020-03-18
layout: post
---

Private kNN-VC is an anonymizer for speech.
Given a speech sample and a target speaker, it outputs speech that preserves the content of the input speech but sounds like the target speaker.
To enhance privacy, the duration and variation of the phones are anonymized, as they contain speaker information.

## Examples

<video controls="" name="0-0_1089-134686-0000_0">
    <source src="https://github.com/carlosfranzreb/carlosfranzreb.github.io/releases/download/v0.1.0/0-0_1089-134686-0000_0.flac" type="audio/mp3">
</video>

{% assign release_url = "https://github.com/carlosfranzreb/carlosfranzreb.github.io/releases/download/v0.1.0/" %}
{% assign duration_values = "0,7,10" | split: "," %}
{% assign variation_values = "0,8,32" | split: "," %}

<table>
    <thead>
        <tr>
            <th>Duration \\ Variation</th>
            {% for dur_val in duration_values %}
                <th>{{ dur_val }}</th>
            {% endfor %}
        </tr>
    </thead>
    <tbody>
        {% for var_val in variation_values %}
            <tr>
                <td><b>{{ p1_val }}</b></td>
                {% for dur_val in duration_values %}
                    <td>
                        <video controls>
                            <source src="{{ release_url }}{{ dur_val }}-{{ var_val }}_1089-134686-0000_0.flac" type="audio/flac">
                        </video>
                    </td>
                {% endfor %}
            </tr>
        {% endfor %}
    </tbody>
</table>