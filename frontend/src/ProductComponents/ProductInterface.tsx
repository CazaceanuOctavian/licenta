export interface Product {
    id: number;
    name: string;
    price: number;
    rating: number;
    is_in_stock: boolean;
    url: string;
    productCode: string;
    imagePath: string;
}

export interface ProductList {
    data: Product[]
}