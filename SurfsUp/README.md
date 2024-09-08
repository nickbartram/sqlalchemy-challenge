# README for Module 10 Challenge (sqlalchemy-challenge)

## Introduction

This challenge involves planning for a ficitonal holiday to Hawaii. It is a climate analysis of the area to help with trip planning. 

## Data

The data is comprised of two CSV files (hawaii_measurements.csv, hawaii_stations.csv) as well as an SQLITE file (hawaii.sqlite). The files contain weather information about different stations across Hawaii.

## Methodology

For this challenge SQLAlchemy is used to examine the SQLITE file. SQLAlchemy provides an ORM (Object-Relational Mapping) system that allows Python applications to interact with SQL databases using Python objects, rather than writing raw SQL queries directly. 

Matplotlib is also used to plot the results of the SQLALchemy queries.

Finally FLASK is used to create a local API that can be used to view results of the aforementioned queries.

## Results

The results show the distribution of rainfall and temperatures over the course of a single year. 

## Conclusion

Based on this analysis Hawaii is a warm place: the distribution of temperatures over the course of a single year skews right towards the warmer side. This is a predictable outcome. The analysis also shows a fairly stochastic distribution of rainfall across a single year; the rainfall is fairly evenly distributed across the year with some peaks around September, February, and April. It might be best to travel in late fall or early winter to avoid heavy rainfall. 

## References

Class materials were used extensively for this assignment, as well as:

* stackoverflow.com
* Xpert Learning Assistant
* ChatGPT.com

## Usage

The FLASK app requires copy and pasting routes from the homepage into the url manually.
