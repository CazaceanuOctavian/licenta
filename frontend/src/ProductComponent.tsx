import React from "react";

interface Product {
    id: number;
    name: string;
    price: number;
    rating: number;
    is_in_stock: boolean;
    url: string;
    productCode: string;
}

export const ProductComponentDefault: React.FC<Product> = ( { name, price, rating, is_in_stock, productCode } ) => {
    return (
        <div className="product-info">
            <h2 className="product-name">
            <a 
            href={`http://localhost:5173/products/fetch_data=${productCode}`} 
            target="_blank" 
            rel="noopener noreferrer"
            >
            {name}
            </a>
            </h2>
            <p className="product-price">{price.toFixed(2)} lei</p>
            <p className="product-rating">Rating: {rating.toFixed(1)}</p>
            <p className="product-stock">
                {is_in_stock ? 'In stoc' : 'Nu este in stoc'}
            </p>
            <p className='product-code'> Cod Produs: {productCode}</p>
        </div>
    )
}

export const ProductComponentDetailed: React.FC<Product> = ( { name, price, rating, is_in_stock, productCode, url } ) => {
    return (
        <div className="product-info">
        <h2 className="product-name">
            {name}
        </h2>
        <p className="product-price">{price.toFixed(2)} lei</p>
        <p className="product-rating">Rating: {rating.toFixed(1)}</p>
        <p className="product-stock">
            {is_in_stock ? 'In stoc' : 'Nu este in stoc'}
        </p>
        <p className='product-code'> Cod Produs: {productCode}</p>
        <p className='origin-url'>
            Link magazin: 
            <a href={url}>                                                
                {url}
            </a> 
        </p>
    </div>
    )
}














