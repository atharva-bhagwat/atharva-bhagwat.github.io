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

<img src='/assets/images/articles/sqlnoir_case1/schema.png' alt-text='case1_schema' width="25">

## Investigation

We start by looking through all the crime scenes that happened at the **Blue Note Lounge**.

```sql
select * from crime_scene
where location = 'Blue Note Lounge';
```

We get this description of the crime:

> "A briefcase containing sensitive documents vanished. A witness reported a man in a trench coat with a scar on his left cheek fleeing the scene."

New **clue**:

- Suspect has a **scar** on his **left cheek**

We now have enough information on the suspect, so we look in the suspects table where the attire is trench coat and there is a scar on the left cheek.

```sql
select * from suspects 
where attire = 'trench coat' and scar = 'left cheek';
```

There are two suspects *Frankie Lombardi* and *Vincent Malone* who match the description.

We can now look at the interviews for these two suspects to see who our culprit is. This can be done in many ways, we simply use a `JOIN` on suspects and interviews tables as they share a common key, filtered using conditions on attire and scar.

```sql
select suspect_id, transcript, name from interviews 
join suspects on suspects.id = interviews.suspect_id 
where attire = 'trench coat' and scar = 'left cheek';
```

> "I wasn’t going to steal it, but I did." ~ Vincent Malone

We got the guy!

----

Thank you [Chris](https://github.com/hristo2612) for creating [SQL Noir](https://www.sqlnoir.com/).
