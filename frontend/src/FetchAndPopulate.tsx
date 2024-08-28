import React, { useState, useEffect } from 'react';

// Define the type for your data
interface Product {
    name: string;
    price: number;
    rating: number;
    is_in_stock: boolean;
    url: string;
    product_code: string;
}

const FetchAndPopulate: React.FC = () => {
    const [query, setQuery] = useState<string>('');
    const [data, setData] = useState<Product[] | null>(null);

        // Handler for key press event
        const handleKeyPress = (event: React.KeyboardEvent<HTMLInputElement>) => {
            if (event.key === 'Enter') {
                fetchData(query);
            }
        };

    // Function to fetch data
    const fetchData = async (query: string) => {
        try {
            console.log('trying to fetch with query...');
            console.log(encodeURIComponent(query))
            const response = await fetch('http://localhost:8080/products/' + encodeURIComponent(query));
            
            if (!response.ok) {
                throw new Error(`HTTP error with Status: ${response.status}`);
            }

            const result: Product[] = await response.json();
            setData(result);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
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
                            <li key={item.product_code} className="product-item">
                                <div className="product-info">
                                    <h2 className="product-name">{item.name}</h2>
                                    <p className="product-price">${item.price.toFixed(2)}</p>
                                    <p className="product-rating">Rating: {item.rating.toFixed(1)}</p>
                                    <p className="product-stock">
                                        {item.is_in_stock ? 'In Stock' : 'Out of Stock'}
                                    </p>
                                    <p className='product-code'> {item.product_code} </p>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
}

export default FetchAndPopulate;
