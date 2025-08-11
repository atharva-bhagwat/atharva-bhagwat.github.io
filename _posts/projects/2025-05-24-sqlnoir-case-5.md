---
layout: post
title: "Case #005: The Silicon Sabotage"
categories: projects
permalink: projects/sqlnoir-case-5
author: Atharva Bhagwat
---
<!-- markdownlint-disable MD032 MD033 -->

QuantumTech, Miami’s leading technology corporation, was about to unveil its groundbreaking microprocessor called “QuantaX.” Just hours before the reveal, the prototype was destroyed, and all research data was erased. Detectives suspect corporate espionage.

Reading the case description these are the **clues** we can pick up:

- Location: **QuantumTech**
- Prototype was destroyed, and all research data was erased; Type of crime: **corporate espionage**

## Going over the schema

There are 7 tables:
- incident_reports:
  - id: **PRIMARY KEY**
- employee_records:
  - id: **PRIMARY KEY**
- witness_statements:
  - id: **PRIMARY KEY**
  - incident_id: **FOREIGN KEY** referencing `id` in `incident_reports`
  - emplotee_id: **FOREIGN KEY** referencing `id` in `employee_records`
- facility_access_logs:
  - id: **PRIMARY KEY**
  - employee_id: **FOREIGN KEY** referencing `id` in `employee_records`
- computer_access_logs:
  - id: **PRIMARY KEY**
  - employee_id: **FOREIGN KEY** referencing `id` in `employee_records`
- keycard_access_logs:
  - id: **PRIMARY KEY**
  - employee_id: **FOREIGN KEY** referencing `id` in `employee_records`
- email_logs:
  - id: **PRIMARY KEY**
  - sender_employee_id: **FOREIGN KEY** referencing `id` in `employee_records`
  - recipient_employee_id: **FOREIGN KEY** referencing `id` in `employee_records`

<img src='/assets/images/articles/sqlnoir_case4/schema.png' alt='case4_schema'>

## Investigation

We start by looking through all the crime scenes where the `location` has QuantumTech.

```sql
select * from incident_reports where location like '%QuantumTech%';
```

> Prototype destroyed; data erased from servers.

New **clue**:
- Incident happened on *April 21, 1989*

Let us also look at witness statements for this crime. We can do this by using a `JOIN` on `incident_reports` and `witness_statements` tables.

```sql
select witness_statements.id, witness_statements.statement from witness_statements 
join incident_reports on witness_statements.incident_id = incident_reports.id 
where location like '%QuantumTech%';
```

> I heard someone mention a server in Helsinki.

> I saw someone holding a keycard marked QX- succeeded by a two-digit odd number.

New **clues**:
- Server in Helsinki mentioned
- Keycard marked QX- succeeded by a two-digit odd number

Using these clues we can find employees that access both the server and facility.

```sql
select * from employee_records 
where id in 
  (
    select employee_id from keycard_access_logs 
    where keycard_code like '%QX-0__' and 
    SUBSTR(keycard_code, -1, 1) in ('1', '3', '5', '7', '9') and 
    access_date = 19890421
) and 
id in 
  (
    select employee_id from computer_access_logs 
    where server_location = 'Helsinki' and 
    access_date = 19890421
);
```

| id | employee_name | department | occupation |
|----|----|----|----|
| 99 | Elizabeth Gordon | Engineering | Solutions Architect |

Only one name pops up. Let's take a look at the email logs either to or from this person.

```sql
select * from email_logs 
where sender_employee_id = 99 or 
recipient_employee_id = 99;
```

Just 1 email recieved where the sender employee id is 263. Let's follow this trail.

```sql
select * from email_logs 
where sender_employee_id = 263 or 
recipient_employee_id = 263;
```

> L’s schedule puts her close enough, but we need her inside F18 before 9. Trigger a minor alert or routine checkup to send her in by 8:30. Make sure she logs the visit. That part matters.

> Unlock 18 quietly by 9. He’ll use his own credentials to access it shortly after L leaves. No questions. Just ensure the timing lines up. The trail will lead exactly where it needs to.

Reading the first email it looks like someone is trying to frame Elizabeth Gordon. The send email will help us get to the actual culprit. Let's look at facility logs for facility 18.

```sql
select * from facility_access_logs where facility_name = 'Facility 18';
```

Only two people accessed this facility in the morning. Elizabeth and an employee with id 297. That must be our guy.

```sql
select * from employee_records where id = 297;
```

> Hristo Bogoev, Principal Engineer

We got him. At QuantumTech, the real glitch was human.

----

Thank you [Chris](https://github.com/hristo2612) for creating [SQL Noir](https://www.sqlnoir.com/).
