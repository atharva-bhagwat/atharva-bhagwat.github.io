---
layout: home
title: Home
---

<div id="intro-wrapper" class="l-text">
 <div id="intro-title-wrapper">
  <div id="intro-image-wrapper">
   <img id="intro-image" src="/images/portrait.jpg"></div>
  <div id="intro-title-text-wrapper">
   <h1 id="intro-title">Atharva Bhagwat</h1>
   <div id="intro-subtitle">Computational Researcher at <a href="https://www.tsankovlab.org/" target='_blank'>Tsankov Lab</a>, Mount Sinai</div>
   <!-- <div id="intro-title-socials">
    {% for link in site.data.social-links %}
     {% if link.on-homepage == true %}
      {% include social-link.html link=link %}
     {% endif %}
    {% endfor %}
   </div> -->
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
</div>
</div>

<p style="font-size: 1.2rem">
 <div>
I'm currently exploring how <b><span class="cv-vis">cellular senescence</span></b> impacts lung tissue using <b><span class="cv-ai">10x Genomics Xenium spatial transcriptomics data</span></b>, with the goal of uncovering key biological pathways that drive these processes.
 </div>
 <div style="height: 0.75rem"></div>
 <div>
Before academia, I was as a Machine Learning Engineer working on anomaly detection and automation in textile industry.
 </div>
</p>
</div>

<hr class="l-page home-hr">

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
