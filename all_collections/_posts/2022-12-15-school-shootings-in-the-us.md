---
layout: post
title: School Shootings in the US
date: 2022-12-15
tags: Project
author: Atharva Bhagwat
logo: "images/logo/nohello.png"
---

## Introduction
United states is one of the most diverse and multi-cultural places in the world. It is home to approximately 332 million, of which more than 25% are people under 17 years of age.

When compared to other countries, the US has a ratio of 120.5 firearms per 100 residents, up from 88 per 100 in 2011, highest among that of other countries around the world.

With increasing number of deaths among people under 17 due to gun violence, schools are eager to find ways to better protect their students. But the steps they are taking like clear bag packs(no bag packs in some cases), risk reinforcing an unhealthy culture of surveillance without actually preventing violence. With recent legislation pushing for gun control within US, we would like to answer questions based on the K-12 school shooting database.

Purpose of the project is to look into K-12 school shooting dataset and perform exploratory analysis using visualization techniques in answering potential questions that lawmakers will be interested in, and provide a factual report of these incidents and make this information easily available and understandable.

Getting a better grasp of school shootings, as challenging as it might be, is a clear priority for preventing harm and disruption for kids, staff, and families.

We would like to start with the number of K-12 schools in the US where school shooting has occurred, by year, with respect to number of victims, analyse patterns across seasons, quarters, and geographical locations.

## About the Data

**Source:** Riedman, David (2022). [K-12 School Shooting Database](https://k12ssdb.org/all-shootings).

**Description:**

K-12 School Shooting Database is an open source database launched and managed by David Riedman in 2018. 

The data consists of all incidents from 1970 to 2022 and is consistently updated. The dataset is divided in to 4 tables: Incident, Shooter, Victim, and Weapon. 

We are using subsets of the incident, weapon, and shooter data tables to generate visualization and answer our questions.

Subset of indicent table has 2171 entries and 19 columns. All tables have features with missing values, this will be handled during the data analysis phase.

## Incident Table

The table contains 2171 incidents from year 1970 to 2022.

Out of all the features in the incident table, analysis focuses on:
- Measures like `victims killed`, `wounded`, and `total number of victims`
- Time series data like `date` and `quarter`
- Geographical information like `state`

## Weapon Table

The original data containted a lot of empty values in the `Weapon_Type` column. We filled this with label `unknown`.

## Shooter Table

The `Age` column in this table consists of `string` data, like: Adult and `integer` data like, 17. While data cleaning, these values were grouped into the following bins:
- 0-12
- 13-17
- 18-21
- 22-30
- 31-50
- 50+

The missing values in the gender column were set to `unknown`.

## More Frequent...

In the last decade, school schootings have become a frequent occuring and have been in the news regularly. This motivated us to begin our exploratory data analysis with a time series of the number of incidents in last 50 years in the US to understand how much things have changed. We used the incident table which has shooting incident records from 1970 till now.

<div id='plot1'>
</div>

<script>
  var div = d3.select("plot1");
  div.append(plot1())
</script>