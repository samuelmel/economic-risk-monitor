CREATE TABLE raw_usuarios (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    username VARCHAR(100),
    email VARCHAR(255),
    address_street VARCHAR(255),
    address_city VARCHAR(150),
    address_zipcode VARCHAR(50),
    phone VARCHAR(100),
    website VARCHAR(255),
    company_name VARCHAR(255),
    dl_load_timestamp TIMESTAMP
);

CREATE TABLE raw_posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    body TEXT,
    dl_load_timestamp TIMESTAMP
);