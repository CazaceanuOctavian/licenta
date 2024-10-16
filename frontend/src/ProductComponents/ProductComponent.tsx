import React from "react";
import "../ProductBox.css";

interface Product {
    id: number;
    name: string;
    price: number;
    rating: number;
    is_in_stock: boolean;
    url: string;
    productCode: string;
    imagePath: string;
    predictedPrice: string;
    
    output?: string;
    setOutput?: (query: string) => void;
}

export const ProductComponentDefault: React.FC<Product> = ({ name, price, rating, is_in_stock, productCode, imagePath }) => {
    return (
        <div className="product-info">
            <div className="upper-product">
            <h2 className="product-name">
                <a 
                href={`http://localhost:5173/products/current_product/fetch_data=${productCode}`} 
                target="_blank" 
                rel="noopener noreferrer"
                >
                {name}
                </a>
            </h2>
            <a className="img-container" href={`http://localhost:5173/products/current_product/fetch_data=${productCode}`} >
                <img 
                    src={imagePath} 
                    style={{ width: '100px', height: 'auto' }} 
                    alt="Product" 
                />
            </a>
            </div>
            <div className="middle-product">
                <p className="product-price">{price.toFixed(2)} lei</p>
                <p className="product-rating">Rating: {rating.toFixed(1)}</p>
                <p className="product-stock">
                    {is_in_stock ? 'In stoc' : 'Nu este in stoc'}
                </p>
                <p className='product-code'> Cod Produs: {productCode}</p>
            </div>
        </div>
    );
};

export const ProductComponentDetailed: React.FC<Product> = ({ name, price, rating, is_in_stock, 
    productCode, url, imagePath, predictedPrice }) => {
    return (
        <div className="product-info-detailed">
            <div className="upper-product">
                <h2 className="product-name">
                    {name}
                </h2>
                <a className="img-container" href={url}> 
                    <img 
                        src={imagePath} 
                        style={{ width: 'auto', height: 'auto' }} 
                        alt="Product" 
                    />
                </a>
            </ div>
            <div className="lower-products">
                <p className="product-price">{price.toFixed(2)} lei</p>
                <p className="predicted-price"> Pretul Prezis pentru luna viitoare: {predictedPrice}</p>
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
        </ div>
    );
};