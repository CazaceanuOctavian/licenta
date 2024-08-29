import React from "react";
import { ProductComponentDefault, ProductComponentDetailed } from "./ProductComponent";
import { Product, ProductList } from "./ProductInterface";


export const ProductListDefault : React.FC<ProductList> = ( { data } ) => {
    return (
        <ul>
        {data.map(item => (
          <ProductComponentDefault id = {item.id} name={item.name} price={item.price} 
            rating={item.rating} is_in_stock = {item.is_in_stock} url={item.url} productCode={item.productCode} />
        ))}
    </ul>
    )
}

export const ProductListDetailed : React.FC<ProductList> = ( { data } ) => {
    return (
        <ul>
        {data.map(item => (
          <ProductComponentDetailed id = {item.id} name={item.name} price={item.price} 
            rating={item.rating} is_in_stock = {item.is_in_stock} url={item.url} productCode={item.productCode} />
        ))}
    </ul>
    )
}

