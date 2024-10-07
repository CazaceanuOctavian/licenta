import React, { ChangeEvent, useEffect, useState } from "react";
import { ProductListDefault, ProductListDetailed } from "../ProductComponents/ListComponent";
import { FetchData } from "./FetchComponent";
import { Product } from "../ProductComponents/ProductInterface";

interface userQueryProp {
    userQuery: string;
    productDisplayType: string
    queryType: string
    selectedValue?: string
    selectedPage?: number
    lowerPrice?: string
    upperPrice?: string
    category?: string
    selectedOrder?: string
    selectedManufacturers?: string[]
}

interface SwitchComponentProps {
    displayType: string;
    queryType: string;
    fetchedData: Product[];
}

const PopulateComponent: React.FC<userQueryProp> = ({ selectedManufacturers, selectedOrder, queryType, productDisplayType, userQuery, selectedValue, selectedPage, lowerPrice, upperPrice, category }) => {
    const [fetchedData, setData] = useState<Product[]>([]);
    
    let apiQuery: string = '';
    let params: string = '';
    let selectedManufacturersStringify: string = ''

    const callApi = async (query: string) => {
        try {
            console.log('FROM APICALL TRYING TO FETCH: ' + query)
            const data = await FetchData(query);
            setData(data);
        } catch (error) {
            console.log('error with fetch operation:' + error)
        }
    }

    useEffect(() => {
        if (selectedValue === '')
            selectedValue = '20'
        if (selectedPage === undefined)
            selectedPage = 1
        if (lowerPrice === '')
            lowerPrice = '0'
        if (upperPrice === '')
            upperPrice = '999999'
        if (selectedOrder === '')
            selectedOrder = 'undefined'
        if (category === '')
            category = 'undefined'

        if (selectedManufacturers === undefined)
            selectedManufacturersStringify = 'undefined'
        else  {
            selectedManufacturersStringify = selectedManufacturers.join('-')
            selectedManufacturersStringify = '"' + selectedManufacturersStringify + '"' 
        }

        if (userQuery !== '') {
            switch(queryType) {
                case "withCategoryOrderingManufacturers":
                    if (selectedManufacturers?.length !== 0) {
                        apiQuery = 'http://localhost:8080/products/name/searchByNamePagePriceCategoryManufacturerOrdering='
                        params = userQuery + ',' + selectedValue + ',' +  selectedPage + ',' +  lowerPrice + ',' 
                            +  upperPrice + ',' +  category + ',' + selectedManufacturersStringify + ',' +  selectedOrder + ',';
                    }
                    else {
                        apiQuery = 'http://localhost:8080/products/name/searchAndPaginateCustomCategoryAndOrdering=' 
                        params = userQuery + ',' + selectedValue + ',' +  selectedPage + ',' +  lowerPrice + ',' 
                            +  upperPrice + ',' +  category + ',' +  selectedOrder + ',';
                    }
                    break;
                case "withProductCode":
                    apiQuery = 'http://localhost:8080/products/code/search=';
                    params = userQuery
                    break;
            }
            callApi(apiQuery + params)
        }
    }, [userQuery, selectedValue, selectedPage, lowerPrice, upperPrice, category, selectedOrder, selectedManufacturers]); 

    const ContextComponent: React.FC<SwitchComponentProps> = ({ displayType, fetchedData }) => {
        switch (displayType) {
            case "default":
                return <ProductListDefault data={fetchedData} />;
            case "detailed":
                return <ProductListDetailed data={fetchedData} />;
            default:
                return null;
        }  
    };

    return (
        <ContextComponent displayType={productDisplayType} queryType={apiQuery + params} fetchedData={fetchedData}></ContextComponent>
    )
}

export default PopulateComponent