package com.licenta.backend;

import org.springframework.beans.factory.annotation.Autowired;
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
    @GetMapping("/products/name/searchAndPaginateCustom={productName},{limit},{page},{lowerPrice},{upperPrice}")
    public Iterable<Product> customSearch(@PathVariable String productName,
            @PathVariable int limit, @PathVariable int page, @PathVariable int lowerPrice,
            @PathVariable int upperPrice) {
        Iterable<Product> retrievedProductList;
        retrievedProductList = this.productRepository.customSearchQuery(productName, limit, page, lowerPrice,
                upperPrice);

        for (Product product : retrievedProductList) {
            System.out.println(product.toString());
        }

        System.out.println("i found the above products by id from the db!");
        return retrievedProductList;
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
}
