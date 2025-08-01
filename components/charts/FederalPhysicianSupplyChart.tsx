"use client";

import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js/auto";
import physicianData from "@/metrics/cihi/physician_supply.json";
import { LineChartDataset } from "@/components/charts/types";
import { getPrimaryLineStyling, getTrendLineStyling } from "./utils/styling";
import { calculateLinearTrend } from "./utils/trendCalculator";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
);

interface FederalPhysicianSupplyChartProps {
  title?: string;
  startYear?: number;
  endYear?: number;
  height?: number;
  showTrend?: boolean;
}

export default function FederalPhysicianSupplyChart({
  title = "Federal Physician Supply",
  startYear = 2019,
  endYear = 2029,
  height = 400,
  showTrend = true,
}: FederalPhysicianSupplyChartProps) {
  // Get federal physician supply data
  const physicianDataObj = physicianData as any;
  const federalData = physicianDataObj.Canada["Physician Supply"] || [];

  // Filter data by year range
  const filteredData = federalData.filter(function (item: any) {
    const year = parseInt(item[0]);
    return year >= startYear && year <= endYear;
  });

  // Extract labels and values
  const labels = filteredData.map(function (item: any) {
    return item[0].toString(); // Year as string
  });

  const chartValues = filteredData.map(function (item: any) {
    return item[1]; // Number of physicians
  });

  const datasets: LineChartDataset[] = [
    {
      label: "Total Physicians",
      data: chartValues,
      ...getPrimaryLineStyling(),
    },
  ];

  // Calculate and add trend line
  if (showTrend && chartValues.length > 1) {
    const trendValues = calculateLinearTrend(chartValues);
    datasets.push({
      label: "Trend",
      data: trendValues,
      ...getTrendLineStyling(),
    });
  }

  const chartData = {
    labels,
    datasets,
  };

  const options: any = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top" as const,
        labels: {
          padding: 15,
          font: {
            size: 12,
          },
        },
      },
      title: {
        display: true,
        text: title,
        font: {
          size: 16,
          weight: "bold" as const,
        },
        padding: {
          top: 10,
          bottom: 20,
        },
      },
      tooltip: {
        callbacks: {
          title: function (context: any) {
            return `Year: ${context[0].label}`;
          },
          label: function (context: any) {
            const value = context.parsed.y;
            return `${context.dataset.label}: ${value.toLocaleString()} physicians`;
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: "Number of Physicians",
          font: {
            size: 14,
          },
          padding: {
            bottom: 10,
          },
        },
        ticks: {
          padding: 8,
          callback: function (value: any) {
            return value.toLocaleString();
          },
        },
        grid: {
          display: true,
          color: "rgba(0, 0, 0, 0.1)",
        },
      },
      x: {
        title: {
          display: true,
          text: "Year",
          font: {
            size: 14,
          },
          padding: {
            top: 10,
          },
        },
        ticks: {
          padding: 5,
        },
        grid: {
          display: true,
          color: "rgba(0, 0, 0, 0.1)",
        },
      },
    },
    layout: {
      padding: {
        left: 15,
        right: 15,
        top: 20,
        bottom: 20,
      },
    },
  };

  return (
    <div
      style={{
        width: "100%",
        height: `${height}px`,
        position: "relative",
      }}
    >
      <Line data={chartData} options={options} />
    </div>
  );
}
