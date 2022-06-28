
/*
Covid 19 Data Exploration 
Skills used: Joins, CTE's, Temp Tables, Windows Functions, Aggregate Functions, Creating Views, Converting Data Types
*/

-- SELECT *
-- FROM CovidDeaths_csv cdc 
-- order by 3, 4

-- Select Data that we are going to be using

-- SELECT Location, date, total_cases, new_cases, total_deaths, population 
-- FROM CovidDeaths_csv cdc
-- order by 1, 2

-- Looking at Total Cases vs Total Deaths

-- SELECT Location, date, total_cases, total_deaths, Cast(total_deaths AS REAL) / total_cases * 100 as death_percentage
-- FROM CovidDeaths_csv cdc
-- WHERE location == 'United States'
-- order by 1, 2

SELECT location, MAX(CAST(total_deaths as INT)) as total_death_count
FROM CovidDeaths_csv cdc 
WHERE continent is ''
Group by location
order by total_death_count DESC 
