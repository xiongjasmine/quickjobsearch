import csv
import requests
from bs4 import BeautifulSoup

# This script scrapes job postings from indeed.com workopolis.com
# and compiles results into a CSV file

# gets an url based on position and location (Indeed)
def get_url(position, location):
    template = "https://ca.indeed.com/jobs?q={}&l={}"
    template = "https://ca.indeed.com/{}-jobs-in-{}"
    position = position.replace(' ', '-')
    location = location.replace(' ', '-')
    url = template.format(position, location)
    return url

# extract job data from a single record (Indeed)
def get_record(card):
    try:
        job_title = card.find('h2', 'jobTitle').text
        if job_title[0:3] == 'new':
            job_title = job_title[3:]
    except AttributeError:
        job_title = ''
    try:
        job_url = 'https://ca.indeed.com' + card.get('href')
    except AttributeError:
        job_url = ''
    try:
        company = card.find('span', 'companyName').text
    except AttributeError:
        company = ''
    try:
        job_location = card.find('div', 'companyLocation').text
    except AttributeError:
        job_location = ''
    try:
        job_summary = card.find('div', 'job-snippet').text.strip()
    except AttributeError:
        job_summary = ''
    try:
        post_date = card.find('span', 'date').text
    except AttributeError:
        post_date = ''

    record = (job_title, company, job_location, post_date, job_summary, job_url)
    return record

# creates the list of job openings
def main(position, location):
    records = []
    url = get_url(position, location)

    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('a', 'tapItem')
        for card in cards:
            record = get_record(card)
            records.append(record)
        try:
            url = 'https://ca.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break

    with open('indeed-results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Job Title', 'Company', 'Location', 'Posted', 'Summary', 'Job URL'])
        writer.writerows(records)

# select the position and location desired
main('software developer intern', 'toronto on')
