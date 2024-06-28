# Smichoff Scraper

This project is a web scraper designed to gather climbing route data from the _[WallOnSight](http://www.wallonsight.com)_ website. The scraper extracts information about the climbing routes, including their details such as holds, difficulty, sector, line number, setter, creation date, character, height, and planned minimum durability. The data is saved in a JSON file for archival purposes.

## Disclaimer

This project was created solely for **personal, non-commercial** use. The data is scraped from the _WallOnSight_ website. The scraper uses only public data and does not access any unauthorized information. In case of any issues or concerns regarding this scraper, please contact me, and I will promptly take it down.

## Contact

For any inquiries or issues, please reach out to me at [nikinayzer@gmail.com].

## Features

- Scrapes route information from the WallOnSight website.
- Extracts detailed information from individual route pages, including height and planned minimum durability.
- Handles pagination to gather data from all available pages.
- Archives routes that have been removed from the website by marking them with an `archive` flag.
- Avoids duplicating existing routes by checking against previously saved data.

## Usage

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/smichoff-scraper.git
    cd smichoff-scraper
    ```

2. **Install the required packages**:
    ```sh
    pip install requests beautifulsoup4
    ```

3. **Run the scraper**:
    ```sh
    python web_scraper.py
    ```

4. **View the results**:
   The scraped data is saved in the `routes.json` file in the project directory.

## File Structure

- `web_scraper.py`: Main script to scrape data from the WallOnSight website.
- `routes.json`: JSON file where the scraped data is saved.

## Example JSON Output

```json
[
    {
        "id": "7351",
        "holds": "Blue Holds",
        "name": "Route Name",
        "difficulty": "5.10",
        "sector": "A (big wall)",
        "line_number": "1",
        "setter": "Setter Name",
        "creation_date": "07.05.2024",
        "character": "Technical",
        "height": "25m",
        "planned_until": "15.08.2024",
        "archive": false
    },
    ...
]
