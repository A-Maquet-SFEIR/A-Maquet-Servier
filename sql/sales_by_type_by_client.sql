SELECT
    transaction.client_id,
    SUM(
        IF(
            UPPER(product.product_type) = 'MEUBLE',
            transaction.prod_qty * transaction.prod_price,
            0
        )
    ) AS ventes_meuble,
    SUM(
        IF(
            UPPER(product.product_type) = 'DECO',
            transaction.prod_qty * transaction.prod_price,
            0
        )
    ) AS ventes_deco
FROM
    `TRANSACTION` transaction
LEFT OUTER JOIN
    `PRODUCT_NOMENCLATURE` product
ON
    transaction.prop_id = product.product_id
WHERE
    PARSE_DATE('%d/%m/%y', transaction.date) BETWEEN DATE(2019, 01, 01) AND DATE(2019, 12, 31)
    AND UPPER(product.product_type) IN ('MEUBLE', 'DECO')
GROUP BY
    transaction.client_id;