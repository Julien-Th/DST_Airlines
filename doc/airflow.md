# Airflow 

## Initialization
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

Connect on : IP:8080 