-- CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Auth123';

-- CREATE DATABASE auth;

-- GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

USE auth;

CREATE TABLE IF NOT EXISTS user (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  username VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);

-- INSERT INTO user (email, username, password) VALUES ('anja@email.com', 'anja23','123');