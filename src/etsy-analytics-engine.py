import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

class EtsyDigitalProductAnalytics:
    def __init__(self):
        self.product_categories = {
            'Digital Planners': {
                'base_creation_cost': 20,  # Time cost in hours
                'avg_price_range': (15, 40),
                'seasonal_factors': {
                    'Q1': 1.5,  # New Year planning boost
                    'Q2': 0.8,
                    'Q3': 1.2,  # Back to school season
                    'Q4': 1.0
                }
            },
            'Printable Wall Art': {
                'base_creation_cost': 8,
                'avg_price_range': (5, 25),
                'seasonal_factors': {
                    'Q1': 0.9,
                    'Q2': 1.2,  # Home decoration season
                    'Q3': 0.8,
                    'Q4': 1.4   # Holiday season
                }
            },
            'Templates': {
                'base_creation_cost': 12,
                'avg_price_range': (10, 30),
                'seasonal_factors': {
                    'Q1': 1.1,
                    'Q2': 1.0,
                    'Q3': 0.9,
                    'Q4': 1.2
                }
            },
            'Social Media Kits': {
                'base_creation_cost': 15,
                'avg_price_range': (20, 50),
                'seasonal_factors': {
                    'Q1': 1.2,
                    'Q2': 1.0,
                    'Q3': 0.9,
                    'Q4': 1.1
                }
            }
        }

    def analyze_product_profitability(self, 
                                    category: str, 
                                    target_price: float,
                                    estimated_monthly_sales: int) -> Dict:
        """
        Calculate detailed profitability metrics for a digital product
        """
        category_data = self.product_categories[category]
        
        # Calculate costs
        creation_cost = category_data['base_creation_cost'] * 25  # Assuming $25/hour value
        monthly_costs = {
            'etsy_listing_fee': 0.20,
            'renewal_fee': 0.20,
            'transaction_fee': target_price * 0.05,
            'payment_processing': target_price * 0.03,
            'advertising_cost': target_price * 0.10  # Assuming 10% of price for advertising
        }
        
        # Calculate revenue and profits
        monthly_revenue = target_price * estimated_monthly_sales
        monthly_total_costs = sum(monthly_costs.values()) * estimated_monthly_sales
        monthly_profit = monthly_revenue - monthly_total_costs
        
        # Calculate ROI and breakeven
        initial_investment = creation_cost + monthly_costs['advertising_cost']
        roi = (monthly_profit * 12) / initial_investment * 100
        breakeven_months = initial_investment / monthly_profit if monthly_profit > 0 else float('inf')
        
        # Calculate seasonal adjustments
        seasonal_profits = {}
        for quarter, factor in category_data['seasonal_factors'].items():
            seasonal_profits[quarter] = monthly_profit * 3 * factor
        
        return {
            'initial_investment': round(initial_investment, 2),
            'monthly_revenue': round(monthly_revenue, 2),
            'monthly_costs': {k: round(v * estimated_monthly_sales, 2) for k, v in monthly_costs.items()},
            'monthly_profit': round(monthly_profit, 2),
            'annual_profit': round(sum(seasonal_profits.values()), 2),
            'roi_percentage': round(roi, 2),
            'breakeven_months': round(breakeven_months, 1),
            'seasonal_quarterly_profits': {k: round(v, 2) for k, v in seasonal_profits.items()}
        }

    def project_market_trends(self, category: str, historical_data: List[Dict]) -> Dict:
        """
        Project market trends and future performance
        """
        df = pd.DataFrame(historical_data)
        
        # Prepare features for trend analysis
        scaler = StandardScaler()
        X = scaler.fit_transform(df[['search_volume', 'competition_level']].values)
        y = df['avg_price'].values
        
        # Fit linear regression model
        model = LinearRegression()
        model.fit(X, y)
        
        # Project next 6 months
        future_months = []
        last_data = df.iloc[-1]
        for i in range(1, 7):
            projected_volume = last_data['search_volume'] * (1 + (0.05 * i))  # Assume 5% monthly growth
            projected_competition = last_data['competition_level'] * (1 + (0.03 * i))  # Assume 3% competition growth
            
            X_pred = scaler.transform([[projected_volume, projected_competition]])
            projected_price = model.predict(X_pred)[0]
            
            future_months.append({
                'month': i,
                'projected_search_volume': round(projected_volume, 2),
                'projected_competition': round(projected_competition, 2),
                'projected_price': round(projected_price, 2)
            })
            
        return {
            'trend_coefficient': model.coef_.tolist(),
            'market_growth_rate': round((projected_volume / last_data['search_volume'] - 1) * 100, 2),
            'price_elasticity': round(model.coef_[0], 3),
            'future_projections': future_months
        }

    def get_optimization_recommendations(self, 
                                      category: str, 
                                      current_metrics: Dict) -> List[Dict]:
        """
        Provide specific recommendations for optimizing product performance
        """
        recommendations = []
        
        # Price optimization
        category_data = self.product_categories[category]
        min_price, max_price = category_data['avg_price_range']
        current_price = current_metrics.get('current_price', 0)
        
        if current_price < min_price:
            recommendations.append({
                'type': 'pricing',
                'action': 'increase_price',
                'potential_impact': round((min_price - current_price) * current_metrics.get('monthly_sales', 0), 2),
                'confidence_score': 0.8
            })
            
        # Seasonal optimization
        current_quarter = f'Q{(datetime.now().month-1)//3 + 1}'
        seasonal_factor = category_data['seasonal_factors'][current_quarter]
        
        if seasonal_factor > 1.1:
            recommendations.append({
                'type': 'seasonal',
                'action': 'increase_marketing',
                'potential_impact': round(current_metrics.get('monthly_profit', 0) * (seasonal_factor - 1), 2),
                'confidence_score': 0.9
            })
            
        return recommendations

class EtsyAIAgent:
    def __init__(self):
        self.base_url = "https://www.etsy.com/search"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_search_results(self, query):
        params = {"q": query, "ref": "search_bar"}
        response = requests.get(self.base_url, params=params, headers=self.headers)
        return BeautifulSoup(response.content, "html.parser")

    def extract_product_info(self, soup):
        products = []
        for item in soup.find_all("li", class_="wt-list-unstyled"):
            title = item.find("h3", class_="wt-text-caption")
            price = item.find("span", class_="currency-value")
            if title and price:
                products.append({
                    "title": title.text.strip(),
                    "price": float(price.text.strip().replace(",", ""))
                })
        return products

    def analyze_search_trends(self):
        # Implement logic to fetch and analyze search trends
        # This is a placeholder and should be replaced with actual API calls or web scraping
        trending_searches = [
            "digital planner", "printable wall art", "social media templates",
            "ebook template", "digital stickers", "lightroom presets",
            "canva templates", "procreate brushes", "digital invitations",
            "printable planner"
        ]
        return trending_searches

    def analyze_product_data(self, products):
        df = pd.DataFrame(products)
        
        # Calculate average price and number of sellers
        avg_price = df["price"].mean()
        num_sellers = len(df)
        
        # Extract keywords from titles
        titles = df["title"].tolist()
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(titles)
        feature_names = vectorizer.get_feature_names_out()
        
        # Get top keywords
        tfidf_sums = np.sum(tfidf_matrix, axis=0)
        top_keywords = [feature_names[i] for i in tfidf_sums.argsort()[0, -10:][0]]
        
        return {
            "avg_price": avg_price,
            "num_sellers": num_sellers,
            "top_keywords": top_keywords
        }

    def run_analysis(self):
        trending_searches = self.analyze_search_trends()
        results = []
        
        for search in trending_searches:
            soup = self.fetch_search_results(search)
            products = self.extract_product_info(soup)
            analysis = self.analyze_product_data(products)
            
            results.append({
                "category": search,
                "avg_price": analysis["avg_price"],
                "num_sellers": analysis["num_sellers"],
                "top_keywords": analysis["top_keywords"]
            })
        
        # Sort results by number of sellers (ascending) and average price (descending)
        sorted_results = sorted(results, key=lambda x: (x["num_sellers"], -x["avg_price"]))
        
        return {
            "top_categories": sorted_results[:10],
            "trending_searches": trending_searches,
            "high_value_hashtags": self.generate_hashtags(sorted_results)
        }

    def generate_hashtags(self, results):
        all_keywords = [keyword for result in results for keyword in result["top_keywords"]]
        keyword_counts = Counter(all_keywords)
        return [f"#{keyword.replace(' ', '')}" for keyword, _ in keyword_counts.most_common(10)]

# Usage
agent = EtsyAIAgent()
analysis_results = agent.run_analysis()
print(analysis_results)
