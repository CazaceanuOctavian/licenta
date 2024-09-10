import React, { useEffect, useState } from "react";
import PopulateComponent from "../UtilityComponents/PopulatePageComponent";
import Navbar from "../UtilityComponents/NavbarComponent";
import QueryPrice from "../UtilityComponents/QueryingComponent";

const Products: React.FC = () => {
    const [userQuery, setUserQuery] = useState<string>('');
    const [selectedValue, setSelectedValue] = useState<string>('')
    const [selectedPage, setSelectedPage] = useState<number>(1)
    const [lowerPrice, setLowerPrice] = useState<string>('')
    const [upperPrice, setUpperPrice] = useState<string>('')
    const [category, setCategory] = useState<string[]>([])

    return (
        <div className="product-component">
            <p>selected elements on page from MAIN is: {selectedValue}</p>
            <p>selected page value from MAIN is: {selectedPage}</p>
            <p>selected price values from MAIN are: {lowerPrice} , {upperPrice}</p>
            <p>current selected category from MAIN is: {category}</p>

            <Navbar userQuery={userQuery} setUserQuery={setUserQuery} 
            selectedValue={selectedValue} setSelectedValue={setSelectedValue}
            selectedPage={selectedPage} setSelectedPage={setSelectedPage} />

            <QueryPrice lowerPice={lowerPrice} upperPrice={upperPrice} 
            setLowerPrice={setLowerPrice} setUpperPrice={setUpperPrice} 
            category={category} setCategory={setCategory}/>

            <PopulateComponent productDisplayType="default" userQuery={userQuery} 
            selectedValue={selectedValue} selectedPage={selectedPage}
            lowerPrice={lowerPrice} upperPrice={upperPrice} />
        </div>
    )
}

export default Products