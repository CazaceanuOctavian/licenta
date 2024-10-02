package com.licenta.backend;

import java.util.List;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

public interface ProductRepository extends CrudRepository<Product, Integer> {
    @Query(value = "SELECT * FROM products WHERE to_tsvector(name) @@ plainto_tsquery(?1)", nativeQuery = true)
    List<Product> findProductByName(String name);

    @Query(value = "SELECT * FROM products WHERE to_tsvector(nproductsame) @@ plainto_tsquery(?1) LIMIT ?2 OFFSET (?3-1) * ?2", nativeQuery = true)
    List<Product> findProductByNameLimit(String name, int limit, int page);

    @Query(value = "SELECT * FROM products WHERE to_tsvector(name) @@ plainto_tsquery(?1) AND raw_price BETWEEN ?4 AND ?5 LIMIT ?2 OFFSET (?3-1) * ?2", nativeQuery = true)
    List<Product> customSearchQueryByPrice(String name, int limit, int page, int lowerPrice, int upperPrice);

    @Query(value = "SELECT * FROM products_lowest_price_no_dups WHERE to_tsvector(name) @@ plainto_tsquery(?1) AND raw_price BETWEEN ?4 AND ?5 AND category LIKE COALESCE(NULLIF(?6, 'undefined'), '%') LIMIT ?2 OFFSET (?3-1) * ?2", nativeQuery = true)
    List<Product> customSearchQueryByCategoryAndPrice(String name, int limit, int page, int lowerPrice, int upperPrice,
            String category);

    @Query(value = "SELECT * FROM view_products_asc WHERE to_tsvector(name) @@ plainto_tsquery(?1) AND raw_price BETWEEN ?4 AND ?5 AND category LIKE COALESCE(NULLIF(?6, 'undefined'), '%') LIMIT ?2 OFFSET (?3-1) * ?2", nativeQuery = true)
    List<Product> customSearchQueryByCategoryAndPriceAsc(String name, int limit, int page, int lowerPrice,
            int upperPrice,
            String category);

    @Query(value = "SELECT * FROM view_products_desc WHERE to_tsvector(name) @@ plainto_tsquery(?1) AND raw_price BETWEEN ?4 AND ?5 AND category LIKE COALESCE(NULLIF(?6, 'undefined'), '%') LIMIT ?2 OFFSET (?3-1) * ?2", nativeQuery = true)
    List<Product> customSearchQueryByCategoryAndPriceDesc(String name, int limit, int page, int lowerPrice,
            int upperPrice,
            String category);

    // @Query(value = "SELECT * FROM products WHERE to_tsvector(name) @@
    // plainto_tsquery(?1) AND raw_price BETWEEN ?4 AND ?5 AND category LIKE ?6
    // LIMIT ?2 OFFSET (?3-1) * ?2")
    // List<Product> customSearchQueryByCategoryAndPriceSorted(String name, int
    // limit, int page, int lowerPrice,
    // int upperPrice,
    // String category, Sort sort);

    @Query(value = "SELECT * FROM 'products' WHERE product_code LIKE ?1", nativeQuery = true)
    List<Product> findProductByProductCode(String productCode);

    @Query(value = "SELECT DISTINCT category FROM products", nativeQuery = true)
    List<String> fetchProductCategories();

    @Query(value = "SELECT * FROM price_history_view WHERE product_code LIKE ?1", nativeQuery = true)
    List<String> fetchProductHistory(String productCode);

}
