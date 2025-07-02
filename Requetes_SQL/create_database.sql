--Database: airlines_flight_delays

--SUPPRIMER LA BASE SI ELLE EXISTE
DROP DATABASE IF EXISTS "airlines_flight_delays";
--Créer la base
CREATE DATABASE airlines_flight_delays
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'French_France.1252' --comment trier les caractères suivant la langue ou région 
    LC_CTYPE = 'French_France.1252'   --comment classifier les caractères: majuscule, minuscule...
    LOCALE_PROVIDER = 'libc'          --indique la bibliotheque système que postgreSQL utilise pour LC_COLLATE et LC_CTYPE
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
	
COMMENT ON DATABASE airlines_flight_delays
    IS '- Base de données pour analyser les retards de vols par compagnie aérienne.
- Stockage des données de vols, Airlines, horaires et incidents.';
	