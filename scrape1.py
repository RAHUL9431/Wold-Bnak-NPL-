import requests
from bs4 import BeautifulSoup
import csv

# specify the URL of the webpage to be scraped
url = "https://projects.worldbank.org/en/projects-operations/projects-list"

# send a GET request to the URL and store the response
response = requests.get(url)

# parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# find the project data table
table = soup.find('table', {'class': 'projectList'})

# create a new CSV file for storing the project data
with open('world_bank_projects.csv', mode='w', newline='') as csv_file:
    # create a CSV writer object
    writer = csv.writer(csv_file)

    # write the header row
    writer.writerow(['Title', 'Status', 'Sector', 'Project ID', 'Country', 'Approval Date', 'Closing Date', 'Total Cost', 'Financing Type', 'Implementing Agency'])

    # extract the project information from each row in the table and write to CSV
    for row in table.find_all('tr')[1:]:
        # extract project data
        title = row.find('td', {'class': 'projectTitle'}).text.strip()
        status = row.find('td', {'class': 'status'}).text.strip()
        sector = row.find('td', {'class': 'sector'}).text.strip()
        project_id = row.find('td', {'class': 'projectNumber'}).text.strip()
        country = row.find('td', {'class': 'country'}).text.strip()
        approval_date = row.find('td', {'class': 'approvalDate'}).text.strip()
        closing_date = row.find('td', {'class': 'closingDate'}).text.strip()
        total_cost = row.find('td', {'class': 'totalCost'}).text.strip()
        financing_type = row.find('td', {'class': 'financingType'}).text.strip()
        implementing_agency = row.find('td', {'class': 'implementingAgency'}).text.strip()

        # write the project data to CSV
        writer.writerow([title, status, sector, project_id, country, approval_date, closing_date, total_cost, financing_type, implementing_agency])

print("Project data saved to world_bank_projects.csv")
