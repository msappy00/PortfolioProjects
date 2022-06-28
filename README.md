# PortfolioProjects
A set of projects to showcase what I'm learning in the field of data analysis.
The end in mind is to contribute to an opensource project or find employment as a data analyst.

1) COVID Data Exploration (SQL Data Exploration)

This first of these projects is built from https://github.com/AlexTheAnalyst/PortfolioProjects
and a Youtube course taught by Alex at https://www.youtube.com/watch?v=qfyynHBFOsM&list=PLUaB-1hjhk8H48Pj32z4GZgGWyylqv85f

My code differs from the original in the following ways:
* I'm using DBeaver Universal Database Manager instead of Microsoft SQL Server
* I took the dataset about a year after the original project, so some of the queries had to be adjusted for value size.
* For example: when converting columns to integers some values now exceed the max int value (2,147,483,647). Those values need to be converted to "bigint" instead of "int".
* The file size for the csv file CovidVaccinations.csv exceeds the 25MB limit set by github, so I've only uploaded the two .xlsx files

The COVID dataset was taken from https://ourworldindata.org/covid-deaths


These are courses linked to in the Youtube playlist. I've tagged each with my progress.

Coursera Courses (https://www.coursera.org):
* (auditing in progress) Google Data Analyst Certification
* (not yet attempted) Data Analysis with Python
* (not yet attempted) IBM Data Analysis Specialization
* (not yet attempted) Tableau Data Visualization

Udemy Courses (https://www.udemy.com):
* (not yet attempted) Python for Data Analysis and Visualization
* (not yet attempted) Statistics for Data Science
* (not yet attempted) SQL for Data Analysts (SSMS)
* (not yet attempted) Tableau A-Z
