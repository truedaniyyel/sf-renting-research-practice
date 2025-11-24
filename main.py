from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv

load_dotenv()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get('https://appbrewery.github.io/Zillow-Clone/', headers=headers)

data = response.text
soup = BeautifulSoup(data, 'html.parser')

all_cards = soup.select(".StyledPropertyCardDataWrapper")

zillow_data = []

for card in all_cards:
        link = card.select_one("a")["href"]
        address = card.select_one("address").get_text().replace(" | ", " ").strip()

        try:
            price_text = card.select_one(".PropertyCardWrapper__StyledPriceLine").get_text()
            clean_price = price_text.replace("/mo", "").split("+")[0]
        except AttributeError:
            clean_price = "N/A"

        zillow_data.append({
            "address": address,
            "price": clean_price,
            "link": link
        })

print(f"Scraped {len(zillow_data)} listings.")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

form_url = os.environ.get("GOOGLE_FORM_URL")

if not form_url:
    print("Error: GOOGLE_FORM_URL not found in .env file")
    exit()

driver.get(form_url)

for listing in zillow_data:
    time.sleep(2)

    all_text_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")

    if len(all_text_inputs) >= 3:
        all_text_inputs[0].send_keys(listing['address'])
        all_text_inputs[1].send_keys(listing['price'])
        all_text_inputs[2].send_keys(listing['link'])

        submit_button = driver.find_element(By.CSS_SELECTOR, '[role="button"][aria-label="Submit"]')
        submit_button.click()

        time.sleep(1.5)

        next_response_link = driver.find_element(By.CSS_SELECTOR, "a")
        next_response_link.click()
    else:
        print("Error: Could not find 3 input fields on this page.")

print("Done!")