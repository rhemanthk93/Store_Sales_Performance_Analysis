import pandas as pd
import os


def load_excel_data(filepath):
    df = pd.read_excel(filepath)
    # print(f"Excel Data Loaded for file path: {filepath}:")
    # print(df.head())  # Display first few rows
    return df


def load_json_data(filepath):
    df = pd.read_json(filepath)
    # print(f"JSON Data Loaded for file path:{filepath}:")
    # print(df.head())  # Display first few rows
    return df


def main():
    # Define the base directory
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    # Define the file paths
    excel_filepath = os.path.join(basedir, 'raw_data_source', 'dataset1.xlsx')
    json_filepath = os.path.join(basedir, 'raw_data_source', 'dataset2.json')

    # Load data into data frames
    excel_df = load_excel_data(excel_filepath)
    json_df = load_json_data(json_filepath)

    # ----------------------------------------------------------------------------------------------------------------

    # Rename columns for consistency
    excel_df.rename(columns={'ORDER_TIME  (PST)': 'ORDER_TIME_PST'}, inplace=True)
    # print(excel_df.head())

    # ----------------------------------------------------------------------------------------------------------------

    # Validate time ranges

    # Convert the ORDER_TIME columns to datetime and ensure they are within the specified range
    excel_df['ORDER_TIME_PST'] = pd.to_datetime(excel_df['ORDER_TIME_PST'], format='%H%M%S').dt.time
    json_df['ORDER_TIME_PST'] = pd.to_datetime(json_df['ORDER_TIME_PST'], format='%H%M%S').dt.time

    # Define the time range
    start_time = pd.to_datetime("05:00:00", format='%H:%M:%S').time()
    end_time = pd.to_datetime("12:00:00", format='%H:%M:%S').time()

    # Filter data within the specified time range
    excel_df = excel_df[(excel_df['ORDER_TIME_PST'] >= start_time) & (excel_df['ORDER_TIME_PST'] <= end_time)]
    json_df = json_df[(json_df['ORDER_TIME_PST'] >= start_time) & (json_df['ORDER_TIME_PST'] <= end_time)]

    # Print the number of records within the time range
    print("\nNumber of records in Excel DataFrame within the time range:", len(excel_df))
    print("Number of records in JSON DataFrame within the time range:", len(json_df))


if __name__ == "__main__":
    main()

# Final Result
# all the time stamp formatting in the excel file are invalid
