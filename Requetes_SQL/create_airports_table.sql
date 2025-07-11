-- Création de la table airports

CREATE TABLE IF NOT EXISTS airports (
    airport_code   VARCHAR(10) NOT NULL PRIMARY KEY,
    airport_name   VARCHAR(100),
    language_code  VARCHAR(10) NOT NULL,
    city_code      VARCHAR(10) NOT NULL,

    -- Clé étrangère vers table language
    CONSTRAINT fk_language_code
        FOREIGN KEY (language_code)
        REFERENCES language(language_code)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- Clé étrangère vers table cities
    CONSTRAINT fk_city_code
        FOREIGN KEY (city_code)
        REFERENCES cities(city_code)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);
