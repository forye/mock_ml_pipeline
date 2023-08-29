import argparse
from ..clustering_model import ClusteringModel


import time
import psutil

def report_to_observer(report_name, data):
    """
    sends an api call to the observer
    handle and logs the report to the cli

    """
    pass

def report_memory_status():
    memory = psutil.virtual_memory()
    total_memory_gb = memory.total/ (1024 ** 3)
    available_memory_gb = memory.available/ (1024 ** 3)
    used_memory_gb = memory.used/ (1024 ** 3)

    report_to_observer('feature_creator_filesystem', f'Total Memory: {total_memory_gb:.2f} GB')
    report_to_observer('feature_creator_filesystem', f'Available Memory: {available_memory_gb:.2f} GB')
    report_to_observer('feature_creator_filesystem', f'Used Memory: {used_memory_gb:.2f} GB')



def main():
    parser = argparse.ArgumentParser(description='Predict using ClusteringModel.')
    parser.add_argument('--source_file', type=str, required=True,
                        help='Path to the source file.')
    parser.add_argument('--model_path', type=str, required=True,
                        help='Path where trained model is saved.')
    parser.add_argument('--log_path', type=str, required=False, default=None,
                        help='Location for the predictions logs to be saved as csv.')
    parser.add_argument('--db_config', type=str, default=None,
                        help='Database configuration in the format: db_name,user,password,host,port')
    parser.add_argument('--table_name', type=str, default='cluster_predictions',
                        help='Database table name to log results in.')
    parser.add_argument('--job_id', type=int, default=int(time.time()),
                        help='Job ID to insert in the database.')
    args = parser.parse_args()

    if args.db_config:
        db_config = dict(zip(['db_name', 'user', 'password', 'host', 'port'], args.db_config.split(',')))
    else:
        db_config = None

    clustering_model = ClusteringModel(db_config)
    clustering_model._load_last_trained_model(args.model_path)
    results = clustering_model.predict_log_results(args.source_file, args.log_path, args.table_name)
    report_to_observer('clustering model prediction', clustering_model.inference(results).value_counts())
    report_memory_status()

    if args.db_config and args.table_name and args.job_id:
        clustering_model.db_connector.insert_dataframe(results, args.table_name, args.job_id)

if __name__ == '__main__':
    main()
