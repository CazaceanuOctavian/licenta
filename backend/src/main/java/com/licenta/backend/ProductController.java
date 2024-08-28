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
    @GetMapping("/products/{name}")
    public Iterable<Product> findAllProducts(@PathVariable String name) {
        Iterable<Product> retrievedProductList;
        retrievedProductList = this.productRepository.findProductByName(name);

        for (Product product : retrievedProductList) {
            System.out.println(product.toString());
        }

        System.out.println("i found stuff from the db!");
        return retrievedProductList;
    }
}
