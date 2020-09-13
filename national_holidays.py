# !usr/bin/env python3
import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
import argparse


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--year',
                        help='Year for which data is to be generated', type=int)
    parser.add_argument(
        '-p', '--path', help='Path to store the file', type=str)
    args = parser.parse_args()
    return args


def monthly_holidays(year, month):
    url = f'http://www.india.gov.in/calendar?date={year}-{month}'
    print(f"Currently Parsing:{url}")
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    tbody = soup.find('tbody')
    try:
        tds = tbody.find_all('td')
    except AttributeError as e:
        raise Exception("This is too early to fetch those Holidays, try again in an year!")
    holidays = []
    for td in tds:
        if td.find('div', attrs={'class': 'item'}) is not None:
            if td.find('div', attrs={'class': 'greenCal'}):
                name = td.find('div', attrs={'class': 'greenCal'}).contents[0]
                holiday = {'date': td['data-date'],
                           'day': td['headers'][0],
                           'holiday': name,
                           'holiday_type': 'Restricted'
                           }
                holidays.append(holiday)
            elif td.find('div', attrs={'class': 'redCal'}):
                name = td.find('div', attrs={'class': 'redCal'}).contents[0]
                holiday = {'date': td['data-date'],
                           'day': td['headers'][0],
                           'holiday': name,
                           'holiday_type': 'Gazetted'
                           }
                holidays.append(holiday)
    return holidays


def generate_dataset(year: str, path: str):
    months = ["{:02d}".format(i) for i in range(1, 13)]
    holidays = []
    for month in months:
        holidays.append(monthly_holidays(year, month))
    yearly = [holiday for monthly in holidays for holiday in monthly]
    df = pd.DataFrame(yearly)
    filename = os.path.join(path, f"{year}.csv")
    df.to_csv(filename, index=False)


def main():
    '''
    usage
    ---
    python national_holidays.py -y <year> -p <path>
    '''
    year = args().year
    path = args().path
    print(" Fetching list of Holidays for the year: ", year)
    generate_dataset(year=year, path=path)
    print(f'Holiday Dataset for the year {year} generated!')


if __name__ == "__main__":
    main()
