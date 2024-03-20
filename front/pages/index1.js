import { useEffect, useState } from 'react';
import Chart from 'chart.js/auto';
import io from 'socket.io-client';
const IndexPage = () => {
  const [chartData, setChartData] = useState({});

  // useEffect(() => {
  //
  //   const socket = new io('ws://localhost:8080', {path: '/ws',transports: ['websocket'],  addTrailingSlash: false,});
  //
  //   socket.io.on("error", (error) => {
  //     console.error(error);
  //   });
  //
  //   socket.onmessage = (event) => {
  //     const newData = JSON.parse(event.data);
  //     setChartData(newData);
  //   };
  //
  //   return () => socket.close();
  // }, []);

  useEffect(() => {

    const ws = new WebSocket('ws://localhost:8080/ws', );

    // ws.onopen = event => {
    //   ws.send("Connect");
    // };


    ws.onmessage = e => {
      const message = JSON.parse(e.data);
      console.log("mess: ", message);
      // setMessages((prev) => [...prev, message.message ?? "EMPTY"]);
    };
    // setWebsckt(ws);
    //clean up function when we close page
    // return () => ws.close();
  }, [])


  useEffect(() => {
    const ctx = document.getElementById('myChart');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: [chartData.ts || ''],
        datasets: [
          {
            label: 'foo',
            data: [chartData.foo || 0],
            borderColor: 'red',
          },
          {
            label: 'bar',
            data: [chartData.bar || 0],
            borderColor: 'blue',
          },
          {
            label: 'foobar',
            data: [chartData.foobar || 0],
            borderColor: 'green',
          },
          {
            label: 'robot',
            data: [chartData.robot || 0],
            borderColor: 'orange',
          },
          {
            label: 'money',
            data: [chartData.money || 0],
            borderColor: 'purple',
          },
          {
            label: 'transaction',
            data: [chartData.transaction || 0],
            borderColor: 'black',
          },
        ],
      },
      options: {
        scales: {
          x: {
            type: 'linear',
            position: 'bottom',
            title: {
              display: true,
              text: 'Time',
            },
          },
          y: {
            type: 'linear',
            position: 'left',
            title: {
              display: true,
              text: 'Count',
            },
          },
        },
      },
    });
  }, [chartData]);

  return <canvas id="myChart" />;
};

export default IndexPage;
