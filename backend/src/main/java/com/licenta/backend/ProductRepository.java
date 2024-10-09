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

    @Query(value= "SELECT * FROM products_lowest_price_no_dups WHERE to_tsvector(name) @@ plainto_tsquery(?1) AND raw_price BETWEEN ?4 AND ?5 AND category LIKE COALESCE(NULLIF(?6, 'undefined'), '%') AND manufacturer IN (?7) LIMIT ?2 OFFSET (?3-1) * ?2;", nativeQuery = true)
    List<Product> fetchByNamePagePriceCategoryManufacturerOrdering(String name, int limit, int page, int lowerPrice, int upperPrice,
        String category, List<String> manufacturers);

    @Query(value= "SELECT * FROM view_products_asc WHERE to_tsvector(name) @@ plainto_tsquery(?1) AND raw_price BETWEEN ?4 AND ?5 AND category LIKE COALESCE(NULLIF(?6, 'undefined'), '%') AND manufacturer IN (?7) LIMIT ?2 OFFSET (?3-1) * ?2;", nativeQuery = true)
    List<Product> fetchByNamePagePriceCategoryManufacturerOrderingAsc(String name, int limit, int page, int lowerPrice, int upperPrice,
        String category, List<String> manufacturers);

    @Query(value= "SELECT * FROM view_products_desc WHERE to_tsvector(name) @@ plainto_tsquery(?1) AND raw_price BETWEEN ?4 AND ?5 AND category LIKE COALESCE(NULLIF(?6, 'undefined'), '%') AND manufacturer IN (?7) LIMIT ?2 OFFSET (?3-1) * ?2;", nativeQuery = true)
    List<Product> fetchByNamePagePriceCategoryManufacturerOrderingDesc(String name, int limit, int page, int lowerPrice, int upperPrice,
        String category, List<String> manufacturers);

    // @Query(value = "SELECT * FROM products WHERE to_tsvector(name) @@
    // plainto_tsquery(?1) AND raw_price BETWEEN ?4 AND ?5 AND category LIKE ?6
    // LIMIT ?2 OFFSET (?3-1) * ?2")
    // List<Product> customSearchQueryByCategoryAndPriceSorted(String name, int
    // limit, int page, int lowerPrice,
    // int upperPrice,
    // String category, Sort sort);

    @Query(value = "SELECT DISTINCT manufacturer FROM products_lowest_price_no_dups WHERE to_tsvector(name) @@ plainto_tsquery(?1) AND raw_price BETWEEN ?2 AND ?3 AND category LIKE COALESCE(NULLIF(?4, 'undefined'), '%')", nativeQuery = true)
    List<String> fetchManufacturersAtPriceRange(String name, int lowerPrice,
            int upperPrice,
            String category);

    @Query(value = "SELECT * FROM products WHERE product_code LIKE ?1", nativeQuery = true)
    List<Product> findProductByProductCode(String productCode);

    @Query(value = "SELECT DISTINCT category FROM products", nativeQuery = true)
    List<String> fetchProductCategories();

    @Query(value = "SELECT * FROM price_history_view WHERE product_code LIKE ?1", nativeQuery = true)
    List<String> fetchProductHistory(String productCode);

    @Query(value = "SELECT products.* FROM products JOIN lowest_historical_price_view ON products.product_code = lowest_historical_price_view.product_code LIMIT 14;", nativeQuery = true)
    List<Product> fetchAllProductHistoryView();

    //TODO --> add limit variable so that you can dynamically select how many items to show
    @Query(value = "SELECT id, name, raw_price, raw_rating, is_in_stock, url, product_code, retailer, imagepath, category, manufacturer, predicted_price FROM products GROUP BY id, name, raw_price, raw_rating, is_in_stock, url, product_code, retailer, imagepath, category, manufacturer, predicted_price ORDER BY MAX(raw_price - predicted_price) DESC LIMIT 14;", nativeQuery = true)
    List<Product> fetchBestPredictedProducts();

    @Query(value = "SELECT CEIL(COUNT(*)::FLOAT / ?2) AS total_pages FROM products_lowest_price_no_dups WHERE to_tsvector(name) @@ plainto_tsquery(?1) AND raw_price BETWEEN ?3 AND ?4 AND category LIKE COALESCE(NULLIF(?5, 'undefined'), '%');", nativeQuery = true)
    String fetchMaxPages(String name, int limit, int lowerPrice, int upperPrice, String category, List<String> manufacturer); 
}
