"""
CREATE TABLE "User"
(
    id SERIAL PRIMARY KEY,
    name text NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    cash integer NOT NULL
);

CREATE TABLE "Product"
(
    id SERIAL PRIMARY KEY,
    name text NOT NULL,
    price integer NOT NULL
);

CREATE TABLE "Basket"
(
    id SERIAL PRIMARY KEY,
    busket_price int NOT NULL,
    id_user int REFERENCES "User"(id) ON DELETE CASCADE ON UPDATE CASCADE,
    id_product int REFERENCES "Product"(id) ON DELETE CASCADE ON UPDATE CASCADE
);
"""
