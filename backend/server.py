from flask import Flask, jsonify
from data_collection_agent import EtsyDataCollector
from data_analysis_agent import EtsyDataAnalyzer
from product_ideation_agent import ProductIdeationAgent
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/etsy-data')
def get_etsy_data():
    collector = EtsyDataCollector()
    data = collector.collect_data()
    
    analyzer = EtsyDataAnalyzer(data)
    analysis_results = analyzer.analyze_data()
    
    ideation_agent = ProductIdeationAgent(analysis_results)
    product_ideas = ideation_agent.create_product_suggestions()
    
    return jsonify({
        'topCategories': analysis_results['top_categories'],
        'competitors': analysis_results['competitors'],
        'profitability': analysis_results['profitability'],
        'salesVolume': analysis_results['sales_volume'],
        'productIdeas': product_ideas
    })

if __name__ == '__main__':
    app.run(debug=True)
