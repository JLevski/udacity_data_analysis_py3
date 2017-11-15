import numpy as np
import pandas as pd
import seaborn as sns

# Dataframes would be more appropriate for this data, but this lesson only
# covers series so I have focussed on that


male_completion = pd.read_csv('male_completion_rate.csv', index_col='Country')
gdp_per_cap = pd.read_csv('gdp_per_capita.csv', index_col='Country')
female_completion = pd.read_csv('female_completion_rate.csv',
                                index_col='Country')
life_expect = pd.read_csv('life_expectancy.csv', index_col='Country')
employment_above_15 = pd.read_csv('employment_above_15.csv',
                                  index_col='Country')

focus_year = '2007'
focus_country = 'United States'

male_completion_year = male_completion[focus_year]
female_completion_year = female_completion[focus_year]
employment_year = employment_above_15[focus_year]
life_expect_year = life_expect[focus_year]
gdp_per_cap_year = gdp_per_cap[focus_year]


male_completion_country = male_completion.loc[focus_country]
female_completion_country = female_completion.loc[focus_country]
employment_country = employment_above_15.loc[focus_country]
life_expect_country = life_expect.loc[focus_country]
gdp_per_cap_country = gdp_per_cap.loc[focus_country]


def max_employment_year(employment):
    '''
    Returns name of the country with highest employment in employment data, and
    the employment in that country
    '''
    max_country = employment.argmax()
    max_value = employment.max()
    return (max_country, max_value)


print(max_employment_year(employment_year))


def overall_completion_rate(female_completion, male_completion):
    '''
    Fill in this function to return a NumPy array containing the overall
    school completion rate for each country. The arguments are NumPy
    arrays giving the female and male completion of each country in
    the same order.
    '''
    return (male_completion + female_completion) / 2.


print(overall_completion_rate(female_completion_year, male_completion_year))


# def standardize_data(values):
#     value = values[0]
#     standardized_value = (values - values.mean()) / values.std()
#     return standardized_value
