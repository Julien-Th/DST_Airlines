-- Création de la table airlines

CREATE TABLE IF NOT EXISTS airlines (
    airline_id   	VARCHAR(10) NOT NULL PRIMARY KEY,
    airline_name 	VARCHAR(100),
    language_code   VARCHAR(10) NOT NULL,

    -- Clé étrangère vers table airlines
    CONSTRAINT fk_language_code
        FOREIGN KEY (language_code)
        REFERENCES language(language_code)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);
