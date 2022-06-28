
/*
Covid 19 Data Exploration 
Skills used: Joins, CTE's, Temp Tables, Windows Functions, Aggregate Functions, Creating Views, Converting Data Types
Software used: DBeaver Universal Database Manager
*/

-- View data by location, date
SELECT *
FROM CovidDeaths_csv cdc 
order by 3, 4

-- Select data that we are going to be using

SELECT Location, date, total_cases, new_cases, total_deaths, population 
FROM CovidDeaths_csv cdc
order by 1, 2

-- Looking at total cases vs total deaths in the United States

SELECT Location, date, total_cases, total_deaths, Cast(total_deaths AS REAL) / total_cases * 100 as death_percentage
FROM CovidDeaths_csv cdc
WHERE location == 'United States'
order by 1, 2

-- Looking at total cases vs total deaths in countries only

SELECT location, MAX(CAST(total_deaths as INT)) as total_death_count
FROM CovidDeaths_csv cdc 
WHERE continent is not ''
Group by location
order by total_death_count DESC 

-- Showing contintents with the highest death count per population

SELECT continent, MAX(CAST(total_deaths as INT)) as total_death_count
FROM CovidDeaths_csv cdc 
WHERE continent is not ''
Group by continent
order by total_death_count DESC 

-- GLOBAL NUMBERS

SELECT SUM(new_cases) as total_cases, SUM(CAST(new_deaths as INT)) as total_deaths, SUM(CAST(new_deaths as INT))/SUM(New_Cases)*100 as death_rate
FROM CovidDeaths_csv cdc
WHERE continent is not ''
order by 1,2
