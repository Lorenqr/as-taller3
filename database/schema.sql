-- TODO: Definir las tablas del sistema

-- Tabla de usuarios
    -- TODO: Agregar campos para id, username, email, password_hash, created_at
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de productos
    -- TODO: Agregar campos para id, name, description, price, stock, image_url, created_at
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de carritos
    -- TODO: Agregar campos para id, user_id, created_at, updated_at
CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabla de items del carrito
    -- TODO: Agregar campos para id, cart_id, product_id, quantity, added_at
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Insertar datos de prueba
INSERT INTO users (username, email, password_hash) VALUES
('ana', 'ana@email.com', 'hash1'),
('juan', 'juan@email.com', 'hash2');

INSERT INTO products (name, description, price, stock, image_url) VALUES
('Shampoo Nutritivo', 'Shampoo para cabello seco y maltratado', 25000.00, 30, 'https://ejemplo.com/shampoo.jpg'),
('Acondicionador Reparador', 'A
condicionador con keratina', 27000.00, 25, 'https://ejemplo.com/acondicionador.jpg');