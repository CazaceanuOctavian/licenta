import React, { ChangeEvent, useEffect, useState } from "react";
import { ProductListDefault, ProductListDetailed } from "./ListComponent";
import { FetchData } from "./FetchComponent";
import { Product } from "./ProductInterface";
import interpretPath from "./InterpretPathFunc";



interface userQueryProp {
    userQuery: string;
}

const PopulateComponent: React.FC<userQueryProp> = ({ userQuery }) => {
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

    return (
        <div>
            <ProductListDefault data={fetchedData} />
        </div>
    )
}

export default PopulateComponent