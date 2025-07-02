-- Création de la table countries
CREATE TABLE IF NOT EXISTS countries (
	country_code VARCHAR(10) NOT NULL PRIMARY KEY,
    Language_code VARCHAR(10) NOT NULL,
    country_name  VARCHAR(100),
-- Définir la clé étrangère vers la table "language"
	CONSTRAINT fk_language
		FOREIGN KEY (language_code)
		REFERENCES language(language_code)
		ON UPDATE CASCADE
		ON DELETE RESTRICT
);	



