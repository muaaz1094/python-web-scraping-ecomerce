import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import logging
from time import sleep

# ---------------- CONFIG ---------------- #

BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = BASE_URL + "catalogue/page-{}.html"
OUTPUT_DIR = "output"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36"
}

REQUEST_TIMEOUT = 10  # seconds
DELAY_BETWEEN_PAGES = 1  # seconds


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_rating(star_tag):
    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    classes = star_tag.get("class", []) if star_tag else []
    for cls in classes:
        if cls in rating_map:
            return rating_map[cls]
    return None


def scrape_page(page_number):
    url = CATALOGUE_URL.format(page_number)
    response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)

    if response.status_code != 200:
        logging.warning(
            f"Page {page_number} returned status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select(".product_pod")

    page_products = []

    for item in items:
        title = item.h3.a["title"]
        price = item.select_one(".price_color").text.strip()
        availability = item.select_one(".availability").text.strip()
        rating = get_rating(item.select_one(".star-rating"))
        product_url = BASE_URL + "catalogue/" + item.h3.a["href"]

        page_products.append({
            "Title": title,
            "Price": price,
            "Availability": availability,
            "Rating": rating,
            "Product URL": product_url
        })

    return page_products


def save_data(products):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.DataFrame(products)

    # Clean and normalize price column
    df["Price"] = (
        df["Price"]
        .str.replace(r"[^\d.]", "", regex=True)
        .astype(float)
    )

    csv_path = os.path.join(OUTPUT_DIR, "products.csv")
    excel_path = os.path.join(OUTPUT_DIR, "products.xlsx")

    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    df.to_excel(excel_path, index=False)

    logging.info(f"Data saved to {csv_path} and {excel_path}")


# ---------------- MAIN ---------------- #

def main():
    all_products = []
    page = 1

    logging.info("Starting web scraping process...")

    while True:
        try:
            logging.info(f"Scraping page {page}")
            page_products = scrape_page(page)

            if not page_products:
                logging.info("No more products found. Ending scraping.")
                break

            all_products.extend(page_products)
            page += 1
            sleep(DELAY_BETWEEN_PAGES)

        except requests.RequestException as e:
            logging.error(f"Request failed on page {page}: {e}")
            break

    logging.info(f"Total products scraped: {len(all_products)}")

    if all_products:
        save_data(all_products)
        logging.info("Scraping completed successfully.")
    else:
        logging.warning("No data scraped.")


if __name__ == "__main__":
    main()
