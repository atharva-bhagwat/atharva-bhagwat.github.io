---
layout: cv
title: CV
permalink: cv/
jsarr:
- js/scripts.js
---

<h1 id="cv-title"><a href="{{ site.url }}">Atharva Bhagwat</a></h1>

<p id="cv-subtitle"><i>Associate Computational Researcher</i></p>

<!-- <div id="cv-toc">
<ul class="cv-description">
	<li>Education</li>
	<li>Industry Research</li>
	<li>Academic Research</li>
	<li>Honors and Awards</li>
	<li>Publications</li>
	<li>Talks</li>
	<li>Press</li>
	<li>Teaching</li>
	<li>Mentoring</li>
	<li>Grants and Funding</li>
	<li>Interactive Articles</li>
	<li>Service</li>
	<li>Design</li>
	<li>References</li>
</ul>
</div> -->

<div>
I design and develop <b><span class="cv-vis">interactive interfaces</span></b> to help people <b><span class="cv-ai">understand machine learning</span></b> models and data-driven systems. Besides building tools, I also create data visualizations and write interactive articles to simply communicate complex ideas.
</div>

<div class="cv-spacer"></div>

<div>
I have collaborated with researchers, designers, developers, and artists while working at Apple, Microsoft Research, NASA Jet Propulsion Lab, and Pacific Northwest National Lab.
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

{% assign journal = site.categories.papers | where: 'type', "journal" %}
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
