from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago

with DAG(
    'sensor_data_pipeline',
    description='Sensor Data Processing Pipeline',
    # schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['prediction'],
) as dag:

    chunker = DockerOperator(
        task_id='daywise_sensorwise_chunker',
        image='daily_sensor_chunker:latest',
        api_version='auto',
        command='--source_file /data/source_data/test.csv --destination_path /data/chunker/',
        volumes=['data_volume:/data'],
    )

    feature_creator = DockerOperator(
        task_id='feature_creator',
        image='feature_creator:latest',
        api_version='auto',
        command='--source_files /data/chunker/ --ftrs_path /data/ftr_data/ --res_filename features.csv \
        --ftr_creator_model_path /data/features_creator_models/feature_creator.pkl' ,
        volumes=['data_volume:/data'],
    )

    clustering_predict = DockerOperator(
        task_id='clustering_predict',
        image='clustering_model_predict:latest',
        api_version='auto',
        command='--source_file /data/ftr_data/transformed.csv --destination_path /data/clusters_prediction/',
        volumes=['data_volume:/data'],
    )

    chunker >> feature_creator >> clustering_predict
