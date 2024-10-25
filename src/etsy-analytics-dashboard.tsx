import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface ProductCategory {
  category: string;
  avg_price: number;
  num_sellers: number;
  top_keywords: string[];
}

interface AnalysisResults {
  top_categories: ProductCategory[];
  trending_searches: string[];
  high_value_hashtags: string[];
}

const EtsyAnalyticsDashboard: React.FC = () => {
  const [analysisResults, setAnalysisResults] = useState<AnalysisResults | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalysisResults = async () => {
      try {
        const response = await axios.get<AnalysisResults>('/api/etsy-analysis');
        setAnalysisResults(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch analysis results');
        setLoading(false);
      }
    };

    fetchAnalysisResults();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!analysisResults) return <div>No data available</div>;

  return (
    <div className="etsy-analytics-dashboard">
      <h1>Etsy Digital Products Analytics Dashboard</h1>
      
      <section>
        <h2>Top 10 Product Categories</h2>
        <ul>
          {analysisResults.top_categories.map((category, index) => (
            <li key={index}>
              <h3>{category.category}</h3>
              <p>Average Price: ${category.avg_price.toFixed(2)}</p>
              <p>Number of Sellers: {category.num_sellers}</p>
              <p>Top Keywords: {category.top_keywords.join(', ')}</p>
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Trending Searches</h2>
        <ul>
          {analysisResults.trending_searches.map((search, index) => (
            <li key={index}>{search}</li>
          ))}
        </ul>
      </section>

      <section>
        <h2>High-Value Hashtags</h2>
        <ul>
          {analysisResults.high_value_hashtags.map((hashtag, index) => (
            <li key={index}>{hashtag}</li>
          ))}
        </ul>
      </section>
    </div>
  );
};

export default EtsyAnalyticsDashboard;
