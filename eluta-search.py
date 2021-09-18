import csv
import requests
from bs4 import BeautifulSoup

# This script scrapes job postings from eluta.ca and compiles
# results into a CSV file

# gets an url based on position and location
def get_url(position, location):
    template = "https://www.eluta.ca/search?q={}&l={}"
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    url = template.format(position, location)
    return url

# extract job data from a single record
def get_record(card):
    atag = card.h2
    try:
        job_title = atag.find('a', 'lk-job-title').text
    except AttributeError:
        job_title = ''
    try:
        job_url = 'https://www.eluta.ca' + atag.find('a')['onclick'][14:-2]
    except AttributeError:
        job_url = ''
    try:
        company = card.find('a', 'employer').text.strip()
    except AttributeError:
        company = ''
    try:
        job_location = ' '.join(card.find('span', 'location').text.strip().split())
    except AttributeError:
        job_location = ''
    try:
        job_summary = card.find('span', 'description').text.strip()[3:]
    except AttributeError:
        job_summary = ''
    try:
        post_date = card.find('a', 'lk').text
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
        cards = soup.find_all('div', 'organic-job')
        for card in cards:
            record = get_record(card)
            records.append(record)
        try:
            url = 'https://www.eluta.ca' + soup.find('a', {'id': 'pager-next'}).get('href')
        except AttributeError:
            break

    with open('eluta-results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Job Title', 'Company', 'Location', 'Posted', 'Summary', 'Job URL'])
        writer.writerows(records)

# select the position and location desired
main('software developer intern', 'toronto on')
