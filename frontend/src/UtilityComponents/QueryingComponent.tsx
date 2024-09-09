import React, { useEffect, useState } from "react";

interface SearchProps {
    lowerPice: string;
    upperPrice: string;
    setLowerPrice: (query: string) => void;
    setUpperPrice: (query: string) => void;
}

const QueryPrice: React.FC<SearchProps> = ({ lowerPice, upperPrice, setLowerPrice, setUpperPrice }) => {
    //const [lowerPice, setLowerPrice] = useState<number>(0)

    // useEffect(() => {
    //     window.addEventListener('keydown', handleKeyPress);
    //             return () => {
    //       window.removeEventListener('keydown', handleKeyPress);
    //     };
    //   }, []); 

    //   function getStringOrDefault(value: string | null): string {
    //     return value !== null ? value : "";
    // }

    // const handleKeyPress = (event: KeyboardEvent) => {
    //     if(event.key === "Enter"){
    //         var search = document.getElementById('search_bar') as HTMLInputElement;
    //         if(search){
    //             let userQuery:string = getStringOrDefault(search.value)
    //             setUserQuery(userQuery)
    //             //move to another url with page 1 as beginning
    //         }
    //     }
    //   };

    return (
        <div>
            <input id="price_bar"
                type="number"
                min="0"
                value={lowerPice}
                onChange={(e) => setLowerPrice(e.target.value)}
                placeholder="MinVal"
            />
                <input id="price_bar"
                min="0"
                type="number"
                value={upperPrice}
                onChange={(e) => setUpperPrice(e.target.value)}
                placeholder="MaxVal"
            />
        </div>
    )
}

export default QueryPrice;