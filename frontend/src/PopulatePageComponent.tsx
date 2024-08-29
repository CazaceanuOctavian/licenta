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
    //fetch when the page loads 
    //load with most viewed elements at some point
    useEffect(() => {
        // Attach the event listener when the component mounts
        window.addEventListener('keydown', handleKeyPress);
        
        // Clean up the event listener when the component unmounts
        return () => {
          window.removeEventListener('keydown', handleKeyPress);
        };
      }, []); // Empty dependency array ensures this effect runs only once

    // const handleKeyPress = (event: ChangeEvent<HTMLInputElement>) => {
    //     if (userQuery.includes('|')) {
    //         console.log('i am handling')
    //         // let searchString = userQuery.slice(0,-1)
    //         callApi('http://localhost:8080/products/name/search=' + encodeURIComponent(userQuery))
    //     }
    // }
    function getStringOrDefault(value: string | null): string {
        return value !== null ? value : "";
    }

    const handleKeyPress = (event: KeyboardEvent) => {
        console.log('Key pressed:', event.key);
        // You can add more logic here to handle different keys
        if(event.key === "Enter"){
            var search = document.getElementById('search_bar') as HTMLInputElement;
            console.log(search)
            if(search){
                let thing:string = getStringOrDefault(search.value)
                console.log(thing)
                callApi('http://localhost:8080/products/name/search=' + encodeURIComponent(thing))
            }
            
        }
      };

    return (
        <div>
            <p>hello from populate page: {userQuery}</p>
            <ProductListDefault data={fetchedData} />
        </div>
    )
}

export default PopulateComponent