import React, { useEffect, useState } from "react";
import Search from "../UtilityComponents/SearchComponent";
import PopulateComponent from "../UtilityComponents/PopulatePageComponent";

const Products: React.FC = () => {
    const [userQuery, setUserQuery] = useState<string>('');
    return (
        <div className="product-component">
            <Search userQuery={userQuery} setUserQuery={setUserQuery} />
            <PopulateComponent productDisplayType="default" userQuery={userQuery}></PopulateComponent>
        </div>
    )
}

export default Products