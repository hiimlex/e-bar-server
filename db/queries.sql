-- Selecionar todos os produtos
SELECT * FROM products;

-- Selecionar todos os garçons
SELECT * FROM waiters;

-- Selecionar todas as mesas
SELECT * FROM `tables`;

-- Selecionar todos os pedidos
SELECT * FROM orders;
-- Selecioanr todos os pedidos, mapeando os produtos, calculando o total

SELECT * FROM order_products;

SELECT
    o.id,
    o.waiter_id,
    o.table_id,
    w.name AS waiter_name,
    SUM(p.price * op.quantity) AS total,
    o.payment_method,
    o.status,
    o.finalized_at,
    o.created_at,
    o.updated_at,
    CASE
        WHEN COUNT(op.order_id) > 0 THEN
            JSON_ARRAYAGG(
                JSON_OBJECT(
                    'product_id', p.id,
                    'name', p.name,
                    'image_url', p.image_url,
                    'category', p.category,
                    'price', p.price,
                    'quantity', op.quantity,
                    'status', op.status
                )
            )
        ELSE
            NULL  -- or any default value you prefer, like '[]'
    END AS products
FROM
    orders o
LEFT JOIN
    order_products op ON o.id = op.order_id
LEFT JOIN
    products p ON op.product_id = p.id
LEFT JOIN
    waiters w ON o.waiter_id = w.id
GROUP BY
    o.id;

