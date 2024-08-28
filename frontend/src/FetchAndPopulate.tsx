import { useEffect, useState } from 'react';

// Define the type for your data
interface Product {
    name: string;
    price: number;
    rating: number;
    is_in_stock: boolean;
    url: string;
    product_code: string;
}

function FetchAndPopulate(searchCategory: string) {
    // Use the defined type with useState
    const [data, setData] = useState<Product[] | null>(null);

    useEffect(() => {
        async function fetchData() {
            try {
                console.log('trying to fetch...');
                const response = await fetch('http://localhost:8080/products/' + searchCategory);
                
                if (!response.ok) {
                    throw new Error(`HTTP error with Status: ${response.status}`);
                }

                const result: Product[] = await response.json();
                setData(result);
            } catch (error) {
                console.error('There was a problem with the fetch operation:', error);
            }
        }

        fetchData();
    }, []); 

    if (data === null) {
        return <div>Loading...</div>;
    }

    console.log('data is:')
    console.log(data)

    return (
        <div className="product-list">
             <ul>
                    {data.map(item => (
                        <li key={item.name} className="product-item">
                            <div className="product-info">
                                <h2 className="product-name">{item.name}</h2>
                                <p className="product-price">${item.price.toFixed(2)}</p>
                                <p className="product-rating">Rating: {item.rating.toFixed(1)}</p>
                                <p className="product-stock">
                                    {item.is_in_stock ? 'In Stock' : 'Out of Stock'}
                                </p>
                            </div>
                        </li>
                    ))}
                </ul>
        </div>    
)}

export default FetchAndPopulate;
