---
layout: post
title: School Shootings in the US
categories: projects
permalink: projects/school-shootings
author: Atharva Bhagwat
---

## Introduction

United states is one of the most diverse and multi-cultural places in the world. It is home to approximately 332 million, of which more than 25% are people under 17 years of age.

When compared to other countries, the US has a ratio of 120.5 firearms per 100 residents, up from 88 per 100 in 2011, highest among that of other countries around the world.

With increasing number of deaths among people under 17 due to gun violence, schools are eager to find ways to better protect their students. But the steps they are taking like clear bag packs(no bag packs in some cases), risk reinforcing an unhealthy culture of surveillance without actually preventing violence. With recent legislation pushing for gun control within US, we would like to answer questions based on the K-12 school shooting database.

Purpose of the project is to look into K-12 school shooting dataset and perform exploratory analysis using visualization techniques in answering potential questions that lawmakers will be interested in, and provide a factual report of these incidents and make this information easily available and understandable.

Getting a better grasp of school shootings, as challenging as it might be, is a clear priority for preventing harm and disruption for kids, staff, and families.

We would like to start with the number of K-12 schools in the US where school shooting has occurred, by year, with respect to number of victims, analyse patterns across seasons, quarters, and geographical locations.

## About the Data

**Source:** [K-12 School Shooting Database](https://k12ssdb.org/all-shootings). Riedman, David (2022).

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

## More Frequent

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

## What weapons are the most common?

<div id='piechart_legend'>
</div>

**States with highest number of incidents**

<div id='piechart_high'>
</div>

**States with lowest number of incidents**

<div id='piechart_low'>
</div>

Taking a look at the distribution of weapons used in states with the highest and the lowest number of incidents after the year 2000 and dig deeper by looking into the state gun laws. We use a pie chart to visualize this information between the two groups of interest.

Looking at the visualization, *handguns*, followed by *rifles* are the top 2 types of weapons used across states with the highest incidents. Interestingly, *rifles* are not involved in states with lower number of incidents.

While there are one or two incidents where a *rifle* or *multiple rifles* were used, the number of casualties in these case is extremely high. Looking at the visualization below, we can see this in the state of Texas, while there was only one incident where *multiple rifles* were used, the number of deaths in that event contributes nearly to a **quarter** of the total deaths in the state. We see similiar cases in other states with higher number of incidents, like California and Florida.

### Victims Killed vs Weapon Used

<div id='killed_vs_weapon_legend'>
</div>
<div id='killed_vs_weapon'>
</div>

## How old?

<div id='age_legend'>
</div>
<div id='age'>
</div>

After looking at what weapons are used, we now look into who uses them. To get a closer look, the gender of the shooters and to which age group they belong to are visualized. We grouped the ages into six categories: 0-12, 13-17, 18-21, 22-30, 31-50, and 50+ years.

It is highly evident that majority of the shooters were male. The age category of 13-17 cause most number of incidents followed by 18-21 age category. Even among the female gender, we observe age category of 13-17 contribute the highest to the total number of incidents.

This raises concern for school authorities. There can be some psychological reason for that to happen. Our dataset contained two possible reasons namely Domestic Abuse or Bullying. We found these incidents to be not related to them. No domestic violence was found for 1892 incidents out of the total incidents, while 1771 indicated no bullying. So there can be some other reasons, which are not present in our dataset.

## Gun Laws

To make sense of access to the weapons used, we refer to gun laws in states with the highest and lowest incidents.

All states in top 5 except for California and Illinois have little to no restrictions on sales of weapon type, magazine size, and necessity of background checks. Texas is the only state to have *campus carry*. Campus carry is allows carrying of guns in parking lots, outdoor walkways on campus, and concealed carry in campus buildings.

While some states with least amount of incidents have little to no restrictions, their low number of incidents can be because of extremely low population in these states. States like Hawaii, Idaho, and West Virginia have population less than 2 million, where as North Dakota has population of about 750k and the US Virgin Islands have the least population, around 110k.

In addition to having low population, the state of Hawaii also has stricter gun laws.

## Do we see a pattern?

<div id='trend_legend'>
</div>
<div id='trend'>
</div>

To uncover seasonality trends, we were interested into seeing what quarter of the year has the most number of incidents. For this, we use a line chart highlighting the last 5 years and plotting number of incidents over quarters.

We observed a couple of things:

- There has been a tremendous increase in number of incidents in last 5 years.
- All years have higher number of incidents in Fall.

## Conclusion

While most states have an age limit of 18 to purchase weapons, We observed that the shooters aged 13-17 contribute the highest. Since they can't legally buy a weapon, one possible measure is to increase **safe keeping of guns** among adults. Gun safe keeping programs can also be mandated when one purchases a weapon.

In addition to this, increasing the age limit for purchasing weapons to 21 will benefit, as the age range 18-21 has the 2nd highest amount of shooters.

States with no laws restricting access to rifles leads to incidents with higher casualties. Restricting access to automatic rifles, in
all states will significantly reduce the number of fatalities.

Since there are a lot of *unknowns* in the weapon type feature of the weapons' table, reducing this could help us uncover patterns.

Looking into the possibility of psychological reasons, we analysed two features from the incident table, namely *Domestic Abuse* and *Bullied*. No domestice violence was found for 87% of 2171 total incidents, while 81% indicated no bullying. So there can be many other factors that can be the causes. States should focus on helping schools build a safe space for students to open up about their problems and anxieties and take necessary steps to help them.

These incidents are rising at an alarming rate and have happened in every part of the country. From our analysis, we infer that,there is no single reason which cause school shootings and we believe there cannot be any one single solution that is going to address this problem.

----

<script>
  plot1();
  const plot2_legend = {Injuries: '#fed976', Deaths: '#b10026'};
  colorize(plot2_legend, 'injuried_death_ratio_legend');
  plot2();
  plot3();
  plot4();
  plot5();
  const plot678_legend = {Unknown: 'lightgray', Handgun: '#377eb8', Other: '#4daf4a', Rifle: '#984ea3', 'Multiple Handguns': '#ff7f00', 'Multiple Rifles': '#ffff33', Shotgun: '#e41a1c'};
  colorize(plot678_legend, 'piechart_legend');
  colorize(plot678_legend, 'killed_vs_weapon_legend');
  plot678();
  const age_legend = {Unknown: "#1f77b4", Male: "#ff7f0e", Female: "#2ca02c", Transgender: "#d62728"};
  colorize(age_legend, 'age_legend');
  plot9();
  const trend_legend = {2018: "#1f77b4", 2019: "#ff7f0e", 2020: "#2ca02c", 2021: "#d62728", 2022: "#9467bd"};
  colorize(trend_legend, 'trend_legend');
  plot10();
</script>
