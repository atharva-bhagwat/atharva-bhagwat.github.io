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

<div id='incident_over_time'>
</div>

We notice a rising trend in the number of shootings over the years which is almost 1200% increase in five decades. Where in during the 70s the yearly shooting occurrence was as low as 20, to the current time where it is almost 260 yearly. We notice a jump in the number of incidents after 2015 where it has increased almost 4 times.

## ...and Deadlier


<div id='injuried_death_ratio_legend'>
</div>

<div id='injuried_death_ratio'>
</div>

We focus on the incidents in the 21st century and look at how the number of injuries and deaths has changed over the years. We use a stacked bar chart to better show both number of injuries and deaths in a year. From the graph above we can see an overview of the injuries and deaths ratio, where injuries are more than deaths however we notice that the death to injury ratio was higher in 2012 compared to the rest of the years. Looking at the data of 2012, the Sandy Hook Elementary School incident led to over 25 deaths and is more likely to have skewed the ratio.

Looking at the last 5 years, we see not only the number of incidents which has gone up, but also the number of deaths have increased.

## Is it the same for everywhere?

<div id='statewise'>
</div>

Now lets see the state-wise spread of indicidents over the years. To visualize this we used a spike map. Here the length of the spike shows the number of total shooting incidents. As we can observe states like California, Texas, Florida have highest number of incidents followed by Illinois, Michigan, Pennsylvania, Ohio and New York.

On paper these states can also be classified highly populated states, so one might believe thats the reason for the high incident count. California is the most populated state followed by Texas, Florida, New York. These states rank in the top 10 states in terms of population. But, when we look ar population density, these states fall down rank. New Jersey which ranks 2nd in population density has very less shooting incidents (21 incidents) as compared to its neighbour New York (83 incidents). So high population cannot be the sole factor for the incident counts across the states.

Since, we cant generalize the occurences of incidents across all states, we delve further and look at the spread of incidents for each state across the timespan from 1970 to 2022. We can use a heatmap to visualize as it help compare all the states with each other using a sequential color scale.

<div id='heatmap_legend'>
</div>
<div id='heatmap'>
</div>

As we notice, this visualization is highly similar to the cumulative incident distribution over the years we see initially. There seems to a sharp increase in number of incidents after 2015 across most of the states, denoted by a orange to dark-red shades in the right side of the visualization. Large number of white spaces in heatmap signifies that there is little to no incidents for majortiy of the states for large number of years. 

This motivates us to understand recent trends inorder to correlate with current state laws. Hence we shift our focus only to incident occurence after the year 2000. Interesting patterns arise when we inspect state-wise breakdown of data from year 2000. States like California, Texas, Illinois, Florida, Pittsburgh, Ohio has seen higher incidents when compared to rest of the country, with California topping the list five times over the last 6 years. Average number of incidents across the top 5 states over the last 22 years seems to over 7. Sadly, there has been only 15 occurences where the top 5 states didnt have a single incident for an entire year over the last 22 years. Illinois has also the highest number of incidents in the recent years, which motivates us further to focus on this group of states. 

If we look at the other end of the spectrum, States like Hawaii, Idaho, North Dakota, US Virgin Islands, West Virginia has low incident count with an average incident occurence of 3.8 per years over the last 22 years. Hence, we decide to compare on these two groups of state in our analysis further.

<div id='heatmap_small_legend'>
</div>
<div id='heatmap_small'>
</div>

<script>
  plot1();
  var plot2_legend = {Injuries: '#fed976', Deaths: '#b10026'};
  colorize(plot2_legend, 'injuried_death_ratio_legend');
  plot2();
  plot3();
  plot4();
  plot5();
</script>

