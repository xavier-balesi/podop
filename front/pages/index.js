import React, {useEffect, useRef} from 'react';
import Chart from '../components/Chart';

const IndexPage = () => {
    const chartRef = useRef();
    // const [transactions, setTransactions] = useState([]);
    useEffect(() => {
        const ws = new WebSocket('ws://localhost:8000/ws',);

        // ws.onopen = event => {
        //   ws.send("Connect");
        // };

        ws.onmessage = e => {
            const backMsg = JSON.parse(e.data);
            console.log("ws input: ", backMsg);
            if (Array.isArray(backMsg)) {
                chartRef.current.addCountsHistory(backMsg)
            } else {
                chartRef.current.addCounts(backMsg)
            }
        };

        //clean up function when we close page
        return () => ws.close();
    }, [])

    return (<div>
            <Chart ref={chartRef}/>
        </div>);
};

export default IndexPage;