import os
import argparse
import pandas as pd
import psycopg2

import dill
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


class ClusteringModel(object):
    def __init__(self, db_config=None):
        super().__init__()

        self.db_config = db_config
        if db_config:
            self.db_connector = PostgresConnector(**db_config)

    model = None
    def _load_trained_model(self, model_path: str, model_file_name: str):
        with open(os.path.join(model_path, model_file_name), 'rb') as f:
            self.model = dill.load(f)

    def _get_last_from_path(self, model_path: str) -> list:
        """
        Sort the files in model_path by the creation time, from newest to oldest
        """
        files_with_times = []
        for filename in os.listdir(model_path):
            full_path = os.path.join(model_path, filename)
            if os.path.isfile(full_path):
                creation_time = os.path.getctime(full_path)
                files_with_times.append((creation_time, filename))
        sorted_files_with_times = sorted(files_with_times, key=lambda x: x[0], reverse=True)
        sorted_filenames = [filename for time, filename in sorted_files_with_times]
        return sorted_filenames

    def _load_last_trained_model(self, model_path: str):
        model_files = self._get_last_from_path(model_path)
        failed = True
        for model_file_name in model_files:
            try:
                self._load_trained_model(model_path, model_file_name)
                failed = False
            except Exception as ex:
                print(
                    f"exception while loading model {model_file_name} from {model_file_name}, got exception:{str(ex)}")
        if failed:
            raise Exception(f'could not load model from {model_path}')


    def train(self, df):
        self.model = self.model.train(df)
        report_to_observer('train model: training clusters distribution', self.model.inference(df).value_counts())

    def train_from_file(self, data_file_path, model_file_path):
        df = pd.read_csv(data_file_path)
        self.train(df)
        with open(model_file_path, 'wb') as f:
            dill.dump(self.model, f)
        report_to_observer('train model: model was saved on', self.model.inference(df).value_counts())


    def predict(self, df):
        results = self.model.inference(df)
        report_to_observer('prediction model: clusters distribution', results.value_counts())
        return results

    def predict_from_file(self, file_path):

        df = pd.read_csv(file_path)
        report_to_observer('clustering model: input describe', df.describe())
        return self.predict(df)

    def predict_log_results(self, file_path, log_file, table_name=None):
        # Create a DataFrame from the results (assuming results is a list or a list of lists)
        df_results = self.predict_from_file(file_path)
        df_results.to_csv(log_file, mode='a', header=False, index=False)
        if self.db_config and table_name:
            self.db_connector.insert_dataframe(df_results, table_name)
        return df_results


class PostgresConnector:
    """
    if I had more time I would use it as a seprated service
    """
    def __init__(self, db_name, user, password, host="localhost", port="5432"):
        self.conn = psycopg2.connect(database=db_name, user=user, password=password, host=host, port=port)

    def execute_query(self, query, data=None):
        cur = self.conn.cursor()
        if data:
            cur.execute(query, data)
        else:
            cur.execute(query)
        self.conn.commit()
        cur.close()

    def insert_dataframe(self, df, table_name, job_id):
        cur = self.conn.cursor()
        # Adding job_id to the columns list
        columns_with_job_id = ['job_id'] + list(df.columns)
        for index, row in df.iterrows():
            query = f"INSERT INTO {table_name} ({','.join(columns_with_job_id)}) VALUES (%s, {','.join(['%s' for _ in df.columns])});"
            # Adding job_id to the tuple of values to insert
            cur.execute(query, (job_id,) + tuple(row))
        self.conn.commit()
        cur.close()


#
# def main():
#     parser = argparse.ArgumentParser(description='Train ClusteringModel.')
#     parser.add_argument('--source_data_file', type=str, required=True,
#                         help='Path to the source data file.')
#
#     parser.add_argument('--destination_model_file', type=str, required=True,
#                         help='Path to the model pkl (dill) file.')
#
#     parser.add_argument('--db_config', type=str,
#                         help='Database configuration in the format: db_name,user,password,host,port')
#     args = parser.parse_args()
#
#     if args.db_config:
#         db_config = dict(zip(['db_name', 'user', 'password', 'host', 'port'], args.db_config.split(',')))
#     else:
#         db_config = None
#
#     clustering_model = ClusteringModel(db_config)
#     clustering_model.train_from_file(args.source_file)
#
# if __name__ == '__main__':
#     main()
