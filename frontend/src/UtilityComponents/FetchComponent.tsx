import { useEffect } from "react";
import { Product} from "../ProductComponents/ProductInterface";

export const FetchData = async (query: string) : Promise<any> => {
    try {
        console.log('trying to fetch with query: ' + query);
        
        const response = await fetch(query);
        
        if (!response.ok) {
            throw new Error(`HTTP error with Status: ${response.status}`);
        }

        const result: Product[] = await response.json();
        console.log(result)
        return result
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        return []
    }

};