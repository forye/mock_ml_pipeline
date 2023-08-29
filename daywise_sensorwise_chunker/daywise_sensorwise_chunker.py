import argparse
import os
import pandas as pd

def report_to_observer(report_name, data):
    """
    sends an api call to the observer
    handle and logs the report to the cli

    """
    pass


class DaywiseSensorwiseChunker(object):
    def __init__(self):
        pass

    def execute(self, source_filepath, destination_path,
                     max_sensors_per_files=1000, max_days_per_file=30,donesign='done_dsc'):
        for file_name in os.listdir(source_filepath):
            if file_name.endswith('.csv') and donesign not in file_name:
                self.execute_file(self, source_filepath, destination_path,
                             max_sensors_per_files, max_days_per_file,donesign)

    def execute_file(self, source_filepath, destination_path,
                max_sensors_per_files=1000, max_days_per_file=30, donesign='done_dsc'):

        # Read the source CSV file into a DataFrame
        df = pd.read_csv(source_filepath, index_col=0)

        # Convert timestamp column to datetime type
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Create the destination directory if it doesn't exist
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
            report_to_observer('DSC_file system', str(destination_path) + 'was created')

        # Get unique sensor IDs
        unique_sensors = df.index.unique()

        # Initialize counters for the output files
        sensor_file_count = 0
        day_file_count = 0

        # Loop through unique sensor IDs in chunks
        for i in range(0, len(unique_sensors), max_sensors_per_files):
            sensor_chunk = unique_sensors[i:i + max_sensors_per_files]
            sensor_df = df[df.index.isin(sensor_chunk)]

            # Sort by timestamp to make it easier to split by date
            sensor_df.sort_values('timestamp', inplace=True)

            # Get the minimum and maximum dates
            min_date = sensor_df['timestamp'].min()
            max_date = sensor_df['timestamp'].max()

            # Initialize end_date for day loop
            end_date = max_date

            while end_date >= min_date:
                start_date = end_date - pd.Timedelta(days=max_days_per_file)

                # Slice DataFrame between start_date and end_date
                time_slice_df = sensor_df[(sensor_df['timestamp'] >= start_date) &
                                          (sensor_df['timestamp'] <= end_date)]

                # Save this chunk to a CSV file if it's not empty
                if not time_slice_df.empty:
                    filename = f"chunk_s{sensor_file_count}_d{day_file_count}.csv"
                    filepath = os.path.join(destination_path, filename)
                    time_slice_df.to_csv(filepath)
                    day_file_count += 1
                    report_to_observer('DSC_file', f' file {filepath} was created')

                # Update end_date for the next iteration
                end_date = start_date

            sensor_file_count += 1



        # mark file as done
        new_name = source_filepath.replace('.csv', donesign + '.csv')
        os.rename(source_filepath, new_name)
        report_to_observer('DSC_file system', source_filepath + 'was renamed to' + new_name)


def main():
    parser = argparse.ArgumentParser(description='Run DailySensorChunker.')
    parser.add_argument('--source_file', type=str, required=True,
                        help='Path to the source file.')
    parser.add_argument('--destination_path', type=str, required=True,
                        help='Path to the destination folder.')
    parser.add_argument('--max_sensors_per_files', type=int, default=1000,
                        help='Maximum number of sensors per file.')
    parser.add_argument('--max_days_per_file', type=int, default=30,
                        help='Maximum number of days per file.')
    parser.add_argument('--donesign', type=str, default='done_dsc',
                        help='File name suffix for completed chunks.')
    args = parser.parse_args()

    chunker = DaywiseSensorwiseChunker()
    chunker.execute(args.source_file, args.destination_path,
                     args.max_sensors_per_files, args.max_days_per_file,
                     args.donesign)

if __name__ == '__main__':
    main()