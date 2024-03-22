import React, {forwardRef, useImperativeHandle, useRef} from 'react';
import HighchartsReact from 'highcharts-react-official';
import Highcharts from 'highcharts/highstock';

import HighchartsExporting from 'highcharts/modules/exporting';

if (typeof Highcharts === 'object') {
    HighchartsExporting(Highcharts);
}

const Chart = forwardRef(function Chart(props, ref) {
    // Create an internal ref to not expose all the DOM to the parent component
    // https://react.dev/reference/react/useImperativeHandle#exposing-a-custom-ref-handle-to-the-parent-component
    const chartRef = useRef();
    useImperativeHandle(ref, () => {
        return {
            addCountsHistory: (countsHistory) => {
                if (chartRef.current) {
                    const chart = chartRef.current.chart;
                    const fooPoints = [];
                    const barPoints = [];
                    const foobarPoints = [];
                    const moneyPoints = [];
                    const robotPoints = [];
                    for (let counts of countsHistory) {
                        fooPoints.push([counts.ts, counts.foo]);
                        barPoints.push([counts.ts, counts.bar]);
                        foobarPoints.push([counts.ts, counts.foobar]);
                        moneyPoints.push([counts.ts, counts.money]);
                        robotPoints.push([counts.ts, counts.robot]);
                    }
                    chart.series[0].setData(fooPoints, false);
                    chart.series[1].setData(barPoints, false);
                    chart.series[2].setData(foobarPoints, false);
                    chart.series[3].setData(moneyPoints, false);
                    chart.series[4].setData(robotPoints, false);
                    chart.redraw();
                }
            }, addCounts: (counts) => {
                if (chartRef.current) {
                    const chart = chartRef.current.chart
                    chart.series[0].addPoint([counts.ts, counts.foo]);
                    chart.series[1].addPoint([counts.ts, counts.bar]);
                    chart.series[2].addPoint([counts.ts, counts.foobar]);
                    chart.series[3].addPoint([counts.ts, counts.money]);
                    chart.series[4].addPoint([counts.ts, counts.robot]);
                    chart.redraw();
                }
            },
        }
    });

    function durationFormatter(ms) {
        const seconds = Number(ms) / 1000;
        const h = Math.floor(seconds % (3600 * 24) / 3600);
        const m = Math.floor(seconds % 3600 / 60);
        return `${h < 10 ? `0${h}` : h}:${m < 10 ? `0${m}` : m}`
    }

    const chartOptions = {
        title: {
            text: 'Resource graph', align: 'left'
        },

        subtitle: {
            text: 'Source: WebSocket from backend', align: 'left'
        },

        plotOptions: {
            series: {
                crosshair: true
            }
        },

        xAxis: {
            labels: {
                formatter: function () {
                    return durationFormatter(this.value);
                }
            }, crosshair: {
                color: '#4E7DD9', dashStyle: 'Dash',
            }, ordinal: false, minRange: 1,
        },

        yAxis: {
            title: {
                text: 'Resource count',
            }
        },

        series: [{name: 'foo',}, {name: 'bar'}, {name: 'foobar'}, {name: 'money'}, {name: 'robot'},],

        chart: {
            zoomType: 'xy'
        },

        tooltip: {
            shared: true,
            crosshairs: true,
            animation: true,
            useHTML: true,
            backgroundColor: 'rgba(255, 255, 255)',
            borderWidth: 1,
            borderRadius: 15,
            borderColor: '#B0C4DB',
            shadow: {
                offsetX: 1, offsetY: 2, width: 2, opacity: 0.05,
            },
            shape: 'square',
            hideDelay: 100,
            outside: false,
        },
    };


    return (<div>
        <HighchartsReact
            highcharts={Highcharts}
            options={chartOptions}
            constructorType="chart"
            ref={chartRef}
        />
    </div>);
});

export default Chart;
