import pandas as pd
import sqlite3

# df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
df = pd.read_csv('Dashboard/covid_data.csv')
df.drop(columns=df.columns[0], axis=1, inplace=True)

# Create sqlite database and cursor
conn = sqlite3.connect('Dashboard/covid.db')
c = conn.cursor()
# Create the table of covid_data
c.execute("""CREATE TABLE IF NOT EXISTS covid_data (
            iso_code varchar(50),
            continent varchar(50),
            location varchar(50),
            date varchar(50),
            total_cases real,
            new_cases real,
            new_cases_smoothed real,
            total_deaths real,
            new_deaths real,
            new_deaths_smoothed real,
            total_cases_per_million real,
            new_cases_per_million real,
            new_cases_smoothed_per_million real,
            total_deaths_per_million real,
            new_deaths_per_million real,
            new_deaths_smoothed_per_million real,
            reproduction_rate real,
            icu_patients varchar(50),
            icu_patients_per_million varchar(50),
            hosp_patients varchar(50),
            hosp_patients_per_million varchar(50),
            weekly_icu_admissions varchar(50),
            weekly_icu_admissions_per_million varchar(50),
            weekly_hosp_admissions varchar(50),
            weekly_hosp_admissions_per_million varchar(50),
            total_tests varchar(50),
            new_tests varchar(50),
            total_tests_per_thousand varchar(50),
            new_tests_per_thousand varchar(50),
            new_tests_smoothed varchar(50),
            new_tests_smoothed_per_thousand varchar(50),
            positive_rate varchar(50),
            tests_per_case varchar(50),
            tests_units varchar(50),
            total_vaccinations varchar(50),
            people_vaccinated varchar(50),
            people_fully_vaccinated varchar(50),
            total_boosters varchar(50),
            new_vaccinations varchar(50),
            new_vaccinations_smoothed varchar(50),
            total_vaccinations_per_hundred varchar(50),
            people_vaccinated_per_hundred varchar(50),
            people_fully_vaccinated_per_hundred varchar(50),
            total_boosters_per_hundred varchar(50),
            new_vaccinations_smoothed_per_million varchar(50),
            new_people_vaccinated_smoothed varchar(50),
            new_people_vaccinated_smoothed_per_hundred varchar(50),
            stringency_index real,
            population real,
            population_density real,
            median_age real,
            aged_65_older real,
            aged_70_older real,
            gdp_per_capita real,
            extreme_poverty varchar(50),
            cardiovasc_death_rate real,
            diabetes_prevalence real,
            female_smokers varchar(50),
            male_smokers varchar(50),
            handwashing_facilities real,
            hospital_beds_per_thousand real,
            life_expectancy real,
            human_development_index real,
            excess_mortality_cumulative_absolute varchar(50),
            excess_mortality_cumulative varchar(50),
            excess_mortality varchar(50),
            excess_mortality_cumulative_per_million varchar(50)
            )""")
conn.commit()

df.to_sql('covid_data', conn, if_exists='append', index=False)
