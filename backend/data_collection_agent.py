import requests
from datetime import datetime
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='../.env')

class EtsyDataCollector:
    def __init__(self):
        self.api_key = os.getenv("ETSY_API_KEY")
        self.shared_secret = os.getenv("ETSY_SHARED_SECRET")
        self.base_url = "https://openapi.etsy.com/v3"
        self.headers = {
            "x-api-key": self.api_key,
            "Authorization": f"Bearer {self.api_key}"
        }

    def get_trending_searches(self):
        endpoint = f"{self.base_url}/application/trending-searches"
        response = requests.get(endpoint, headers=self.headers)
        if response.status_code == 200:
            return response.json().get('trending_searches', [])
        else:
            print(f"Error fetching trending searches: {response.status_code}")
            return []

    def get_product_data(self, search_term):
        endpoint = f"{self.base_url}/application/listings/active"
        params = {
            "keywords": search_term,
            "limit": 100,  # Adjust as needed
            "sort_on": "created",
            "sort_order": "desc"
        }
        response = requests.get(endpoint, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            print(f"Error fetching product data for {search_term}: {response.status_code}")
            return []

    def collect_data(self):
        trending_searches = self.get_trending_searches()
        data = []
        for search_term in trending_searches:
            product_data = self.get_product_data(search_term)
            for product in product_data:
                data.append({
                    "search_term": search_term,
                    "listing_id": product.get("listing_id"),
                    "title": product.get("title"),
                    "price": product.get("price", {}).get("amount"),
                    "currency": product.get("price", {}).get("currency_code"),
                    "quantity": product.get("quantity"),
                    "views": product.get("views"),
                    "num_favorers": product.get("num_favorers"),
                    "created_timestamp": product.get("created_timestamp"),
                })
        
        return pd.DataFrame(data)

if __name__ == "__main__":
    collector = EtsyDataCollector()
    data = collector.collect_data()
    output_dir = "../data"
    os.makedirs(output_dir, exist_ok=True)
    data.to_csv(f"{output_dir}/etsy_data_{datetime.now().strftime('%Y%m%d')}.csv", index=False)
    print(f"Data collected and saved to {output_dir}/etsy_data_{datetime.now().strftime('%Y%m%d')}.csv")
