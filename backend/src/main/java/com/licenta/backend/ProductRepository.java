package com.licenta.backend;

import java.util.List;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

public interface ProductRepository extends CrudRepository<Product, Integer> {

    @Query(value = "SELECT * FROM products WHERE to_tsvector(name) @@ plainto_tsquery(?1)", nativeQuery = true)
    List<Product> findProductByName(String name);

    @Query(value = "SELECT * FROM products WHERE product_code LIKE ?1", nativeQuery = true)
    List<Product> findProductByProductCode(String productCode);
}
