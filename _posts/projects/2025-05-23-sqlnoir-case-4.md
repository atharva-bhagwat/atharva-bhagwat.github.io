---
layout: post
title: "Case #004: The Midnight Masquerade Murder"
categories: projects
permalink: projects/sqlnoir-case-4
author: Atharva Bhagwat
---
<!-- markdownlint-disable MD032 MD033 -->

On October 31, 1987, at a Coconut Grove mansion masked ball, Leonard Pierce was found dead in the garden.

Reading the case description these are the **clues** we can pick up:

- Location: **Coconut Grove mansion**
- Date: **October 31, 1987**
- Leonard Pierce was found dead; Type of crime: **murder**

## Going over the schema

There are 9 tables:
- crime_scene:
  - id: **PRIMARY KEY**
- person:
  - id: **PRIMARY KEY**
- witness_statements:
  - id: **PRIMARY KEY**
  - crime_scene_id: **FOREIGN KEY** referencing `id` in `crime_scene`
  - witness_id: **FOREIGN KEY** referencing `id` in `person`
- final_interviews:
  - id: **PRIMARY KEY**
  - person_id: **FOREIGN KEY** referencing `id` in `person`
- vehicle_registry:
  - id: **PRIMARY KEY**
  - person_id: **FOREIGN KEY** referencing `id` in `person`
- catering_orders:
  - id: **PRIMARY KEY**
  - person_id: **FOREIGN KEY** referencing `id` in `person`
- phone_records:
  - id: **PRIMARY KEY**
  - caller_id: **FOREIGN KEY** referencing `id` in `person`
  - recipient_id: **FOREIGN KEY** referencing `id` in `person`
- hotel_checkins:
  - id: **PRIMARY KEY**
  - person_id: **FOREIGN KEY** referencing `id` in `person`
- surveillance_records:
  - id: **PRIMARY KEY**
  - hotel_checkin_id: **FOREIGN KEY** referencing `id` in `hotel_checkins`

<img src='/assets/images/articles/sqlnoir_case4/schema.png' alt='case4_schema'>

## Investigation

We start by looking through all the crime scenes where the `location` has Coconut Grove and `date` is October 31, 1987.

```sql
select * from crime_scene where date = 19871031 and location like '%Coconut Grove%';
```

> During a masked ball, a body was found in the garden. Witnesses mentioned a hotel booking and suspicious phone activity.

Let us also look at witness statements for this crime. We can do this by using a `JOIN` on `crime_scene` and `witness_statements` tables.

```sql
select witness_statements.witness_id, witness_statements.clue from witness_statements 
join crime_scene on witness_statements.crime_scene_id = crime_scene.id 
where crime_scene.date = 19871031 and 
crime_scene.location like '%Coconut Grove%';
```

> I overheard a booking at The Grand Regency.

> I noticed someone at the front desk discussing Room 707 for a reservation made yesterday.

New **clues**:
- Hotel booking at *The Grand Regency*
- Room *707* booked on *October 30, 1987*

We look into all the surveillance records for hotel checkins at The Grand Regency for room 707 on October 30, 1987.

```sql
select surveillance_records.id, surveillance_records.hotel_checkin_id, 
surveillance_records.note from surveillance_records 
join hotel_checkins on surveillance_records.hotel_checkin_id = hotel_checkins.id
where hotel_checkins.hotel_name = 'The Grand Regency' and 
hotel_checkins.room_number = 707 and
hotel_checkins.check_in_date = 19871030 and
surveillance_records.note is not NULL;
```

| hotel_checkin_id | note |
|----|----|
| 119 | Subject was overheard yelling on a phone: "Did you kill him?" |

We can look at hotel checkins for id 119 and see which person checked in.

```sql
select * from hotel_checkins where id = 119;
```

| id | person_id | hotel_name | check_in_date | room_number |
|----|----|----|----|----|
| 119 | 11 | The Grand Regency | 19871030 | 707 |

We now look into the phone records for person id 11. *(Query below also looks at phone records for person id 58 as they are the recipient of the call)*

```sql
select * from phone_records where caller_id in (11, 58) or recipient_id in (11, 58);
```

> "Why did you kill him, bro? You should have left the carpenter do it himself!"

> "I will do it. Only if you give me that nice Lambo of yours."

New **clues**:
- Suspect maybe be a carpenter
- Suspect owns a Lamborghini

We can use `JOIN` on `person` and `vehicle_registry` to find our suspect.

```sql
select * from vehicle_registry 
join person on person.id = vehicle_registry.person_id 
where car_make = 'Lamborghini' and 
person.occupation like 'carpenter';
```

*Marco Santos* is the only name which pops up. Let us look at final interview for this person.

```sql
select * from final_interviews
where person_id = 97;
```

> "I ordered the hit. It was me. You caught me." ~ Marco Santos

We got him. The mask slipped.

----

Thank you [Chris](https://github.com/hristo2612) for creating [SQL Noir](https://www.sqlnoir.com/).
