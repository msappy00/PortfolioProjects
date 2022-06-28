
/*
Covid 19 Data Exploration 
Skills used: Joins, CTE's, Temp Tables, Aggregate Functions, Creating Views, Converting Data Types
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
WHERE continent is not null
Group by location
order by total_death_count DESC 

-- Showing continents with the highest death count per population

SELECT continent, MAX(CAST(total_deaths as INT)) as total_death_count
FROM CovidDeaths_csv cdc 
WHERE continent is not null
Group by continent
order by total_death_count DESC 

-- GLOBAL NUMBERS

SELECT SUM(new_cases) as total_cases, SUM(CAST(new_deaths as INT)) as total_deaths, SUM(CAST(new_deaths as INT))/SUM(New_Cases)*100 as death_rate
FROM CovidDeaths_csv cdc
WHERE continent is not null
order by 1,2

-- Total Population vs Vaccinations
-- Shows Percentage of Population that has recieved at least one Covid Vaccine

Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CAST(vac.new_vaccinations as REAL)) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
From CovidDeaths_csv dea
Join CovidVaccinations_csv vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not ''
order by 2,3

-- Using Common Table Expression (CTE) to perform Calculation on Partition By in previous query

With PopvsVac (Continent, Location, Date, Population, New_Vaccinations, RollingPeopleVaccinated)
as
(
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CAST(vac.new_vaccinations as REAL)) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
From CovidDeaths_csv dea
Join CovidVaccinations_csv vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not ''
--order by 2,3
)
Select *, (RollingPeopleVaccinated/Population)*100
From PopvsVac

-- Using Temp Table to perform Calculation on Partition By in previous query

DROP Table if exists PercentPopulationVaccinated
Create Table PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric,
RollingPeopleVaccinated numeric
)

Insert into PercentPopulationVaccinated
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CAST(vac.new_vaccinations as REAL)) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
From CovidDeaths_csv dea
Join CovidVaccinations_csv vac
	On dea.location = vac.location
	and dea.date = vac.date

Select *, (RollingPeopleVaccinated/Population)*100
From PercentPopulationVaccinated

-- Creating View to store data for later visualizations

Create View PercentPopulationVaccinated as
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CAST(vac.new_vaccinations as REAL)) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
From CovidDeaths_csv dea
Join CovidVaccinations_csv vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not ''
