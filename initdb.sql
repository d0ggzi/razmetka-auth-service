CREATE TABLE IF NOT EXISTS role
(
    id       SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS users
(
    id       SERIAL PRIMARY KEY,
    email VARCHAR(50) NOT NULL UNIQUE,
    password TEXT        NOT NULL,
    name VARCHAR(50) NOT NULL,
    role_id   INT NOT NULL,
    CONSTRAINT fk_user_role_id
    FOREIGN KEY (role_id)
        REFERENCES role (id)
);

INSERT INTO role
VALUES (1, 'admin'),
       (2, 'expert'),
       (3, 'customer'),
       (4, 'assessor')
ON CONFLICT DO NOTHING;
