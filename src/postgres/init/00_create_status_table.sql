-- Supprimer la table status si elle existe déjà
DROP TABLE IF EXISTS status;

-- Création de la table status
CREATE TABLE IF NOT EXISTS status (
    status_code VARCHAR(10) NOT NULL PRIMARY KEY,
    description  VARCHAR(255)
);
