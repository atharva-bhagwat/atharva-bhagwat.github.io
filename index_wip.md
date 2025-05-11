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

🚧 Work in progress.. 🚧
