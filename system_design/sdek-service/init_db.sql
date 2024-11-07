-- Создание базы данных
CREATE DATABASE archdb;

-- Подключение к базе данных
\c archdb;

-- Создание таблицы пользователей с полями для хранения хешированного пароля
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индекс для быстрого поиска по имени пользователя
CREATE INDEX IF NOT EXISTS idx_username ON users(username);

-- Создание таблицы для товаров
CREATE TABLE IF NOT EXISTS packages (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    height FLOAT NOT NULL,
    width FLOAT NOT NULL,
    long FLOAT NOT NULL,
    weight FLOAT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_user_id ON packages(user_id);


-- Тестовые данные
INSERT INTO users (username, email, password, age) VALUES 
('admin', 'admin@example.com', '$2b$12$DFKswboZoqOSSKQn78yZMe87qgAMHsUZ.Zvqs98MIqbraZgfZeTdS', 8)
ON CONFLICT DO NOTHING;

INSERT INTO users (username, email, password, age) VALUES
('alice', 'alice@example.com', '$2b$12$KIX/1Q0B1gYH3C8.x0ZQ1Oe1fS0f8s7H9r9a5e6q2gG1H5Xv4e5kO', 25),
('bob', 'bob@example.com', '$2b$12$D9U1Zc4F3lW4uD9gF3lW6uOe7f5s8s7H9r9a5e6q2gG1H5Xv4e5kO', 30),
('charlie', 'charlie@example.com', '$2b$12$A3L2F0Q0B1gYH3C8.x0ZQ1Oe1fS0f8s7H9r9a5e6q2gG1H5Xv4e5kO', 22),
('dave', 'dave@example.com', '$2b$12$E5U2Zc4F3lW4uD9gF3lW6uOe7f5s8s7H9r9a5e6q2gG1H5Xv4e5kO', 28),
('eve', 'eve@example.com', '$2b$12$F7U3Zc4F3lW4uD9gF3lW6uOe7f5s8s7H9r9a5e6q2gG1H5Xv4e5kO', 27),
('frank', 'frank@example.com', '$2b$12$G8U4Zc4F3lW4uD9gF3lW6uOe7f5s8s7H9r9a5e6q2gG1H5Xv4e5kO', 35),
('grace', 'grace@example.com', '$2b$12$H9U5Zc4F3lW4uD9gF3lW6uOe7f5s8s7H9r9a5e6q2gG1H5Xv4e5kO', 29),
('heidi', 'heidi@example.com', '$2b$12$I0U6Zc4F3lW4uD9gF3lW6uOe7f5s8s7H9r9a5e6q2gG1H5Xv4e5kO', 33),
('ivan', 'ivan@example.com', '$2b$12$J1U7Zc4F3lW4uD9gF3lW6uOe7f5s8s7H9r9a5e6q2gG1H5Xv4e5kO', 31),
('judy', 'judy@example.com', '$2b$12$K2U8Zc4F3lW4uD9gF3lW6uOe7f5s8s7H9r9a5e6q2gG1H5Xv4e5kO', 26);
