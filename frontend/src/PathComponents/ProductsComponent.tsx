import React, { useEffect, useState } from "react";
import Search from "../UtilityComponents/SearchComponent";
import PopulateComponent from "../UtilityComponents/PopulatePageComponent";
import Navbar from "../UtilityComponents/NavbarComponent";

const Products: React.FC = () => {
    const [userQuery, setUserQuery] = useState<string>('');
    const [selectedValue, setSelectedValue] = useState<string>('')
    const [selectedPage, setSelectedPage] = useState<number>(1)

    return (
        <div className="product-component">
            <p>selected page value is from MAIN: {selectedPage}</p>
            <Navbar userQuery={userQuery} setUserQuery={setUserQuery} 
            selectedValue={selectedValue} setSelectedValue={setSelectedValue}
            selectedPage={selectedPage} setSelectedPage={setSelectedPage} />
            <PopulateComponent productDisplayType="default" userQuery={userQuery} selectedValue={selectedValue} selectedPage={selectedPage}></PopulateComponent>
        </div>
    )
}

export default Products