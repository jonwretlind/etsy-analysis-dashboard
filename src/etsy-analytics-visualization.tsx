import React from 'react';
import { Bar, Pie, Line } from 'react-chartjs-2';
import { Chart as ChartJS, registerables } from 'chart.js';
ChartJS.register(...registerables);

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

interface EtsyAnalyticsVisualizationProps {
  analysisResults: AnalysisResults;
}

const EtsyAnalyticsVisualization: React.FC<EtsyAnalyticsVisualizationProps> = ({ analysisResults }) => {
  const categoryNames = analysisResults.top_categories.map(cat => cat.category);
  const avgPrices = analysisResults.top_categories.map(cat => cat.avg_price);
  const numSellers = analysisResults.top_categories.map(cat => cat.num_sellers);

  const barChartData = {
    labels: categoryNames,
    datasets: [
      {
        label: 'Average Price',
        data: avgPrices,
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  const pieChartData = {
    labels: categoryNames,
    datasets: [
      {
        data: numSellers,
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
          '#FF9F40', '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
        ],
      },
    ],
  };

  const lineChartData = {
    labels: categoryNames,
    datasets: [
      {
        label: 'Number of Sellers',
        data: numSellers,
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };

  return (
    <div className="etsy-analytics-visualization">
      <h2>Product Category Analysis</h2>
      <div className="chart-container">
        <Bar data={barChartData} options={{ responsive: true, maintainAspectRatio: false }} />
      </div>

      <h2>Market Share by Number of Sellers</h2>
      <div className="chart-container">
        <Pie data={pieChartData} options={{ responsive: true, maintainAspectRatio: false }} />
      </div>

      <h2>Seller Distribution Across Categories</h2>
      <div className="chart-container">
        <Line data={lineChartData} options={{ responsive: true, maintainAspectRatio: false }} />
      </div>

      <h2>High-Value Hashtags</h2>
      <div className="hashtag-cloud">
        {analysisResults.high_value_hashtags.map((hashtag, index) => (
          <span key={index} className="hashtag">{hashtag}</span>
        ))}
      </div>
    </div>
  );
};

export default EtsyAnalyticsVisualization;
