import React, { ChangeEvent, useEffect, useState } from "react";
import { ProductListDefault, ProductListDetailed } from "../ProductComponents/ListComponent";
import { FetchData } from "./FetchComponent";
import { Product } from "../ProductComponents/ProductInterface";
import interpretPath from "./InterpretPathFunc";

interface userQueryProp {
    userQuery: string;
    productDisplayType: string
    selectedValue?: string
    selectedPage?: number
}

interface SwitchComponentProps {
    displayType: string;
    fetchedData: Product[];
}

const PopulateComponent: React.FC<userQueryProp> = ({ productDisplayType, userQuery, selectedValue, selectedPage }) => {
    const [fetchedData, setData] = useState<Product[]>([]);
    
    let apiQuery: string = interpretPath()

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
        if (selectedValue === undefined)
            selectedValue = '20'
        if (selectedPage === undefined)
            selectedPage = 1
            callApi(userQuery + ',' + selectedValue + ',' + selectedPage)
      }, [userQuery, selectedValue, selectedPage]); 

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
        <div>
                <p>selected page value is from FUNCTION: {selectedPage}</p>
                <ContextComponent displayType={productDisplayType} fetchedData={fetchedData}></ContextComponent>
        </div>
    )
}

export default PopulateComponent