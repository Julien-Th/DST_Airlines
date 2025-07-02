-- Connexion explicite à la base de données airlines_flight_delays
\c airlines_flight_delays;

-- Supprimer la table language si elle existe déjà
DROP TABLE IF EXISTS language;

-- Création de la table language
CREATE TABLE IF NOT EXISTS language (
    language_code VARCHAR(10) NOT NULL PRIMARY KEY,
    description  VARCHAR(255)
);
