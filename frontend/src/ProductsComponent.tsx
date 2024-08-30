import React, { useEffect, useState } from "react";
import Search from "./SearchComponent";
import PopulateComponent from "./PopulatePageComponent";

const Products: React.FC = () => {
    const [userQuery, setUserQuery] = useState<string>('');
    return (
        <div className="product-component">
            <Search userQuery={userQuery} setUserQuery={setUserQuery} />
            <PopulateComponent userQuery={userQuery}></PopulateComponent>
        </div>
    )
}

export default Products