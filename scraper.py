from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

load_dotenv()
URL = os.environ.get("URL")


# Smartphones
def smartphones_scraper():
    initial_response = requests.get(f"{URL}/search/Smartphones?page=1")
    initial_soup = BeautifulSoup(initial_response.text, "html.parser")

    num_results = int(
        [
            x.text.split(" ")[0]
            for x in initial_soup.select(".search_content__khPDA > span:nth-child(1)")
        ][0]
    )
    pages = math.ceil(num_results / 10)

    product_brands = []
    product_names = []
    product_prices = []
    product_offers = []

    for page in range(1, pages + 1):
        response = requests.get(f"{URL}/search/Smartphones?page={page}")
        soup = BeautifulSoup(response.text, "html.parser")

        product_brands.extend(
            [x.text.split(" ")[0] for x in soup.select(".horizontal-card_name__7qix5")]
        )

        product_names.extend(
            [
                " ".join(x.text.split(" ")[1::])
                for x in soup.select(".horizontal-card_name__7qix5")
            ]
        )

        product_prices.extend(
            [
                float(x.text[2::])
                for x in soup.select(
                    ".horizontal-card_offer__Lq4E6 > span:nth-child(1)"
                )
            ]
        )

        product_offers.extend(
            [
                float(x.text[2::])
                for x in soup.select(
                    ".horizontal-card_offer__Lq4E6 > span:nth-child(2)"
                )
            ]
        )

    df = pd.DataFrame(
        {
            "Name": product_names,
            "Price": product_prices,
            "Offer": product_offers,
            "Brand": product_brands,
        }
    )

    df.to_csv("./data/smartphones.csv", index=False, encoding="utf-8")


# Laptops
def laptops_scraper():
    initial_response = requests.get(f"{URL}/search/Laptops?page=1")
    initial_soup = BeautifulSoup(initial_response.text, "html.parser")

    num_results = int(
        [
            x.text.split(" ")[0]
            for x in initial_soup.select(".search_content__khPDA > span:nth-child(1)")
        ][0]
    )
    pages = math.ceil(num_results / 10)

    product_brands = []
    product_names = []
    product_prices = []
    product_offers = []

    for page in range(1, pages + 1):
        response = requests.get(f"{URL}/search/Laptops?page={page}")
        soup = BeautifulSoup(response.text, "html.parser")

        product_brands.extend(
            [x.text.split(" ")[0] for x in soup.select(".horizontal-card_name__7qix5")]
        )

        product_names.extend(
            [
                " ".join(x.text.split(" ")[1::])
                for x in soup.select(".horizontal-card_name__7qix5")
            ]
        )

        product_prices.extend(
            [
                float(x.text[2::])
                for x in soup.select(
                    ".horizontal-card_offer__Lq4E6 > span:nth-child(1)"
                )
            ]
        )

        product_offers.extend(
            [
                float(x.text[2::])
                for x in soup.select(
                    ".horizontal-card_offer__Lq4E6 > span:nth-child(2)"
                )
            ]
        )

    df = pd.DataFrame(
        {
            "Name": product_names,
            "Price": product_prices,
            "Offer": product_offers,
            "Brand": product_brands,
        }
    )

    df.to_csv("./data/laptops.csv", index=False, encoding="utf-8")


smartphones_scraper()
laptops_scraper()
