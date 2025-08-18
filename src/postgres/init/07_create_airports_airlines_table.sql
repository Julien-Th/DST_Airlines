-- Création de la table airports_airlines
CREATE TABLE IF NOT EXISTS airports_airlines (
    airport_code   VARCHAR(10) NOT NULL,
    airline_id     VARCHAR(10) NOT NULL,

    -- Clé étrangère vers la table airports
    CONSTRAINT fk_airport_code
        FOREIGN KEY (airport_code)
        REFERENCES airports(airport_code)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- Clé étrangère vers la table airlines
    CONSTRAINT fk_airline_id
        FOREIGN KEY (airline_id)
        REFERENCES airlines(airline_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- Clé primaire composée
    CONSTRAINT pk_airports_airlines
        PRIMARY KEY (airport_code, airline_id)
);