from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

load_dotenv()
URL = os.environ.get("URL")


# Products scraper
def products_scraper(
    section: str,
    brand_selector: str = ".horizontal-card_name__7qix5",
    name_selector: str = ".horizontal-card_name__7qix5",
    price_selector: str = ".horizontal-card_offer__Lq4E6 > span:nth-child(1)",
    offer_selector: str = ".horizontal-card_offer__Lq4E6 > span:nth-child(2)",
):
    initial_response = requests.get(f"{URL}/search/{section}?page=1")
    initial_soup = BeautifulSoup(initial_response.text, "html.parser")

    results = int(
        [
            x.text.split(" ")[0]
            for x in initial_soup.select(".search_content__khPDA > span:nth-child(1)")
        ][0]
    )
    pages = math.ceil(results / 10)

    brands = []
    names = []
    prices = []
    offers = []

    for page in range(1, pages + 1):
        response = requests.get(f"{URL}/search/{section}?page={page}")
        soup = BeautifulSoup(response.text, "html.parser")

        brands.extend([x.text.split(" ")[0] for x in soup.select(brand_selector)])

        names.extend(
            [" ".join(x.text.split(" ")[1::]) for x in soup.select(name_selector)]
        )

        prices.extend([float(x.text[2::]) for x in soup.select(price_selector)])

        offers.extend([float(x.text[2::]) for x in soup.select(offer_selector)])

        df = pd.DataFrame(
            {
                "Name": names,
                "Price": prices,
                "Offer": offers,
                "Brand": brands,
            }
        )

        df.to_csv(f"./data/{section.lower()}.csv", index=False, encoding="utf-8")


# Smartphones
products_scraper(
    section="Smartphones",
)

# Laptops
products_scraper(section="Laptops")
