import React, { useEffect, useState } from "react";
import PopulateComponent from "../UtilityComponents/PopulatePageComponent";
import Navbar from "../UtilityComponents/NavbarComponent";
import QueryPrice from "../UtilityComponents/QueryingComponent";
import "../ProductSearch.css"

const Products: React.FC = () => {
    const [userQuery, setUserQuery] = useState<string>('');
    const [selectedValue, setSelectedValue] = useState<string>('')
    const [selectedPage, setSelectedPage] = useState<number>(1)
    const [lowerPrice, setLowerPrice] = useState<string>('')
    const [upperPrice, setUpperPrice] = useState<string>('')
    const [categories, setCategory] = useState<string[]>([])
    const [selectedCategory, setSelectedCategory] = useState<string>('')
    const [selectedOrder, setSelectedOrder] = useState<string>('')

    return (
        <div className="product-component">
            <p>selected ordering is: {selectedOrder}</p>
            <Navbar displayType="withFullFeatures" userQuery={userQuery} setUserQuery={setUserQuery} 
            selectedValue={selectedValue} setSelectedValue={setSelectedValue}
            selectedPage={selectedPage} setSelectedPage={setSelectedPage} />

            <div className="main-page-div">
                <QueryPrice lowerPice={lowerPrice} upperPrice={upperPrice} 
                setLowerPrice={setLowerPrice} setUpperPrice={setUpperPrice} 
                categories={categories} setCategories={setCategory} 
                selectedCategory={selectedCategory} setSelectedCategory={setSelectedCategory}
                selectedOrder={selectedOrder} setSelectedOrder={setSelectedOrder}/>

                <PopulateComponent productDisplayType="default" queryType='withCategoryAndOrdering' userQuery={userQuery} 
                selectedValue={selectedValue} selectedPage={selectedPage}
                lowerPrice={lowerPrice} upperPrice={upperPrice} category={selectedCategory} selectedOrder={selectedOrder}/>
            
            </div>

            <Navbar displayType="withOnlyButtons" userQuery={userQuery} setUserQuery={setUserQuery} 
            selectedValue={selectedValue} setSelectedValue={setSelectedValue}
            selectedPage={selectedPage} setSelectedPage={setSelectedPage} />
        </div>
    )
}

export default Products