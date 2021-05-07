import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# This script scrapes job postings from workopolis.com and compiles
# results into a CSV file

# gets an url based on position and location
def get_url(position, location):
    template = "https://www.workopolis.com/jobsearch/find-jobs?ak={}&l={}"
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    url = template.format(position, location)
    return url

# extract job data from a single record
def get_record(card):
    atag = card.h2
    job_title = atag.get('title')
    job_url = 'https://www.workopolis.com' + atag.find('a')['href']

    company = card.find('div', 'JobCard-property').text.strip()
    job_location = card.find('span', 'JobCard-property').text.strip()
    job_location = job_location[2:]
    job_summary = card.find('div', 'JobCard-snippet').text.strip()

    today = datetime.today().strftime('%Y-%m-%d')

    record = (job_title, company, job_location, today, job_summary, job_url)
    return record

# creates the list of job openings
def main(position, location):
    records = []
    url = get_url(position, location)

    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('article', 'JobCard')
        for card in cards:
            record = get_record(card)
            records.append(record)
        try:
            url = 'https://www.workopolis.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break

    with open('workopolis-results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['JobTitle', 'Company', 'Location', 'ExtractDate', 'Summary', 'JobUrl'])
        writer.writerows(records)

# select the position and location desired
main('software developer intern', 'toronto on')
