import React, {useEffect, useRef} from 'react';
import Chart from '../components/Chart';

const IndexPage = () => {
    const chartRef = useRef();
    // const [transactions, setTransactions] = useState([]);
    useEffect(() => {
        const ws = new WebSocket('ws://localhost:8080/ws',);

        // ws.onopen = event => {
        //   ws.send("Connect");
        // };

        ws.onmessage = e => {
            const point = JSON.parse(e.data);
            console.log("mess: ", point);
            // setTransactions(point)
            chartRef.current.addTransactions(point)
        };

        //clean up function when we close page
        return () => ws.close();
    }, [])

    return (<div>
            <h1>Chart</h1>
            <Chart ref={chartRef}/>
        </div>);
};

export default IndexPage;