import React, { useEffect, useState } from "react";
import { FetchData } from "./FetchComponent";
import '../QueryComponent.css'
import '../ProductComponents/ManufacturerComponent'
import { ManufacturerListComponent } from "../ProductComponents/ManufacturerComponent";

interface SearchProps {
    lowerPice: string;
    upperPrice: string;
    setLowerPrice: (query: string) => void;
    setUpperPrice: (query: string) => void;
    categories: string[];
    setCategories: (query: string[]) => void;
    selectedCategory: string
    setSelectedCategory: (query: string) => void;
    selectedOrder: string
    setSelectedOrder: (query: string) =>void;
    manufacturers: string[]
    setSelecteManufacturers: (query: string[]) =>void;
    
    userQuery:string
}

const QueryPrice: React.FC<SearchProps> = ({userQuery, selectedOrder, selectedCategory, lowerPice, upperPrice, categories, manufacturers, setSelectedOrder, setLowerPrice, setUpperPrice, setCategories, setSelectedCategory, setSelecteManufacturers }) => {

    const callApiCategories = async () => {
        try {
            console.log('FROM APICALL TRYING TO FETCH: CATEGORIES');
            const data = await FetchData('http://localhost:8080/products/categories');
            const fetchedManufacutrers = await FetchData('http://localhost:8080/products/name/fetchManufacturersInPriceRange=' + userQuery + ',' + lowerPice + ',' + upperPrice + ',' + 'undefined,desc,')
            setCategories(data);
            setSelecteManufacturers(fetchedManufacutrers)
        } catch (error) {
            console.log('error with fetch operation: ' + error);
        }
    };

    const callApiManufacturers = async () => {
        try {
            console.log('FROM APICALL TRYING TO FETCH: CATEGORIES');
            const fetchedManufacutrers = await FetchData('http://localhost:8080/products/name/fetchManufacturersInPriceRange=' + userQuery + ',' + lowerPice + ',' + upperPrice + ',' + 'undefined,desc,')
            //const fetchedManufacutrers = await FetchData('http://localhost:8080/products/name/fetchManufacturersInPriceRange=laptop,20,9999,undefined,desc,')
            setSelecteManufacturers(fetchedManufacutrers)
        } catch (error) {
            console.log('error with fetch operation: ' + error);
        }
    };

    const handleCategoryChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedCategory(event.target.value);
      };

      const handleOrderChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedOrder(event.target.value);
      };

    useEffect(() => {
        callApiCategories();
        lowerPice = '0'
        upperPrice = '999999'
    }, []);

    useEffect(() => {
        callApiManufacturers();
    }, [userQuery])

    return (
        <div className="query-options">
            <p>intervalul de pret:</p>
            <div className="price-container">
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
            </div>
            <p>ordonare: </p>
            <div className="price-ordering-container">
                <select id="order-dropdown" value={selectedOrder} onChange={handleOrderChange}>
                    <option value={'undefined'}>--Select--</option>
                    <option value={'desc'}>Descrescatoare</option>
                    <option value={'asc'}>Crescatoare</option>
                </select>
            </div>
            <p>categoria de produs:</p>
            <div className="category-container">
                <select id="category-dropdown" value={selectedCategory} onChange={handleCategoryChange}>
                    <option value={'undefined'}>--Select--</option>
                    {categories.map((option, index) => (
                        <option key={index} value={option}>
                            {option}
                        </option>
                    ))}
                </select> 
            </div>
            <p>producatori: </p>
            <ManufacturerListComponent data={manufacturers}/>
        </div>
    );
    
};

export default QueryPrice;
