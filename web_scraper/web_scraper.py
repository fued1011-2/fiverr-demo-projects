import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_quotes(output_file="quotes.csv"):
    url = "https://quotes.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = []
    for quote_block in soup.find_all("div", class_="quote"):
        text = quote_block.find("span", class_="text").get_text()
        author = quote_block.find("small", class_="author").get_text()
        quotes.append({"text": text, "author": author})

    df = pd.DataFrame(quotes)
    df.to_csv(output_file, index=False)
    print(f"Saved {len(df)} quotes to {output_file}")

if __name__ == "__main__":
    scrape_quotes()
