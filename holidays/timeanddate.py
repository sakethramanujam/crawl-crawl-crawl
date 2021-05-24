#!/usr/bin/env python3
import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
import argparse


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-y", "--year", help="Year for which data is to be generated", type=int
    )
    parser.add_argument("-p", "--path", help="Path to store the file", type=str)
    args = parser.parse_args()
    return args


def holidays_timeanddate(year):
    url = f"https://www.timeanddate.com/holidays/india/{year}"
    headers = {"Accept-Language": "en-US,en;q=0.5"}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    trs = soup.find_all("tr", {"data-date": True})
    months = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }
    holidays = []
    for tr in trs:
        date, month = tr.find("th").text.split()
        date = int(date)
        month = months[month]
        tds = tr.find_all("td")
        holiday = {
            "date": f"{year}-{month:02d}-{date:02d}",
            "day": tds[0].text,
            "holiday": tds[1].text,
            "holiday_type": tds[2].text,
        }
        holidays.append(holiday)
    return holidays


def generate_dataset_timeanddate(year: str, path: str):
    yearly = holidays_timeanddate(year)
    df = pd.DataFrame(yearly)
    filename = os.path.join(path, f"{year}_timeanddate.csv")
    df.to_csv(filename, index=False)


def main():
    """
    usage
    ---
    python timeanddate.py -y <year> -p <path>
    """
    year = args().year
    path = args().path
    print(" Fetching list of Holidays for the year: ", year)
    generate_dataset_timeanddate(year=year, path=path)
    print(f"Holiday Dataset for the year {year} generated!")


if __name__ == "__main__":
    main()
