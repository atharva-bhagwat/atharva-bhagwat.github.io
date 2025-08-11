---
layout: page
title: Articles
permalink: articles/
---
<div class="cover-wrapper cover-wrapper-3-col l-page">
    {% assign sortedArticles = site.data.articles | where: "featured", true %}
    {% for feature in sortedArticles %}
    {% include feature.html feature=feature %}
    {% endfor %}
</div>
