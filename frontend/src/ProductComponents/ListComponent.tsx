import React from "react";
import { ProductComponentDefault, ProductComponentDetailed } from "./ProductComponent";
import { ProductList } from "./ProductInterface";
import "../ProductList.css"


export const ProductListDefault : React.FC<ProductList> = ( { data } ) => {
    return (
    <ul className="product-list">
        {data.map(item => (
          <ProductComponentDefault id = {item.id} name={item.name} price={item.price} 
            rating={item.rating} is_in_stock = {item.is_in_stock} url={item.url} productCode={item.productCode} 
            imagePath={item.imagePath} predictedPrice=''/>
        ))}
    </ul>
    )
}

export const ProductListDetailed : React.FC<ProductList> = ( { data } ) => {
    return (
    <ul className="product-list">
        {data.map(item => (
          <ProductComponentDetailed id = {item.id} name={item.name} price={item.price} 
            rating={item.rating} is_in_stock = {item.is_in_stock} url={item.url} productCode={item.productCode}
            imagePath={item.imagePath} predictedPrice={item.predictedPrice}/>
        ))}
        
    </ul>
    )
}

