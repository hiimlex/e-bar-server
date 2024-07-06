-- CREATE DATABASE social_sips
-- Use social_sips

-- Criar tabela de produtos
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(255) NOT NULL,
    stock INT NOT NULL,
    `active` BOOLEAN DEFAULT 1,
    image_url VARCHAR(400) NOT NULL
);

-- Criar tabela de garçons
CREATE TABLE waiters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `active` BOOLEAN NOT NULL DEFAULT 1,
    is_admin BOOLEAN NOT NULL DEFAULT 0
);

-- Criar tabela de mesas
CREATE TABLE `tables` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    waiter_id INT,
    `active` BOOLEAN NOT NULL DEFAULT 1,
    in_use BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (waiter_id) REFERENCES waiters(id)
);

-- Criar tabela de pedidos
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    waiter_id INT,
    table_id INT,
    total DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL DEFAULT 'pending',
    finalized_at TIMESTAMP NULL DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (waiter_id) REFERENCES waiters(id),
    FOREIGN KEY (table_id) REFERENCES tables(id)
);

-- Criar tabela de associação entre pedidos e produtos
CREATE TABLE order_products (
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    status VARCHAR(255) NOT NULL DEFAULT 'pending',
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
