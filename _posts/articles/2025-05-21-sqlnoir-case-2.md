---
layout: post
title: "Case #002: The Stolen Sound"
categories: articles
permalink: articles/sqlnoir-case-2
author: Atharva Bhagwat
---
<!-- markdownlint-disable MD032 MD033 -->

In the neon glow of 1980s Los Angeles, the West Hollywood Records store was rocked by a daring theft. A prized vinyl record, worth over $10,000, vanished during a busy evening, leaving the store owner desperate for answers. Vaguely recalling the details, you know the incident occurred on July 15, 1983, at this famous store.

Reading the case description these are the **clues** we can pick up:

- Location: **West Hollywood Records**
- Date: **July 15, 1983**
- Vinyl record was stolen; Type of crime: **theft**

## Going over the schema

There are 4 tables:
- crime_scene:
  - id: **PRIMARY KEY**
- witnesses:
  - id: **PRIMARY KEY**
  - crime_scene_id: **FOREIGN KEY** referencing `id` in `crime_scene`
- suspects:
  - id: **PRIMARY KEY**
- interviews:
  - suspect_id: **FOREIGN KEY** referencing `id` in `suspects`

<img src='/assets/images/articles/sqlnoir_case2/schema.png' alt='case2_schema'>

## Investigation

We start by looking through all the **thefts** that happened on **July 15, 1983** at **West Hollywood Records**.

```sql
select * from crime_scene where location = 'West Hollywood Records' and type = 'theft' and date = 19830715;
```

With the query result we confirm that we are looking at the correct crime.

We now look into the witnesses related to this crime. We can do this by using a `JOIN` on `crime_scene` and `witnesses` tables on their common key, using the filters we just used.

```sql
select witnesses.id, witnesses.clue from witnesses 
join crime_scene on witnesses.crime_scene_id = crime_scene.id 
where location = 'West Hollywood Records' and 
type = 'theft' and date = 19830715;
```

> "I saw a man wearing a red bandana rushing out of the store." ~ witness #1

> "The main thing I remember is that he had a distinctive gold watch on his wrist." ~ witness #2

New **clues**:
- Suspect was wearing a **red bandana**
- Suspect had a **gold watch**

We have enough information on the suspect, so we look in the **suspects** table where the bandana color is red and accessory is a gold watch.

```sql
select * from suspects 
where bandana_color = 'red' and 
accessory = 'gold watch';
```

There are three suspects *Tony Ramirez*, *Mickey Rivera*, and *Rico Delgado* who match the description.

We can now look at the interviews for these three suspects to see who our culprit is. We will use a `JOIN` on `suspects` and `interviews` tables as they share a common key, using the filters we just used.

```sql
select suspect_id, transcript, name from interviews 
join suspects on suspects.id = interviews.suspect_id 
where bandana_color = 'red' and accessory = 'gold watch';
```

> "I couldn't help it. I snapped and took the record." ~ Rico Delgado

We got him. Turns out the vinyl played both sides—and side B had all the evidence.

----

Thank you [Chris](https://github.com/hristo2612) for creating [SQL Noir](https://www.sqlnoir.com/).
