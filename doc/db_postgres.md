## Installation
- `cd src/postgres/`
- lancer le docker : `docker-compose up -d`
- Accéder au CLI PostgreSQL qui s'exécute à l'intérieur du conteneur Docker : `docker exec -it pg_container bash`
- `psql -h localhost -U julien dst_db`

## Commandes utiles

## docker-compose.yaml

- Notre premier service utilise l'image PostgreSQL. Il crée un conteneur nommé qui va héberger la base de données
- Le second service est l'image pgadmin4, qui fournit une interface web pour gérer les bases de données
