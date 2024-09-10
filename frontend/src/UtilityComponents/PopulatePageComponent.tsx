import React, { ChangeEvent, useEffect, useState } from "react";
import { ProductListDefault, ProductListDetailed } from "../ProductComponents/ListComponent";
import { FetchData } from "./FetchComponent";
import { Product } from "../ProductComponents/ProductInterface";

interface userQueryProp {
    userQuery: string;
    productDisplayType: string
    selectedValue?: string
    selectedPage?: number
    lowerPrice?: string
    upperPrice?: string
}

interface SwitchComponentProps {
    displayType: string;
    fetchedData: Product[];
}

const PopulateComponent: React.FC<userQueryProp> = ({ productDisplayType, userQuery, selectedValue, selectedPage, lowerPrice, upperPrice }) => {
    const [fetchedData, setData] = useState<Product[]>([]);
    
    let apiQuery: string = '';

    const callApi = async ( query: string ) => {
        try {
            console.log('FROM APICALL TRYING TO FETCH: ' + apiQuery + query)
            const data = await FetchData( apiQuery + query);
            setData(data);
        } catch (error) {
            console.log('error with fetch operation:' + error)
        }
    }
 
    useEffect(() => {
        if (window.location.href.includes('search')) {
            if (selectedValue === '')
                selectedValue = '20'
            if (selectedPage === undefined)
                selectedPage = 1
            if (lowerPrice === '')
                lowerPrice = '0'
            if (upperPrice === '')
                upperPrice = '999999'
            callApi(userQuery + ',' + selectedValue + ',' + selectedPage + ',' + lowerPrice + ',' + upperPrice)
        }
        else {
            callApi(userQuery)
        }
      }, [userQuery, selectedValue, selectedPage, lowerPrice, upperPrice]); 

    const ContextComponent: React.FC<SwitchComponentProps> = ({ displayType, fetchedData }) => {
        switch (displayType) {
            case "default":
                apiQuery = 'http://localhost:8080/products/name/searchAndPaginateCustom=';
                return <ProductListDefault data={fetchedData} />;
            case "detailed":
                apiQuery = 'http://localhost:8080/products/code/search=';
                return <ProductListDetailed data={fetchedData} />;
            default:
                return null;
        }
    };

    return (
        <div>
                <ContextComponent displayType={productDisplayType} fetchedData={fetchedData}></ContextComponent>
        </div>
    )
}

export default PopulateComponent