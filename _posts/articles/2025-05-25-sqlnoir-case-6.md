---
layout: post
title: "Case #006: The Vanishing Diamond"
categories: articles
permalink: articles/sqlnoir-case-6
author: Atharva Bhagwat
---
<!-- markdownlint-disable MD032 MD033 -->

At Miami’s prestigious Fontainebleau Hotel charity gala, the famous “Heart of Atlantis” diamond necklace suddenly disappeared from its display.

Reading the case description these are the **clues** we can pick up:

- Location: **Fontainebleau Hotel**
- Famous “Heart of Atlantis” diamond necklace suddenly disappeared; Type of crime: **theft**

## Going over the schema

There are 6 tables:
- crime_scene:
  - id: **PRIMARY KEY**
- guest:
  - id: **PRIMARY KEY**
- attire_registry:
  - id: **PRIMARY KEY**
  - guest_id: **FOREIGN KEY** referencing `id` in `guest`
- witness_statements:
  - id: **PRIMARY KEY**
  - guest_id: **FOREIGN KEY** referencing `id` in `guest`
- final_interviews:
  - id: **PRIMARY KEY**
  - guest_id: **FOREIGN KEY** referencing `id` in `guest`
- marina_rentals:
  - id: **PRIMARY KEY**
  - renter_guest_id: **FOREIGN KEY** referencing `id` in `guest`

<img src='/assets/images/articles/sqlnoir_case6/schema.png' alt='case6_schema'>

## Investigation

We start by looking through all the crime scenes where the `location` has Fontainebleau Hotel.

```sql
select * from crime_scene where location like '%Fontainebleau Hotel%';
```

> The Heart of Atlantis necklace disappeared. Many guests were questioned but only two of them gave valuable clues. One of them is a really famous actor. The other one is a woman who works as a consultant for a big company and her first name ends with "an".

New **clues**:
- witness #1 is a famous actor
- witness #2 is a woman who works as a consultant and her first name ends with 'an'

Let us look at witness statements using the witness descriptions we just got. We can do this by using a `JOIN` on `guest` and `witness_statements` tables.

```sql
select witness_statements.guest_id, guest.name, witness_statements.clue from witness_statements 
join guest on witness_statements.guest_id = guest.id 
where guest.occupation like '%Actor%' or 
(guest.occupation like '%consultant%' and guest.name like '%an %');
```

> I overheard someone say, "Meet me at the marina, dock 3.
> I saw someone holding an invitation ending with "-R". He was wearing a navy suit and a white tie.

New **clues**:
- Marina dock 3 is relevant
- Invitation ending with '-R' wearing a navy suit and white tie

Let's look at marina rentals using the other clues as filters. We can use `JOIN` on `guest`, `attire_registry`, and `marina_rentals`.

```sql
select guest.id, guest.name, guest.invitation_code, attire_registry.note, 
marina_rentals.dock_number, marina_rentals.rental_date, marina_rentals.boat_name from guest 
join attire_registry on guest.id = attire_registry.guest_id 
join marina_rentals on guest.id = marina_rentals.renter_guest_id  
where attire_registry.note like '%navy suit, white tie%' and 
guest.invitation_code like '%-R';
```

We only get one entry. This has to be our guy. Let's look at the final interview.

```sql
select guest.name, final_interviews.confession from guest 
join final_interviews on guest.id = final_interviews.guest_id 
where guest.id = 105;
```

> "I was the one who took the crystal. I guess I need a lawyer now?" ~ Mike Manning

We got him. Too bad the spotlight never left the “Heart of Atlantis”.

----

Thank you [Chris](https://github.com/hristo2612) for creating [SQL Noir](https://www.sqlnoir.com/).
