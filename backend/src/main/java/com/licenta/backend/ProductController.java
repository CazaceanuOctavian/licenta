package com.licenta.backend;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProductController {
    @Autowired
    private ProductRepository productRepository;

    @CrossOrigin(origins = "*")
    @GetMapping("/products/name/search={name}")
    public Iterable<Product> findAllProductsByName(@PathVariable String name) {
        Iterable<Product> retrievedProductList;
        retrievedProductList = this.productRepository.findProductByName(name);

        for (Product product : retrievedProductList) {
            System.out.println(product.toString());
        }

        System.out.println("i the above product by name from the db!");
        return retrievedProductList;
    }

    @CrossOrigin(origins = "*")
    @GetMapping("/products/code/search={productCode}")
    public Iterable<Product> findAllProductsByProductCode(@PathVariable String productCode) {
        Iterable<Product> retrievedProductList;
        retrievedProductList = this.productRepository.findProductByProductCode(productCode);

        for (Product product : retrievedProductList) {
            System.out.println(product.toString());
        }

        System.out.println("i found the above products by id from the db!");
        return retrievedProductList;
    }

    @CrossOrigin(origins = "*")
    @GetMapping("/products/name/searchAndPaginate={productName},{limit},{page}")
    public Iterable<Product> findAllProductsByProductNameLimit(@PathVariable String productName,
            @PathVariable int limit, @PathVariable int page) {
        Iterable<Product> retrievedProductList;
        retrievedProductList = this.productRepository.findProductByNameLimit(productName, limit, page);

        for (Product product : retrievedProductList) {
            System.out.println(product.toString());
        }

        System.out.println("i found the above products by id from the db!");
        return retrievedProductList;
    }

    @CrossOrigin(origins = "*")
    @GetMapping("/products/name/searchAndPaginateCustom={productName},{limit},{page},{lowerPrice},{upperPrice},")
    public Iterable<Product> customPaginateSearchPrice(@PathVariable String productName,
            @PathVariable int limit, @PathVariable int page, @PathVariable int lowerPrice,
            @PathVariable int upperPrice) {
        Iterable<Product> retrievedProductList;
        retrievedProductList = this.productRepository.customSearchQueryByPrice(productName, limit, page, lowerPrice,
                upperPrice);

        for (Product product : retrievedProductList) {
            System.out.println(product.toString());
        }

        System.out.println("i found the above products by id from the db!");
        return retrievedProductList;
    }

    @CrossOrigin(origins = "*")
    @GetMapping("/products/name/searchAndPaginateCustomCategory={productName},{limit},{page},{lowerPrice},{upperPrice},{category}")
    public Iterable<Product> customPaginateSearchPriceCategory(@PathVariable String productName,
            @PathVariable int limit, @PathVariable int page, @PathVariable int lowerPrice,
            @PathVariable int upperPrice, @PathVariable String category) {
        Iterable<Product> retrievedProductList;
        retrievedProductList = this.productRepository.customSearchQueryByCategoryAndPrice(productName, limit, page,
                lowerPrice,
                upperPrice, category);

        for (Product product : retrievedProductList) {
            System.out.println(product.toString());
        }

        System.out.println("i found the above products by id from the db!");
        return retrievedProductList;
    }

    @CrossOrigin(origins = "*")
    @GetMapping("/products/name/searchAndPaginateCustomCategoryAndOrdering={productName},{limit},{page},{lowerPrice},{upperPrice},{category},{order},")
    public Iterable<Product> customPaginateSearchPriceCategoryAndOrdering(
            @PathVariable String productName,
            @PathVariable int limit,
            @PathVariable int page,
            @PathVariable int lowerPrice,
            @PathVariable int upperPrice,
            @PathVariable String category,
            @PathVariable String order) {

        Iterable<Product> retrievedProductList;
        retrievedProductList = this.productRepository.customSearchQueryByCategoryAndPrice(productName, limit, page,
                lowerPrice,
                upperPrice, category);

        List<Product> productList = new ArrayList<>();
        for (Product product : retrievedProductList) {
            productList.add(product);
        }

        retrievedProductList = this.productRepository.customSearchQueryByCategoryAndPrice(productName, limit, page,
                lowerPrice,
                upperPrice, category);

        if (String.valueOf(order).equals("asc")) {
            Collections.sort(productList, new Comparator<Product>() {
                @Override
                public int compare(Product p1, Product p2) {
                    return Double.compare(p1.getPrice(), p2.getPrice());
                }
            });
        } else {
            Collections.sort(productList, new Comparator<Product>() {
                @Override
                public int compare(Product p1, Product p2) {
                    return Double.compare(p2.getPrice(), p1.getPrice());
                }
            });
        }
        for (Product product : retrievedProductList) {
            System.out.println(product.toString());
        }

        System.out.println("i found the above products by id from the db!");
        return productList;
    }

    @CrossOrigin(origins = "*")
    @GetMapping("/products/categories")
    public Iterable<String> findCategories() {
        Iterable<String> retrievedCategoryList;
        retrievedCategoryList = this.productRepository.fetchProductCategories();

        for (String category : retrievedCategoryList) {
            System.out.println(category);
        }

        System.out.println("i the above product by name from the db!");
        return retrievedCategoryList;
    }

    @CrossOrigin(origins = "*")
    @GetMapping("/products/productHistory={product_code}")
    public Iterable<String> findHistory(@PathVariable String product_code) {
        Iterable<String> retrievedCategoryList;
        retrievedCategoryList = this.productRepository.fetchProductHistory(product_code);

        for (String category : retrievedCategoryList) {
            System.out.println(category);
        }

        System.out.println("i the above product by name from the db!");
        return retrievedCategoryList;
    }

}
