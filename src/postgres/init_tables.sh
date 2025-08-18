DB_USER="julien"
DB_PASSWORD="datascientest"
DB_NAME="dst_db"
DB_HOST="localhost"
DB_PORT="5432"

# path scripts init tables
SQL_SCRIPTS_DIR="init/"

# execute each script SQL
for sql_file in "$SQL_SCRIPTS_DIR"/*.sql; do
    echo "Execute $sql_file"
    docker exec -i pg_container psql -U $DB_USER -d $DB_NAME < $sql_file
done
