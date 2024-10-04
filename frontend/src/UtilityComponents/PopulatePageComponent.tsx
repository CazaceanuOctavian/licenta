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
}

interface SwitchComponentProps {
    displayType: string;
    queryType: string;
    fetchedData: Product[];
}

// interface QueryComponentProps {
//     queryType: string;
//     fetchedData: Product[];
// }

const PopulateComponent: React.FC<userQueryProp> = ({ selectedOrder, queryType, productDisplayType, userQuery, selectedValue, selectedPage, lowerPrice, upperPrice, category }) => {
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
            if (selectedOrder === '')
                selectedOrder = 'undefined'
            if (category === '')
                category = 'undefined'
            //SEE HOW YOU CAN REMOVE THE HARD CODING SHIT YOU DID HERE
            callApi(userQuery + ',' + selectedValue + ',' + selectedPage + ',' + lowerPrice + ',' + upperPrice + ',' + category + ',' + selectedOrder + ',')
        }
        else {
            callApi(userQuery)
        }
      }, [userQuery, selectedValue, selectedPage, lowerPrice, upperPrice, category, selectedOrder]); 

    //TODO --> queryType switch statement might be shit, look to see if you can refactor at some point...
    const ContextComponent: React.FC<SwitchComponentProps> = ({ displayType, queryType, fetchedData }) => {
        switch(queryType) {
            case "withNoCategory":
                apiQuery = 'http://localhost:8080/products/name/searchAndPaginateCustom=';
                console.log('called withNoCategory')
                break;
            case "withCategory":
                if (category === '') {
                    apiQuery = 'http://localhost:8080/products/name/searchAndPaginateCustom=';
                    console.log('called withCategory but found no category so defaulted to withNoCategory')
                }
                else {
                    apiQuery = 'http://localhost:8080/products/name/searchAndPaginateCustomCategory=';
                    console.log('called withCategory')
                }
                break;
            case "withCategoryAndOrdering":
                apiQuery = 'http://localhost:8080/products/name/searchAndPaginateCustomCategoryAndOrdering='
                console.log('called withCategoryAndOrdering')
                break;
            case "withProductCode":
                apiQuery = 'http://localhost:8080/products/code/search=';
                console.log('called withProductCode')
                break;
        }
        //======================================================================
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
        <ContextComponent displayType={productDisplayType} queryType={queryType} fetchedData={fetchedData}></ContextComponent>
    )
}

export default PopulateComponent