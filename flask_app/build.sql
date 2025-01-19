DROP TABLE IF EXISTS recettes;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS pizzas;
DROP TABLE IF EXISTS ingredients; 

CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(128) NOT NULL UNIQUE,
    username VARCHAR(128) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    pizzaiolo BOOLEAN DEFAULT FALSE,
    totp VARCHAR(32)
);

CREATE TABLE pizzas(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(20) NOT NULL,
  price FLOAT NOT NULL,
  description VARCHAR(256) 
);

CREATE TABLE ingredients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(20) NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE recettes(
    id_pizza INTEGER NOT NULL,
    id_ingredient INTEGER NOT NULL,
    FOREIGN KEY (id_pizza) REFERENCES pizzas(id),
    FOREIGN KEY (id_ingredient) REFERENCES ingredients(id),
    PRIMARY KEY (id_pizza, id_ingredient)
);
 