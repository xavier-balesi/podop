import React from 'react';
import Chart from '../components/Chart';

const IndexPage = () => {
    // useEffect(() => {
    //
    //     const ws = new WebSocket('ws://localhost:8080/ws', );
    //
    //     // ws.onopen = event => {
    //     //   ws.send("Connect");
    //     // };
    //
    //
    //     ws.onmessage = e => {
    //         const point = JSON.parse(e.data);
    //         console.log("mess: ", point);
    //
    //         if (this.chartRef.current) {
    //             chartRef.current.chart.series[0].addPoint(
    //                 [point.ts, point.foo],
    //                 true
    //             );
    //         }
    //     };
    //     //clean up function when we close page
    //     return () => ws.close();
    // }, [])

  return (
      <div>
        <h1>Chart</h1>
        <Chart />
      </div>
  );
};

export default IndexPage;