import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar, Pie, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement
);

const Dashboard = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await axios.get('http://localhost:5000/api/etsy-data');
        setData(result.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    fetchData();
  }, []);

  if (!data) return <div>Loading...</div>;

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Etsy Data Analysis',
      },
    },
  };

  return (
    <div className="dashboard">
      <h1>Etsy Product Analysis Dashboard</h1>
      <div className="chart-container">
        <Bar data={data.topCategories} options={chartOptions} />
        <Pie data={data.competitors} options={chartOptions} />
        <Line data={data.profitability} options={chartOptions} />
        <Bar data={data.salesVolume} options={chartOptions} />
      </div>
      <div className="product-ideas">
        <h2>Product Ideas</h2>
        <ul>
          {data.productIdeas.map((idea, index) => (
            <li key={index}>
              <h3>{idea.name}</h3>
              <p>{idea.description}</p>
              <p>Keywords: {idea.keywords.join(', ')}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;
