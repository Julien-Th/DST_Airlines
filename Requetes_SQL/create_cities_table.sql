-- Création de la table cities

CREATE TABLE IF NOT EXISTS cities (
    city_code    VARCHAR(10) NOT NULL PRIMARY KEY,
    city_name      VARCHAR(100),
    language_code  VARCHAR(10) NOT NULL,
    country_code   VARCHAR(10) NOT NULL,

    -- Clé étrangère vers table language
    CONSTRAINT fk_language_code
        FOREIGN KEY (language_code)
        REFERENCES language(language_code)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- Clé étrangère vers table countries
    CONSTRAINT fk_country_code
        FOREIGN KEY (country_code)
        REFERENCES countries(country_code)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);
