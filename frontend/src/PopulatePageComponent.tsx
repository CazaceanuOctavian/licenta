import React, { ChangeEvent, useEffect, useState } from "react";
import { ProductListDefault, ProductListDetailed } from "./ListComponent";
import { FetchData } from "./FetchComponent";
import { Product } from "./ProductInterface";

interface userQueryProp {
    userQuery: string;
}

const PopulateComponent: React.FC<userQueryProp> = ({ userQuery }) => {
    const [fetchedData, setData] = useState<Product[]>([]);

    const callApi = async ( query: string ) => {
        try {
            const data = await FetchData(query);
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