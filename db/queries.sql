-- Selecionar todos os produtos
SELECT * FROM products;

-- Selecionar todos os garçons
SELECT * FROM waiters;

-- Selecionar todas as mesas
SELECT * FROM `tables`;

-- Selecionar todos os pedidos
SELECT * FROM orders;

ALTER TABLE waiters ADD is_admin BOOLEAN DEFAULT 0;

UPDATE products SET category = 'Refrigerantes' WHERE id = 14;