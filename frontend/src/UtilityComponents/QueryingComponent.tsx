import React, { useEffect, useState } from "react";
import { FetchData } from "./FetchComponent";

interface SearchProps {
    lowerPice: string;
    upperPrice: string;
    setLowerPrice: (query: string) => void;
    setUpperPrice: (query: string) => void;
    category: string[];
    setCategory: (query: string[]) => void;
}

const QueryPrice: React.FC<SearchProps> = ({ lowerPice, upperPrice, category, setLowerPrice, setUpperPrice, setCategory }) => {

    const callApi = async () => {
        try {
            console.log('FROM APICALL TRYING TO FETCH: CATEGORIES');
            const data = await FetchData('http://localhost:8080/products/categories');
            setCategory(data);
        } catch (error) {
            console.log('error with fetch operation: ' + error);
        }
    };

    useEffect(() => {
        callApi();
    }, []);

    return (
        <div className="query-options">
            <input
                id="price-bar-min"
                type="number"
                min="0"
                value={lowerPice}
                onChange={(e) => setLowerPrice(e.target.value)}
                placeholder="MinVal"
            />
            <input
                id="price-bar-max"
                type="number"
                min="0"
                value={upperPrice}
                onChange={(e) => setUpperPrice(e.target.value)}
                placeholder="MaxVal"
             /> 
            <select id="category-dropdown">
                <option value="">--Select--</option>
                {category.map((option, index) => (
                    <option key={index} value={option}>
                        {option}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default QueryPrice;
