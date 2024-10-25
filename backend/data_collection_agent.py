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

    # ... (rest of the class implementation remains the same)

if __name__ == "__main__":
    collector = EtsyDataCollector()
    data = collector.collect_data()
    output_dir = "../data"
    os.makedirs(output_dir, exist_ok=True)
    data.to_csv(f"{output_dir}/etsy_data_{datetime.now().strftime('%Y%m%d')}.csv", index=False)
    print(f"Data collected and saved to {output_dir}/etsy_data_{datetime.now().strftime('%Y%m%d')}.csv")
