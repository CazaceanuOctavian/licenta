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

    @CrossOrigin(origins = "http://localhost:5173/")
    @GetMapping("/products/{name}")
    public Iterable<Product> findAllProducts(@PathVariable String name) {
        Iterable<Product> bigThing;
        bigThing = this.productRepository.findProductByName(name);

        for (Product product : bigThing) {
            System.out.println(product.toString());
        }

        System.out.println("i found stuff from the db!");
        return bigThing;
    }
}
