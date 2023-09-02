from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago

with DAG(
    'sensor_data_training_pipeline',
    description='Sensor Data Training Pipeline',
    # schedule_interval=None,  # Override to fit your needs
    # start_date=days_ago(1),
    # catchup=False,
    tags=['training'],
) as dag:

    chunker = DockerOperator(
        task_id='daywise_sensorwise_chunker',
        image='daily_sensor_chunker:latest',
        api_version='auto',
        command='--source_file /data/data_column/source_data/train_data.csv --destination_path /data/chunker/',
        volumes=['data_volume:/data'],
    )

    feature_creator = DockerOperator(
        task_id='feature_creator',
        image='feature_creator:latest',
        api_version='auto',
        command='--source_file /data/chunker/output.csv --destination_path /data/ftr_data/',
        volumes=['data_volume:/data'],
    )

    clustering_train = DockerOperator(
        task_id='clustering_train',
        image='clustering_model_train:latest',
        api_version='auto',
        command='--source_file /data/ftr_data/transformed.csv --model_path /data/model/',
        volumes=['data_volume:/data'],
    )

    chunker >> feature_creator >> clustering_train
