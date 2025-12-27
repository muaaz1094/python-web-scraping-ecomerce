#  Python Web Scraping – E-commerce Product Data

## Description

This project is a professional Python-based web scraper that extracts structured product data from an e-commerce website. It automatically navigates through multiple pages, collects relevant product information, and exports the data into clean, analysis-ready formats.

The scraper follows real-world best practices, including pagination handling, request headers, error handling, logging, and automated data export.

## Data Extracted

- Product Title
- Price
- Availability
- Rating
- Product URL

## Features

- Automatic pagination across all available pages
- Browser-like request headers to reduce blocking
- Requests timeout and error handling
- Logging to track scrapping progress
- Clean, modular, and reusable code structure
- Automated export to CSV and Excel formats

## Tools & Technologies

- Python
- Requests
- BeautifulSoup
- Pandas

## Output Formats

The saved data is stored in the output directory in the following formats:

- products.csv
- products.xlsx

## Use Cases

- Market research
- Product and price analysis
- Competitor monitoring
- Data collection and automation
- Business intelligence workflows

## How to Run

1. Clone the repository
2. Create and activate virtual enviroment
3. Install dependencies using `pip install -r requirements.txt`
4. Run `python scraper.py`

## Screenshots

### Script Execution

![Terminal Output](screenshots/terminal-success.png)

### Generated Output Files

![Output Files](screenshots/output-files.png)

### Excel Data Preview

![Excel Preview](screenshots/excel-preview.png)
