# Airflow 

## Initialization
### Docker airflow
```
mkdir airflow
cd airflow
wget https://dst-de.s3.eu-west-3.amazonaws.com/airflow_fr/docker-compose/docker-compose.yaml
mkdir ./dags ./logs ./plugins
sudo chmod -R 777 logs/
sudo chmod -R 777 dags/
sudo chmod -R 777 plugins/
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

docker-compose up airflow-init
docker-compose up -d
docker container ls

```
### Script pour utiliser l'interface en ligne de commande de Airflow mais aussi se connecter aux containers via un shell bash ou un shell Python

```
wget https://dst-de.s3.eu-west-3.amazonaws.com/airflow_avance_fr/docker-compose/airflow.sh
chmod +x airflow.sh
```

### Connexion à l'interface web
Connect on : ```<IP_machine_Airflow>:8080```

user : ```airflow```

password : ```airflow```

### Connexion en ligne de commande
./airflow.sh bash

### Création d'un dag
Créer un fichier .py dans le dossier airflow/dags
Patienter quelques minutes pour que Airflow le prenne en compte automatiquement et qu'il apparaisse dans la liste des dags sur l'interface

### Lors d'une reconnexion (sur une autre adresse IP?), relancer les commandes
cd airflow
docker-compose up airflow-init
docker-compose up -d