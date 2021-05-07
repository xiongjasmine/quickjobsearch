# This script was made following a YouTube tutorial from Izzy Analytics
# Link to his GitHub: https://github.com/israel-dryer/Indeed-Job-Scraper

import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# This script scrapes job postings from indeed.com and compiles
# results into a CSV file

# gets an url based on position and location
def get_url(position, location):
    template = "https://ca.indeed.com/jobs?q={}&l={}"
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    url = template.format(position, location)
    return url

# extract job data from a single record
def get_record(card):
    atag = card.h2.a
    job_title = atag.get('title')
    job_url = 'https://ca.indeed.com' + atag.get('href')

    company = card.find('span', 'company').text.strip()
    job_location = card.find('div', 'recJobLoc').get('data-rc-loc')
    job_summary = card.find('div', 'summary').text.strip()

    post_date = card.find('span', 'date').text
    today = datetime.today().strftime('%Y-%m-%d')

    record = (job_title, company, job_location, post_date, today, job_summary, job_url)
    return record

# creates the list of job openings
def main(position, location):
    records = []
    url = get_url(position, location)

    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', 'jobsearch-SerpJobCard')
        for card in cards:
            record = get_record(card)
            records.append(record)
        try:
            url = 'https://ca.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break

    with open('indeed-results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Job Title', 'Company', 'Location', 'Post Date', 'Extract Date', 'Summary', 'Job URL'])
        writer.writerows(records)

# select the position and location desired
main('software developer intern', 'toronto on')
