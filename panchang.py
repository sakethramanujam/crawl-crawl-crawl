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

def holidays_panchang(year):
    url = f'https://panchang.astrosage.com/calendars/indiancalendar?language=en&date={year}'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all("div", class_="pan-row")
    tables = soup.find_all("table")
    months = {
        "January": 1,
        "February": 2,
        "March": 3, 
        "April": 4,
        "May": 5,
        "June":6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }
    legend = {}
    holidays = []
    for row in rows:
        bs = row.find_all("b") 
        for b in bs:
            legend[b["style"]] = b.text.rstrip()[2:]
    for table in tables:
        month = table.find("thead").find('tr').find('th').text.split()[0]
        if month not in months:
            continue
        month = months[month]
        trs = table.find("tbody").find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            date, day = tds[0].text.split()
            date = int(date)
            links = tds[1].find_all('a', style=True)
            links.extend(tds[1].find_all('b', style=True))
            for link in links:
                holiday = {'date': f'{year}-{month:02d}-{date:02d}',
                            'day': day,
                            'holiday': link.text,
                            'holiday_type': legend[link['style']]
                            }
                holidays.append(holiday)
    return holidays

def generate_dataset_panchang(year: str, path: str):
    yearly = holidays_panchang(year)
    df = pd.DataFrame(yearly)
    filename = os.path.join(path, f"panchang_{year}.csv")
    df.to_csv(filename, index=False)

def main():
    '''
    usage
    ---
    python panchang.py -y <year> -p <path>
    '''
    year = args().year
    path = args().path
    print(" Fetching list of Holidays for the year: ", year)
    generate_dataset_panchang(year=year, path=path)
    print(f'Holiday Dataset for the year {year} generated!')


if __name__ == "__main__":
    main()
