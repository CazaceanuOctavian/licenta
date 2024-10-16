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
    @Column(name = "id")
    private Integer productId;
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
    @Column(name = "url")
    private String url;
    @Column(name = "imagepath")
    private String imagePath;
    @Column(name = "category")
    private String category;
    @Column(name = "predicted_price")
    private float predictedPrice;
    @Column(name = "manufacturer")
    private String manufacturer;

    public Product(String name, float price, boolean isInStock, byte rating, String productCode, String url,
            String imagePath, String category, float predictedPrice) {
        this.name = name;
        this.price = price;
        this.isInStock = isInStock;
        this.rating = rating;
        this.productCode = productCode;
        this.url = url;
        this.imagePath = imagePath;
        this.category = category;
        this.predictedPrice = predictedPrice;
        this.manufacturer = manufacturer;
    }

    private Product() {

    }

    public void setManufacturer(String manufacturer) {
        this.manufacturer = manufacturer;
    }

    public String getManufacturer() {
        return this.manufacturer;
    }

    public void setPredictedPrice(float newPredictedPrice) {
        this.predictedPrice = newPredictedPrice;
    }

    public float getPredictedPrice() {
        return this.predictedPrice;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getCategory() {
        return this.category;
    }

    public String getImagePath() {
        return this.imagePath;
    }

    public void setImagePath(String imagePath) {
        this.imagePath = imagePath;
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

    public void setProductCode(String productCode) {
        this.productCode = productCode;
    }

    public String getProductCode() {
        return this.productCode;
    }

    public void setId(int id) {
        this.productId = id;
    }

    public int getId() {
        return this.productId;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getUrl() {
        return this.url;
    }

    @Override
    public String toString() {
        return "Product [id=" + productId + ", name=" + name + ", price=" + price + ", isInStock=" + isInStock
                + ", rating="
                + rating + ", productCode=" + productCode + "]";
    }

}
