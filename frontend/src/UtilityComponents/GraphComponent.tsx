import { useEffect, useState } from "react";
import { FetchData } from "./FetchComponent";
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const GraphComponent: React.FC = () => {
    const [graphData, setGraphData] = useState<string>('');
    const [arrayGraphData, setArrayGraphData] = useState<number[]>([]);

    const graph = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June'],
        datasets: [
          {
            label: 'Pret Produs',
            data: arrayGraphData, 
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
          },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top' as const,
            },
            title: {
                display: true,
                text: 'Monthly Sales',
            },
        },
    };

    const callApi = async () => {
        try {
            console.log('FROM APICALL TRYING TO FETCH: PRICE HISTORY');
            const data = await FetchData('http://localhost:8080/products/productHistory=Z15T001D0');
            setGraphData(data);
        } catch (error) {
            console.log('error with fetch operation: ' + error);
        }
    };

    useEffect(() => {
        callApi();
    }, []);

    useEffect(() => {
        if (graphData) {
            // Transform graphData to array of numbers
            const parsedData = graphData[0].split(',').map(Number)
            setArrayGraphData(parsedData);
        }
    }, [graphData]);

    return (
        <div className='price-history-graph'>
            <Bar data={graph} options={options} />
        </div>
    );
};

export default GraphComponent;
