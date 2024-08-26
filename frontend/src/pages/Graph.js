import { useEffect, useState } from "react";
import Chart from "chart.js/auto";
import { readString } from "react-papaparse";
import { Scatter } from "react-chartjs-2";
import zoomPlugin from "chartjs-plugin-zoom";

import csv from "../assets/data.csv";
import "./graph.css";

Chart.register(zoomPlugin);

export default function Graph() {
  const X_AXIS = "x";
  const Y_AXIS = "y";
  const POINT_RADIUS = 5;
  const SHOW_GRID = true;

  const [data, setData] = useState({ datasets: [] });

  useEffect(() => {
    const papaConfig = {
      complete: (results, file) => {
        const parsed = results.data.map(function (row) {
          return {
            x: row[1],
            y: row[2],
            name: row[0],
          };
        });
        console.log(parsed);

        setData({
          datasets: [
            {
              label: "Ingredients",
              backgroundColor: "black",
              data: parsed,
              pointRadius: POINT_RADIUS,
              pointHoverRadius: POINT_RADIUS + 2,
            },
          ],
        });
      },
      download: true,
      error: (error, file) => {
        console.log("Error while parsing:", error, file);
      },
    };
    readString(csv, papaConfig);
  }, []);

  const options = {
    scales: {
      xAxes: {
        scaleLabel: {
          display: true,
          labelString: X_AXIS,
        },
        gridLines: {
          display: SHOW_GRID,
        },
        ticks: {
          callback: function (value, index, values) {
            return value.toLocaleString();
          },
        },
      },
      yAxes: {
        scaleLabel: {
          display: true,
          labelString: Y_AXIS,
        },
        gridLines: {
          display: SHOW_GRID,
        },
        ticks: {
          callback: function (value, index, values) {
            return value.toLocaleString();
          },
        },
      },
    },
    plugins: {
      tooltip: {
        displayColors: false,
        callbacks: {
          label: function (ctx) {
            console.log(ctx);
            return ctx.raw.name;
          },
        },
      },
      zoom: {
        pan: {
          enabled: true,
          mode: "xy",
        },
        zoom: {
          wheel: {
            enabled: true,
          },
          pinch: {
            enabled: true,
          },
          mode: "xy",
        },
      },
    },
  };

  return <Scatter options={options} data={data} />;
}
