SELECT
    PARSE_DATE('%d/%m/%y', transaction.date) AS date
    SUM(transaction.prod_qty * transaction.prod_price) AS ventes
FROM
    `TRANSACTION` transaction
WHERE
    PARSE_DATE('%d/%m/%y', transaction.date) BETWEEN DATE(2019, 01, 01) AND DATE(2019, 12, 31)
GROUP BY
    transaction.date
ORDER BY
    PARSE_DATE('%d/%m/%y', transaction.date) ASC;