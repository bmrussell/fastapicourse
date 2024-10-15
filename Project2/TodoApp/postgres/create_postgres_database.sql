-- Postgresql

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS todos;

CREATE TABLE users (
  id SERIAL,
  email varchar(200) DEFAULT NULL,
  username varchar(45) DEFAULT NULL,
  first_name varchar(45) DEFAULT NULL,
  last_name varchar(45) DEFAULT NULL,
  password_hash varchar(200) DEFAULT NULL,
  is_active boolean DEFAULT NULL,
  role varchar(45) DEFAULT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE todos (
  id SERIAL,
  title varchar(200) DEFAULT NULL,
  description varchar(200) DEFAULT NULL,
  priority integer  DEFAULT NULL,
  complete boolean  DEFAULT NULL,
  owner_id integer  DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (owner_id) REFERENCES users(id)
);

INSERT INTO users (
    id,
    email,
    username, first_name, last_name,
    password_hash,
    is_active,
    role
  )
VALUES (
    1,
    'spiny@eed.com',
    'spiny', 'spiny', 'norman',
    '$2b$12$sXe3s28T3cZPNtz6aM44/OIS2NKhRmZaO8IfMsFgnzHRfpUQJj/xu', -- 'paasword
    true,
    'admin'
  );

-- Then
--  alembic upgrade 9f61e5cc11d1