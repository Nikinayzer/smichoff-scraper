import requests
from bs4 import BeautifulSoup
import json
import os

# Base URL of the page to scrape
base_url = 'http://www.wallonsight.com/routes/list'
route_base_url = 'http://www.wallonsight.com/routes/detail'

# File paths
json_file = 'routes.json'

# Initialize a set to hold existing route IDs
existing_ids = set()


def scrape_route_details(route_id):
    route_url = f"{route_base_url}/{route_id}"
    print(f"Scraping route detail page: {route_url}")
    response = requests.get(route_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    height_div = soup.find('div', {'class': 'routeHeight'})
    height = height_div.text.strip() if height_div else ''

    planned_until = ''
    data_table = soup.find('table', {'class': 'dataTable'})

# in case the table is not found, the scraper will not break
    if data_table:
        tbody = data_table.find('tbody')
        if tbody:
            planned_until_td = tbody.find_all('td')[5]
            planned_until = planned_until_td.text.strip() if planned_until_td else ''

    return height, planned_until



def scrape_page(url):
    print(f"Scraping page: {url}")
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', id='niceTable')

    if table:
        print("Table found on page")
        # Initialize a list to hold the data from this page
        page_data = []

        tbody = table.find('tbody')
        if tbody:
            print("Tbody found in table")

            for row in tbody.find_all('tr'):
                columns = row.find_all('td')

                row_id = row['id'].replace('route_row_', '')  # Extract ID from <tr> id attribute
                holds = columns[1].div['title'] if columns[1].div else ''
                name = columns[2].a.text if columns[2].a else ''
                difficulty = columns[3].text.strip() if columns[3] else ''
                sector = columns[4].text.strip() if columns[4] else ''
                line_number = columns[5].text.strip() if columns[5] else ''
                setter = columns[6].text.strip() if columns[6] else ''
                creation_date = columns[7].text.strip() if columns[7] else ''
                character = ', '.join(img['title'] for img in columns[8].find_all('img')) if columns[8] else ''

                height, planned_until = scrape_route_details(row_id)

                if row_id:
                    page_data.append({
                        'id': row_id,
                        'holds': holds,
                        'name': name,
                        'difficulty': difficulty,
                        'sector': sector,
                        'line_number': line_number,
                        'setter': setter,
                        'creation_date': creation_date,
                        'character': character,
                        'height': height,
                        'planned_until': planned_until,
                        'archive': False
                    })

            return page_data
        else:
            print(f"No tbody found in table with id 'niceTable' on page {url}")
            return []
    else:
        print(f"No table with id 'niceTable' found on page {url}")
        return []


def load_existing_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
            return existing_data
    else:
        return []


print(f"Loading existing data from {json_file}")
all_routes = load_existing_data(json_file)
print(f"Existing routes loaded: {len(all_routes)} routes found")

# Populate existing_ids set with IDs from existing routes
for route in all_routes:
    if 'id' in route:
        existing_ids.add(route['id'])
    else:
        print(f"Route {route} does not have an 'id' key")

# Track found route IDs
found_ids = set()

# Iterate over each pagination page
offset = 0
while True:
    url = f"{base_url}?limitOffset={offset}"

    page_data = scrape_page(url)

    if not page_data:
        print(f"No routes found on page {url}. Stopping.")
        break

    for route in page_data:
        found_ids.add(route['id'])
        if route['id'] not in existing_ids:
            all_routes.append(route)
            existing_ids.add(route['id'])
            print(f"Added route {route['id']} - {route['name']}")

    offset += 50

# Update existing routes to archive if they are not found in the new data
for route in all_routes:
    if route['id'] not in found_ids:
        route['archive'] = True
        print(f"Archived route {route['id']} - {route['name']}")

json_data = json.dumps(all_routes, ensure_ascii=False, indent=4)

#print(json_data)

with open(json_file, 'w', encoding='utf-8') as f:
    f.write(json_data)

print(f"Data saved to {json_file}")
