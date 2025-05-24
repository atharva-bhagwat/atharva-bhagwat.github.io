---
layout: post
title: "Case #003: The Miami Marina Murder"
categories: articles
permalink: articles/sqlnoir-case-3
author: Atharva Bhagwat
---
<!-- markdownlint-disable MD032 MD033 -->

A body was found floating near the docks of Coral Bay Marina in the early hours of August 14, 1986.

Reading the case description these are the **clues** we can pick up:

- Location: **Coral Bay Marina**
- Date: **August 14, 1986**
- Dead body was found; Type of crime: **murder**

## Going over the schema

There are 6 tables:
- crime_scene:
  - id: **PRIMARY KEY**
- person:
  - id: **PRIMARY KEY**
- hotel_checkins:
  - id: **PRIMARY KEY**
  - person_id: **FOREIGN KEY** referencing `id` in `person`
- confessions:
  - id: **PRIMARY KEY**
  - person_id: **FOREIGN KEY** referencing `id` in `person`
- interviews:
  - id: **PRIMARY KEY**
  - person_id: **FOREIGN KEY** referencing `id` in `person`
- surveillance_records:
  - id: **PRIMARY KEY**
  - person_id: **FOREIGN KEY** referencing `id` in `person`
  - hotel_checkin_id: **FOREIGN KEY** referencing `id` in `hotel_checkin`

<img src='/assets/images/articles/sqlnoir_case3/schema.png' alt='case3_schema'>

## Investigation

We start by looking through all the crime scenes where the `location` is Coral Bay Marina and `date` is August 14, 1986.

```sql
select * from crime_scene where date = 19860814 and location = 'Coral Bay Marina';
```

> The body of an unidentified man was found near the docks. Two people were seen nearby: one who lives on 300ish "Ocean Drive" and another whose first name ends with "ul" and his last name ends with "ez".

New **clues**:
- Two people seen
  - one lives on 300ish "Ocean Drive"
  - other first name ends with "ul" and his last name ends with "ez"

We now look into the `person` table where `address` has *300ish Ocean Drive* or the `name` is of pattern \*ul \*ez

```sql
select * from person 
where address like '3__ %Ocean Drive%' or 
name like '%ul %ez';
```

The two names that pop-up are *Carlos Mendez* and *Raul Gutierrez*. We can use `JOIN` on person and interviews with the filters we just used.

```sql
select interviews.transcript from interviews 
join person on interviews.person_id = person.id 
where person.address like '3__ %Ocean Drive%' or 
name like '%ul %ez';
```

> "I saw someone check into a hotel on August 13. The guy looked nervous."
> "I heard someone checked into a hotel with 'Sunset' in the name."

New **clues**:
- Suspect checked into a hotel on August 13, 1986
- Hotel has 'Sunset' in its name

We can use `JOIN` this time on `hotel_checkins` table and `person` table where the check in date is August 13, 1986 and hotel has 'Sunset' in its name.

```sql
select * from hotel_checkins 
join person on hotel_checkins.person_id = person.id 
where hotel_checkins.hotel_name like '%Sunset%' and 
hotel_checkins.check_in_date = 19860813;
```

Well, this does not narrow down our list of suspects. We can look into the `surveillance_records` where the `person_id` is present in the hotel checkins we just looked at.

```sql
select * from surveillance_records where 
person_id in (
  select hotel_checkins.person_id from hotel_checkins 
  join person on hotel_checkins.person_id = person.id 
  where hotel_checkins.hotel_name like '%Sunset%' and 
  hotel_checkins.check_in_date = 19860813
) and suspicious_activity is not NULL;
```

After a little bit of grunt work we can narrow down our search to these suspects:

| person_id | hotel_checkin_id | suspicious_activity |
|----|----|----|
| 6 | 34 | Spotted entering late at night |
| 7 | 89 | Seen arguing with an unknown person |
| 8 | 2 | Left suddenly at 3 AM |

We can now look at confessions where `person_id` in `[6, 7, 8]`. To simplify, we `JOIN` `confessions` and `person` tables to directly get person name along with the confession.

```sql
select person.name, confessions.confession from confessions 
join person on person.id = confessions.person_id 
where person_id in (6,7,8);
```

> "Alright! I did it. I was paid to make sure he never left the marina alive." ~ Thomas Brown

We got him. The tide tried to keep the secret. But in Coral Bay, even the water talks.

----

Thank you [Chris](https://github.com/hristo2612) for creating [SQL Noir](https://www.sqlnoir.com/).
