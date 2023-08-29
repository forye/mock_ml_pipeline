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
    parser = argparse.ArgumentParser(description='Train ClusteringModel.')
    parser.add_argument('--source_file', type=str, required=True,
                        help='Path to the source file.')
    parser.add_argument('--model_filename_and_path', type=str, required=True,
                        help='Path where trained model pkl (dill) file is to be saved.')

    args = parser.parse_args()

    clustering_model = ClusteringModel()
    clustering_model.train_from_file(args.source_file, args.model_filename_and_path)

if __name__ == '__main__':
    main()
