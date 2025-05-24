---
layout: post
title: "Case #002: The Stolen Sound"
categories: articles
permalink: articles/sqlnoir-case-2
author: Atharva Bhagwat
---

In the neon glow of 1980s Los Angeles, the West Hollywood Records store was rocked by a daring theft. A prized vinyl record, worth over $10,000, vanished during a busy evening, leaving the store owner desperate for answers. Vaguely recalling the details, you know the incident occurred on July 15, 1983, at this famous store. Your task is to track down the thief and bring them to justice.

Reading the case description these are the **clues** we can pick up:

- Location: **West Hollywood Records**
- Date: **July 15, 1983**
- Vinyl record was stolen; Type of crime: **theft**

## Going over the schema

There are 3 tables:

- crime_scene:
  - id: **PRIMARY KEY**
- suspects:
  - id: **PRIMARY KEY**
- interviews:
  - suspect_id: **FORIEGN KEY** referencing `id` in `suspects`

<img src='/assets/images/articles/sqlnoir_case1/schema.png' alt='case1_schema' width="25">

## Investigation

----

Thank you [Chris](https://github.com/hristo2612) for creating [SQL Noir](https://www.sqlnoir.com/).
