package com.licenta.backend;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "products")
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Integer id;
    @Column(name = "name")
    private String name;
    @Column(name = "raw_price")
    private float price;
    @Column(name = "is_in_stock")
    private boolean isInStock;
    @Column(name = "raw_rating")
    private byte rating;
    @Column(name = "product_code")
    private String productCode;

    public Product(String name, float price, boolean isInStock, byte rating) {
        this.name = name;
        this.price = price;
        this.isInStock = isInStock;
        this.rating = rating;
    }

    private Product() {

    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public float getPrice() {
        return price;
    }

    public void setPrice(float price) {
        this.price = price;
    }

    public boolean isInStock() {
        return isInStock;
    }

    public void setInStock(boolean isInStock) {
        this.isInStock = isInStock;
    }

    public byte getRating() {
        return rating;
    }

    public void setRating(byte rating) {
        this.rating = rating;
    }

    @Override
    public String toString() {
        return "Product [id=" + id + ", name=" + name + ", price=" + price + ", isInStock=" + isInStock + ", rating="
                + rating + ", productCode=" + productCode + "]";
    }

}
