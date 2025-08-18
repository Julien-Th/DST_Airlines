-- Création de la table aircraft

CREATE TABLE IF NOT EXISTS aircraft (
    aircraft_code    VARCHAR(10) NOT NULL PRIMARY KEY,
    aircraft_name    VARCHAR(100),
    airline_id   	 VARCHAR(10) NOT NULL,

    -- Clé étrangère vers table airlines
    CONSTRAINT fk_airline_id
        FOREIGN KEY (airline_id)
        REFERENCES airlines(airline_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

