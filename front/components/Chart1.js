import React, { useEffect, useRef, useState } from 'react';
import HighchartsReact from 'highcharts-react-official';
import Highcharts from 'highcharts/highstock';

import HighchartsExporting from 'highcharts/modules/exporting';

if (typeof Highcharts === 'object') {
  HighchartsExporting(Highcharts);
}

const Chart = () => {
    const chartRef = useRef();


    useEffect(() => {

        const ws = new WebSocket('ws://localhost:8080/ws', );

        // ws.onopen = event => {
        //   ws.send("Connect");
        // };


        ws.onmessage = e => {
            const point = JSON.parse(e.data);
            console.log("mess: ", point);

            if (chartRef.current) {
                chartRef.current.chart.series[0].addPoint(
                    [point.ts, point.foo],
                    true
                );
            }
        };
        // setWebsckt(ws);
        //clean up function when we close page
        return () => ws.close();
    }, [])


    const [chartOptions, setChartOptions] = useState({
        xAxis: {
            type: 'logarithmic',
            crosshair: {
                color: '#4E7DD9',
                dashStyle: 'Dash',
            },
            ordinal: false,
            minRange: 1,
        },
        yAxis: {
            opposite: false,
            labels: {
                format: '{value}%',
            },
            gridLineDashStyle: 'Dash',
            gridLineColor: '#01052D40',
            gridLineWidth: 0.5,
            // min: yAxisMin,
        },
        series: [
            {
                type: 'areaspline',
                name: 'Chart',
                data: null,
                lineWidth: 3,
                lineColor: '#4E7DD9',
                fillColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1,
                    },
                    stops: [
                        [0, 'rgba(78, 125, 217, 0.4)'],
                        [1, 'rgba(78, 125, 217, 0.05)'],
                    ],
                },
                marker: {
                    fillColor: 'white',
                    lineWidth: 2,
                    radius: 3,
                    lineColor: '#4E7DD9',
                },
                animation: {
                    duration: 500,
                },
            },
        ],
        chart: {
            backgroundColor: 'transparent',
            // zoomType: "x",
        },
        navigation: {
            enabled: false,
            buttonOptions: {
                enabled: false,
            },
        },
        rangeSelector: { enabled: false },
        credits: { enabled: false },
        tooltip: {
            animation: true,
            // xDateFormat: "",
            useHTML: true,
            backgroundColor: 'rgba(255, 255, 255)',
            borderWidth: 1,
            borderRadius: 15,
            borderColor: '#B0C4DB',
            shadow: {
                offsetX: 1,
                offsetY: 2,
                width: 2,
                opacity: 0.05,
            },
            shape: 'square',
            // split: true,
            hideDelay: 100,
            outside: false,
        },
        navigator: {
            handles: {
                // lineWidth: 1,
                width: 20,
                height: 30,
            },
            maskFill: 'rgba(78, 125, 217, 0.2)',
            outlineWidth: 0,
            enabled: false,
            xAxis: {},
        },
        scrollbar: {
            enabled: false,
        },
    });

    useEffect(() => {
        setChartOptions({
            series: {
                data: [],
            },
        });
    }, []);

    return (
        <div>
            <HighchartsReact
                highcharts={Highcharts}
                options={chartOptions}
                constructorType="chart"
                ref={chartRef}
            />
        </div>
    );
};

export default Chart;
