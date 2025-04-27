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
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
 </div>
 <div style="height: 1rem"></div>
 <div>
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
 </div>
 <div style="height: 1rem"></div>
 <div>
 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
 </div>
</div>

<hr class="l-middle home-hr">

<h2 class="feature-title">Featured <a href="/cv/#publications">Research Publications</a></h2>

<p class="feature-text">
 Latest research for fans of human-computer interaction, data visualization, and machine learning.
</p>

{% comment %}
<div class="cover-wrapper cover-wrapper-3-col l-page">
 {% assign sortedPublications = site.categories.papers | sort: 'feature-order' %}
 {% for feature in sortedPublications %}
  {% if feature.featured == true %}
   {% include feature.html feature=feature %}
  {% endif %}
 {% endfor %}
{% endcomment %}

<br>
<h2 class="feature-title">Featured <a href="/dissertation">Dissertation Publications</a></h2>

<p class="feature-text">
 My dissertation contributed interactive interfaces to enable machine learning interpretability at scale and for everyone.
</p>

<div class="cover-wrapper cover-wrapper-1-col l-text">
 {% include dissertation/document.html details=false location=home %}
</div>

{% comment %}
<div class="cover-wrapper cover-wrapper-3-col l-page">
 {% assign sortedPublications = site.categories.papers | sort: 'feature-order' %}
 {% for feature in sortedPublications %}
  {% if feature.dissertation == true %}
   {% include feature.html feature=feature %}
  {% endif %}
 {% endfor %}
</div>
{% endcomment %}

<br>
<h2 class="feature-title">Apple <a href="https://developer.apple.com/design/human-interface-guidelines/">Chart Design Guidelines</a></h2>

<p class="feature-text">
 Guidance and best practices to help designers and developers create the best charts for Apple platforms.
</p>

{% comment %}
<div class="cover-wrapper cover-wrapper-2-col l-middle">
 {% for feature in site.data.designs %}
  {% if feature.featured == true %}
   {% include feature.html feature=feature %}
  {% endif %}
 {% endfor %}
</div>
{% endcomment %}

<br>
<h2 class="feature-title">Featured <a href="/cv/#interactive-articles">Interactive Articles</a></h2>

<p class="feature-text">
 Enhanced reading experiences that demonstrate what's possible when dynamic media are effectively combined.

</p>

{% comment %}
<div class="cover-wrapper cover-wrapper-3-col l-page">
 {% assign sortedArticles = site.data.articles | where: "featured", true %}
 {% assign ia = site.categories.papers | where:"permalink", "papers/interactive-articles" %}

 {% assign feature = sortedArticles[1] %}
 {% include feature.html feature=feature %}

 {% assign feature = sortedArticles[0] %}
 {% include feature.html feature=feature %}

 {% assign feature = ia[0] %}
 {% include feature.html feature=feature %}
</div>
{% endcomment %}

<br>
<h2 class="feature-title"><a href="https://parametric.press/about">Parametric Press</a></h2>

<p class="feature-text">
 A born-digital, experimental magazine dedicated to showcasing the expository power of the web.
</p>

{% comment %}
<div class="cover-wrapper cover-wrapper-2-col l-middle">
 {% assign parametric = site.data.articles | where: "parametric-issue", true %}
 {% for feature in parametric %}
  {% include feature.html feature=feature %}
 {% endfor %}
</div>
{% endcomment %}

[cv]: {{ site.url }}/cv
