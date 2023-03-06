import requests
from bs4 import BeautifulSoup
import csv

# Make a GET request to the website and get the HTML content
response = requests.get("https://projects.worldbank.org/en/projects-operations/projects-home")
soup = BeautifulSoup(response.content, "html.parser")

# Create a CSV file to store the project information
with open("world_bank_projects.csv", mode="w", newline="", encoding="utf-8") as csv_file:
    # Create a CSV writer object
    writer = csv.writer(csv_file)

    # Write the header row
    writer.writerow(
        ["Project ID", "Project Name", "Status", "Sector", "Total Cost", "Board Approval Date", "Closing Date",
         "Sub-sector", "Location", "Region", "Borrower", "Implementing Agency", "Project Description",
         "Project Abstract", "Major Sector %", "Environmental Category", "Themes"])

    # Find all project items and extract their information
    projects = soup.find_all("div", {"class": "proj-list-item"})
    for project in projects:
        project_id = project.get("data-projectid")
        project_name = project.find("a").text.strip()
        project_status = project.find("div", {"class": "proj-status"}).text.strip()
        project_sector = project.find("div", {"class": "proj-sector"}).text.strip()
        project_total_cost = project.find("div", {"class": "proj-cost"}).text.strip()
        project_board_approval_date = project.find("div", {"class": "proj-board-approval-date"}).text.strip()
        project_closing_date = project.find("div", {"class": "proj-closing-date"}).text.strip()
        project_sub_sector = project["sector"][0]["code"] if project["sector"] else ""
        project_location = project["countryshortname"] if project["countryshortname"] else ""
        project_region = project["regionname"] if project["regionname"] else ""
        project_borrower = project["borrower"][0]["name"] if project["borrower"] else ""
        project_implementing_agency = project["impagency"][0]["name"] if project["impagency"] else ""
        project_description = project["project_description"] if project["project_description"] else ""
        project_abstract = project["project_abstract"]['cdata'] if project["project_abstract"] else ""
        project_major_sector_percent = project["sector"][0]["sectorcodepercent"] if project["sector"] else ""
        project_environmental_category = project["environmentalcategory"] if project["environmentalcategory"] else ""
        project_themes = [theme["name"] for theme in project["theme"]] if project["theme"] else ""

        # Write the project information to the CSV file
        writer.writerow(
            [project_id, project_name, project_status, project_sector, project_total_cost, project_board_approval_date,
             project_closing_date, project_sub_sector, project_location, project_region, project_borrower,
             project_implementing_agency, project_description, project_abstract, project_major_sector_percent,
             project_environmental_category, project_themes])
