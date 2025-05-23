---
layout: post
title: "Case #001: The Vanishing Briefcase"
categories: articles
permalink: articles/sqlnoir-case-1
author: Atharva Bhagwat
---
<!-- markdownlint-disable MD032 MD033 -->

Set in the gritty 1980s, a valuable briefcase has disappeared from the Blue Note Lounge. A witness reported that a man in a trench coat was seen fleeing the scene.

Reading the case description these are the **clues** we can pick up:

- Crime happened in the 1980s
- Briefcase disappeared; Type of crime: **theft**
- Location: **Blue Note Lounge**
- Man in a **trench coat** was seen fleeing the scene

## Going over the schema

There are 3 tables:
- crime_scene:
  - id: **PRIMARY KEY**
- suspects:
  - id: **PRIMARY KEY**
- interviews:
  - suspect_id: **FOREIGN KEY** referencing `id` in `suspects`

<img src="/assets/images/articles/sqlnoir_case1/schema.png" alt="case1_schema">

## Investigation

We start by looking through all the crime scenes that happened at the **Blue Note Lounge**.

```sql
select * from crime_scene where location = 'Blue Note Lounge';
```

We get this description of the crime:

> "A briefcase containing sensitive documents vanished. A witness reported a man in a trench coat with a scar on his left cheek fleeing the scene."

New **clue**:

- Suspect has a **scar** on his **left cheek**

We have enough information on the suspect, so we look in the **suspects** table where the attire is trench coat and there is a scar on the left cheek.

```sql
select * from suspects where attire = 'trench coat' and scar = 'left cheek';
```

There are two suspects *Frankie Lombardi* and *Vincent Malone* who match the description.

We can now look at the interviews for these two suspects to see who our culprit is. This can be done in many ways, we simply use a `JOIN` on `suspects` and `interviews` tables as they share a common key, filtered using conditions on attire and scar.

```sql
select suspect_id, transcript, name from interviews 
join suspects on suspects.id = interviews.suspect_id 
where attire = 'trench coat' and scar = 'left cheek';
```

> "I wasn’t going to steal it, but I did." ~ Vincent Malone

We got the guy. The briefcase didn’t grow legs—just found the wrong hands.

----

Thank you [Chris](https://github.com/hristo2612) for creating [SQL Noir](https://www.sqlnoir.com/).
