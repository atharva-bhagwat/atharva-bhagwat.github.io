---
layout: cv
title: CV
permalink: cv/
jsarr:
- js/scripts.js
---

<h1 id="cv-title"><a href="{{ site.url }}">Atharva Bhagwat</a></h1>

<p id="cv-subtitle"><i>Associate Computational Researcher</i></p>

<div>
I'm currently exploring how <b><span class="cv-vis">cellular senescence</span></b> impacts lung tissue using <b><span class="cv-ai">10x Genomics Xenium spatial transcriptomics data</span></b>, with the goal of uncovering key biological pathways that drive these processes.
</div>

<div class="cv-spacer"></div>

<div class="cv-image-links-wrapper">
 <div class="cv-image-links">
  {% for link in site.data.social-links %}
   {% if link.cv-group == 1 %}
    {% include cv-social-link.html link=link %}
   {% endif %}
  {% endfor %}
 </div>
 <div class="cv-image-links">
  {% for link in site.data.social-links %}
   {% if link.cv-group == 2 %}
    {% include cv-social-link.html link=link %}
   {% endif %}
  {% endfor %}
 </div>
</div>

***

## Education

{::nomarkdown}
{% for degree in site.data.education %}
{% include cv/degree.html degree=degree %}
{% endfor %}
{:/}

## Work Experience

{% for experience in site.data.experiences %}
{% include cv/experience.html experience=experience %}
{% endfor %}

## Publications

{% assign selectedBoolForBibtex = false %}

{% assign journal = site.data.publications | where: 'type', "journal" %}
{% for pub in journal %}
{% include cv/publication.html pub=pub selectedBoolForBibtex=selectedBoolForBibtex %}
{% endfor %}

## Posters

{% assign selectedBoolForBibtex = false %}

{% assign journal = site.data.publications | where: 'type', "poster" %}
{% for pub in journal %}
{% include cv/publication.html pub=pub selectedBoolForBibtex=selectedBoolForBibtex %}
{% endfor %}

## Awards

{% for award in site.data.awards %}
{% include cv/award.html award=award %}
{% endfor %}

## Mentoring

{::nomarkdown}
{% for mentee in site.data.mentoring %}
{% include cv/mentee.html mentee=mentee %}
{% endfor %}
{:/}

[cv]: {{ site.url }}/cv.pdf "My CV."
