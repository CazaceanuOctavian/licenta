//oh, my beloved...

import React, { useState, useEffect } from 'react';
import { ProductListDefault, ProductListDetailed } from './ProductComponents/ListComponent';

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

    if (true) {
         // Function to fetch data
        const fetchData = async (query: string) => {
            try {
                console.log('trying to fetch with query...');
                
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
                       <ProductListDefault data={data} />
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
                            <ProductListDetailed data={data} />
                        )}
                    </div>
            </div>
        );
    }
}

export default FetchAndPopulate;
