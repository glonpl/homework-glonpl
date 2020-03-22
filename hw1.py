from typing import List
import pandas as pd
import datetime

CONFIRMED_CASES_URL = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
                      f"/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv "

"""
When downloading data it's better to do it in a global scope instead of a function.
This speeds up the tests significantly
"""
confirmed_cases = pd.read_csv(CONFIRMED_CASES_URL, error_bad_lines=False)


def poland_cases_by_date(day: int, month: int, year: int = 2020) -> int:
    """
    Returns confirmed infection cases for country 'Poland' given a date.

    Ex.
    >>> poland_cases_by_date(7, 3, 2020)
    5
    >>> poland_cases_by_date(11, 3)
    31

    :param year: 4 digit integer representation of the year to get the cases for, defaults to 2020
    :param day: Day of month to get the cases for as an integer indexed from 1
    :param month: Month to get the cases for as an integer indexed from 1
    :return: Number of cases on a given date as an integer
    """
    d=datetime.date(year,month,day)

    return confirmed_cases.loc[confirmed_cases["Country/Region"]=="Poland"][f"{d.month}/{d.day}/{d.year-2000}"].values[0]

    # poland=clean.loc[clean["Country/Region"]=='Poland']
    # print(poland)
    # Your code goes here (remove pass)



def top5_countries_by_date(day: int, month: int, year: int = 2020) -> List[str]:
    """
    Returns the top 5 infected countries given a date (confirmed cases).

    Ex.
    >>> top5_countries_by_date(27, 2, 2020)
    ['China', 'Korea, South', 'Cruise Ship', 'Italy', 'Iran']
    >>> top5_countries_by_date(12, 3)
    ['China', 'Italy', 'Iran', 'Korea, South', 'France']

    :param day: 4 digit integer representation of the year to get the countries for, defaults to 2020
    :param month: Day of month to get the countries for as an integer indexed from 1
    :param year: Month to get the countries for as an integer indexed from 1
    :return: A list of strings with the names of the coutires
    """
    d=datetime.date(year,month,day)
    return list(confirmed_cases.groupby(["Country/Region"]).sum().sort_values(by=[f"{d.month}/{d.day}/{d.year-2000}"],ascending=False).head(5).index)

def top5_countries_by_date_prove_me_Im_wrong(day: int, month: int, year: int = 2020) -> List[str]:
    d=datetime.date(year,month,day)
    return list(confirmed_cases.groupby(["Country/Region"])[d.strftime('%m/%d/%y').lstrip("0").replace(" 0", " ").replace("/0", "/")].sum().groupby("Country/Region").cumsum().sort_values(ascending=False).head(5).index) #tests doesn't pass somehow



def no_new_cases_count(day: int, month: int, year: int = 2020) -> int:
    """
    Returns the number of countries/regions where the infection count in a given day was the same as the previous day.
    Ex.
    >>> no_new_cases_count(11, 2, 2020)
    35
    >>> no_new_cases_count(3, 3)
    57
    :param day: 4 digit integer representation of the year to get the cases for, defaults to 2020
    :param month: Day of month to get the countries for as an integer indexed from 1
    :param year: Month to get the countries for as an integer indexed from 1
    :return: Number of countries/regions where the count has not changed in a day
    """

    today = datetime.date(day=day,month=month,year=year)
    yesterday = today + datetime.timedelta(days=-1)
    today=today.strftime('%-m/%-d/%y')
    yesterday=yesterday.strftime('%-m/%-d/%y')
    to_check= confirmed_cases.get([yesterday,today])
    count = 0
    size_range=confirmed_cases.shape[0]
    for i in range(0 , size_range):
        if to_check.loc[i][0]!=0: #doesn't seem to be needed according to task... but the example values
            if to_check.loc[i][0].item()==to_check.loc[i][1].item():
                count += 1
                #print(to_check.loc[i],count) #debug
    return count

def no_new_cases_count_prove_me_Im_wrong(day: int, month: int, year: int = 2020) -> int:
    today = datetime.date(day=day,month=month,year=year)
    yesterday = (today + datetime.timedelta(days=-1)).strftime('%-m/%-d/%y')
    today=today.strftime('%-m/%-d/%y')
    to_check= confirmed_cases.get([yesterday,today])
    count = 0
    size_range=confirmed_cases.shape[0]
    for i in range(0 , size_range):
        if to_check.loc[i][0]!=0: #this if statement doesn't seem to be needed according to task... but the example values...
            if to_check.loc[i][0].item()==to_check.loc[i][1].item():
                count += 1
                #print(to_check.loc[i],count) #debug
    return count
