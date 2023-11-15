# from dotenv import load_dotenv
# import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

URL = "https://tech-ecommerce-ebon.vercel.app"


# Products scraper
def products_scraper(
    category: str,
    brand_selector: str = ".horizontal-card_name__7qix5",
    name_selector: str = ".horizontal-card_name__7qix5",
    price_selector: str = ".horizontal-card_offer__Lq4E6 > span:nth-child(1)",
    offer_selector: str = ".horizontal-card_offer__Lq4E6 > span:nth-child(2)",
):
    # Search for products of a specific category composing the URL
    initial_response = requests.get(f"{URL}/search/{category}?page=1")
    initial_soup = BeautifulSoup(initial_response.text, "html.parser")

    # Get the number of results for this search
    results = int(
        [
            x.text.split(" ")[0]
            for x in initial_soup.select(".search_content__khPDA > span:nth-child(1)")
        ][0]
    )
    # Get the number of available pages for this search
    pages = math.ceil(results / 10)

    # Data fields
    brands = []
    names = []
    prices = []
    offers = []

    # Iterate through product pages and create a dataframe to export as CSV
    for page in range(1, pages + 1):
        response = requests.get(f"{URL}/search/{category}?page={page}")
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

        df.to_csv(f"./data/{category.lower()}.csv", index=False, encoding="utf-8")


initial_response = requests.get(f"{URL}/")
initial_soup = BeautifulSoup(initial_response.text, "html.parser")

categories = [
    x.text
    for x in initial_soup.select(
        ".header_categories__21wx4 > option:not(:first-of-type)"
    )
]

for cat in categories:
    products_scraper(category=cat)
