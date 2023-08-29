import argparse
import os
import pandas as pd
import dill as dill
# from FeatureCreator import FeatureCreator
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


class FeatureCreator(object):
    def __init__(self, ftr_creator_model_path):
        with open(ftr_creator_model_path, 'rb') as f:
            self.model = dill.load(f)

    def transform(self, df):
        report_to_observer('feature_creator_transformer', f'before aggregation, file contained {df.shape[0]} rows')
        return self.model.transform(df)

    def transform_file(self, file_path):
        df = pd.read_csv(file_path)
        return self.transform(df)

    def transform_multi_file(self, files_path, destination_folder=None, res_filename=None):
        # Initialize an empty DataFrame to collect all transformed DataFrames
        combined_df = pd.DataFrame()
        cntr =0

        # Loop through all the files in the given folder
        for file_name in os.listdir(files_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(files_path, file_name)
                transformed_df = self.transform_file(file_path)
                combined_df = pd.concat([combined_df, transformed_df], ignore_index=True)
                cntr+=1
        report_memory_status()

        # Optionally, save the combined DataFrame to a new CSV file
        if destination_folder and res_filename:
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            output_path = os.path.join(destination_folder, res_filename)
            combined_df.to_csv(output_path, index=False)
            report_to_observer('feature_creator_filesystem', f'saved a combined features file to {output_path}')

        report_to_observer('feature_creator_filesystem', f'created a {combined_df.shape} df out of {cntr} files')



        return combined_df



def main():
    parser = argparse.ArgumentParser(description='Run FeatureCreator.')
    parser.add_argument('--source_files', type=str, required=True,
                        help='Path to the source files.')
    parser.add_argument('--ftrs_path', type=str, required=True,
                        help='Path where the features are saved.')
    parser.add_argument('--res_filename', type=str, required=True,
                        help='File name which the features are saved.')
    parser.add_argument('--ftr_creator_model_path', type=str, required=True,
                        help='The model that implement the creation of the features.')
    args = parser.parse_args()

    feature_creator = FeatureCreator(args.ftr_creator_model_path)

    df_transformed = feature_creator.transform_multi_file(args.source_files, args.ftrs_path, args.res_filename)
    print(df_transformed)

if __name__ == '__main__':
    main()
