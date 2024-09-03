import React, { ChangeEvent, useEffect, useState } from "react";
import { ProductListDefault, ProductListDetailed } from "../ProductComponents/ListComponent";
import { FetchData } from "./FetchComponent";
import { Product } from "../ProductComponents/ProductInterface";
import interpretPath from "./InterpretPathFunc";

interface userQueryProp {
    userQuery: string;
    productDisplayType: string
}

interface SwitchComponentProps {
    displayType: string;
    fetchedData: Product[];
}

const PopulateComponent: React.FC<userQueryProp> = ({ productDisplayType, userQuery }) => {
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
        callApi(userQuery)
      }, [userQuery]); 

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

    //make it a switch statement
    return (
        <div>
            {
                <ContextComponent displayType={productDisplayType} fetchedData={fetchedData}></ContextComponent>
            }
        </div>
    )
}

export default PopulateComponent