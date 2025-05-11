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
   <div id="intro-subtitle">Associate Computational Researcher at Tsankov Lab</div>
   <div id="intro-title-socials">
    {% for link in site.data.social-links %}
     {% if link.on-homepage == true %}
      {% include social-link.html link=link %}
     {% endif %}
    {% endfor %}
   </div>
  </div>
 </div>
 <!-- <hr class="l-middle home-hr"> -->
 <div id="everything-else" class="l-middle">
  <a href="{{ site.url }}/cv"><div><i class="fa fa-portrait icon icon-right-space"></i>CV</div></a>
  <a href="{{ site.url }}/projects"><div><i class="fa fa-shapes icon icon-right-space"></i>Projects</div></a>
  <!-- <a href="{{ site.url }}/everything-else"><div><i class="fa fa-list-ul icon icon-right-space"></i>Everything Else</div></a> -->
 </div>
 <div>
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
 </div>
 <div style="height: 1rem"></div>
 <div>
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
 </div>
 <div style="height: 1rem"></div>
 <div>
 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
 </div>
</div>

<hr class="l-middle home-hr">

<h2 class="feature-title"><a href="/cv/#publications">Publications</a></h2>

{% assign selectedBoolForBibtex = false %}
{% assign journal = site.data.publications | where: 'type', "journal" %}
{% for pub in journal %}
{% include cv/publication.html pub=pub selectedBoolForBibtex=selectedBoolForBibtex %}
{% endfor %}

<h2 class="feature-title"><a href="/cv/#articles">Articles</a></h2>

<div class="cover-wrapper cover-wrapper-3-col l-page">
 {% assign sortedArticles = site.data.articles | where: "featured", true %}
{% for feature in sortedArticles %}
{% include feature.html feature=feature %}
{% endfor %}
</div>

[cv]: {{ site.url }}/cv
