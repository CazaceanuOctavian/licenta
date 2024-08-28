import React, { useState, useEffect } from 'react';

// Define the type for your data
interface Product {
    id: number;
    name: string;
    price: number;
    rating: number;
    is_in_stock: boolean;
    url: string;
    productCode: string;
}

const FetchAndPopulate: React.FC = () => {
    const [query, setQuery] = useState<string>('');
    const [data, setData] = useState<Product[] | null>(null);
    const currentHref = window.location.href;


    if (currentHref === 'http://localhost:5173/') {
         // Function to fetch data
        const fetchData = async (query: string) => {
            try {
                console.log('trying to fetch with query...');
                console.log(encodeURIComponent(query))
                
                const response = await fetch('http://localhost:8080/products/name/search=' + encodeURIComponent(query));
                
                if (!response.ok) {
                    throw new Error(`HTTP error with Status: ${response.status}`);
                }

                const result: Product[] = await response.json();
                console.log(result)
                setData(result);
            } catch (error) {
                console.error('There was a problem with the fetch operation:', error);
            }
        };

        // Handler for key press event
        const handleKeyPress = (event: React.KeyboardEvent<HTMLInputElement>) => {
            if (event.key === 'Enter') {
                fetchData(query);
            }
        };

        return (
            <div>
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={handleKeyPress}
                    placeholder="Enter your query and press Enter"
                />
                <div className="product-list">
                    {data === null ? (
                        <div>Loading...</div>
                    ) : (
                        <ul>
                            {data.map(item => (
                                <li key={item.id} className="product-item">
                                    <div className="product-info">
                                        <h2 className="product-name">
                                        <a 
                                        href={`http://localhost:5173/products/fetch_data=${item.productCode}`} 
                                        target="_blank" 
                                        rel="noopener noreferrer"
                                        >
                                        {item.name}
                                        </a>
                                        </h2>
                                        <p className="product-price">{item.price.toFixed(2)} lei</p>
                                        <p className="product-rating">Rating: {item.rating.toFixed(1)}</p>
                                        <p className="product-stock">
                                            {item.is_in_stock ? 'In stoc' : 'Nu este in stoc'}
                                        </p>
                                        <p className='product-code'> Cod Produs: {item.productCode}</p>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            </div>
        );
    }

    else {
        let productCode: string = currentHref.split('=')[1]

        const fetchData = async () => {
            try {
                console.log('trying to fetch product with code: ' + productCode + '...')        

                const response = await fetch('http://localhost:8080/products/code/search=' + productCode);
                
                if (!response.ok) {
                    throw new Error(`HTTP error with Status: ${response.status}`);
                }

                const result: Product[] = await response.json();
                console.log(result)
                setData(result);
            } catch (error) {
                console.error('There was a problem with the fetch operation:', error);
            }
        };

        useEffect(() => {
            fetchData();
        }, []); 
    
        return (
                <div>
                    <div className="product-list">
                        {data === null ? (
                            <div>Loading...</div>
                        ) : (
                            <ul>
                                {data.map(item => (
                                    <li key={item.id} className="product-item">
                                        <div className="product-info">
                                            <h2 className="product-name">
                                                {item.name}
                                            </h2>
                                            <p className="product-price">{item.price.toFixed(2)} lei</p>
                                            <p className="product-rating">Rating: {item.rating.toFixed(1)}</p>
                                            <p className="product-stock">
                                                {item.is_in_stock ? 'In stoc' : 'Nu este in stoc'}
                                            </p>
                                            <p className='product-code'> Cod Produs: {item.productCode}</p>
                                            <p className='origin-url'>
                                                Link magazin: 
                                                <a href={item.url}>                                                
                                                    {item.url}
                                                </a> 
                                            </p>
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
            </div>
        );
    }
}

export default FetchAndPopulate;
