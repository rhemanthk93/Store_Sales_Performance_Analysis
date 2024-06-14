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

    # Fix the order time pst in the excel file

    # Check and correct the length of ORDER_TIME_PST entries
    excel_df['ORDER_TIME_PST'] = excel_df['ORDER_TIME_PST'].astype(str).str.zfill(6)

    # Identify invalid time entries in the Excel DataFrame after padding
    invalid_times_excel = excel_df[~excel_df['ORDER_TIME_PST'].str.match(r'^\d{6}$')]
    invalid_times_excel_count = invalid_times_excel.shape[0]
    print("Number of invalid ORDER_TIME_PST entries in Excel DataFrame after padding:", invalid_times_excel_count)

    # Convert ORDER_TIME columns to datetime and ensure they are within the specified range
    excel_df['ORDER_TIME_PST'] = pd.to_datetime(excel_df['ORDER_TIME_PST'], format='%H%M%S', errors='coerce').dt.time
    json_df['ORDER_TIME_PST'] = pd.to_datetime(json_df['ORDER_TIME_PST'], format='%H%M%S', errors='coerce').dt.time

    # Capture the rows with invalid datetime conversion before dropping them
    invalid_datetime_excel_df = excel_df[excel_df['ORDER_TIME_PST'].isna()]
    invalid_datetime_json_df = json_df[json_df['ORDER_TIME_PST'].isna()]

    # Count rows before dropping NaNs
    rows_before_dropping_nan_excel = excel_df.shape[0]
    rows_before_dropping_nan_json = json_df.shape[0]

    # Drop rows with invalid datetime conversions (if any)
    excel_df = excel_df.dropna(subset=['ORDER_TIME_PST'])
    json_df = json_df.dropna(subset=['ORDER_TIME_PST'])

    # Count dropped rows
    dropped_nan_excel = rows_before_dropping_nan_excel - excel_df.shape[0]
    dropped_nan_json = rows_before_dropping_nan_json - json_df.shape[0]

    print(f"Number of rows dropped in Excel DataFrame due to invalid datetime conversion: {dropped_nan_excel}")
    print(f"Number of rows dropped in JSON DataFrame due to invalid datetime conversion: {dropped_nan_json}")

    # Print the ORDER_TIME_PST values of dropped rows due to invalid datetime conversion
    print("\nORDER_TIME_PST values of rows dropped in Excel DataFrame due to invalid datetime conversion:")
    print(invalid_datetime_excel_df['ORDER_TIME_PST'].tolist())

    print("\nORDER_TIME_PST values of rows dropped in JSON DataFrame due to invalid datetime conversion:")
    print(invalid_datetime_json_df['ORDER_TIME_PST'].tolist())


if __name__ == "__main__":
    main()

# Final Result
# even after fixing the formatting, there are 4 invalid order time values in the excel file
