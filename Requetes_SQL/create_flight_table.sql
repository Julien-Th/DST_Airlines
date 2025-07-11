-- Création de la table flight

CREATE TABLE IF NOT EXISTS flight (
    flight_number          VARCHAR(20) NOT NULL,
    airport_code_depart    VARCHAR(10) NOT NULL,
    schedule_date_depart   DATE        NOT NULL,
    schedule_time_depart   TIME,
    actual_date_depart     DATE,
    actual_time_depart     TIME,
    status_code_depart     VARCHAR(10),
    airport_code_arrival   VARCHAR(10),
    schedule_date_arrival  DATE,
    schedule_time_arrival  TIME,
    actual_date_arrival    DATE,
    actual_time_arrival    TIME,
    status_code_arrival    VARCHAR(10),
    aircraft_code          VARCHAR(10),

    -- Clé primaire composée
    CONSTRAINT pk_flight PRIMARY KEY (flight_number, schedule_date_depart),

    -- Clé étrangère : aéroport de départ
    CONSTRAINT fk_airport_depart
        FOREIGN KEY (airport_code_depart)
        REFERENCES airports(airport_code)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- Clé étrangère : aéroport d’arrivée
    CONSTRAINT fk_airport_arrival
        FOREIGN KEY (airport_code_arrival)
        REFERENCES airports(airport_code)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- Clé étrangère : statut de départ
    CONSTRAINT fk_status_depart
        FOREIGN KEY (status_code_depart)
        REFERENCES status(status_code)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- Clé étrangère : statut d’arrivée
    CONSTRAINT fk_status_arrival
        FOREIGN KEY (status_code_arrival)
        REFERENCES status(status_code)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- Clé étrangère : avion utilisé
    CONSTRAINT fk_aircraft
        FOREIGN KEY (aircraft_code)
        REFERENCES aircraft(aircraft_code)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);