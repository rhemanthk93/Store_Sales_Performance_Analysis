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

    # check if there any order times that are outside the given range of 5am to 12pm

    # Check and correct the length of ORDER_TIME_PST entries
    excel_df['ORDER_TIME_PST'] = excel_df['ORDER_TIME_PST'].astype(str).str.zfill(6)

    # Convert ORDER_TIME columns to datetime and set invalid conversions to None
    excel_df['ORDER_TIME_PST'] = pd.to_datetime(excel_df['ORDER_TIME_PST'], format='%H%M%S', errors='coerce').dt.time
    json_df['ORDER_TIME_PST'] = pd.to_datetime(json_df['ORDER_TIME_PST'], format='%H%M%S', errors='coerce').dt.time

    # Capture the rows with invalid datetime conversion
    invalid_datetime_excel_df = excel_df[excel_df['ORDER_TIME_PST'].isna()]
    invalid_datetime_json_df = json_df[json_df['ORDER_TIME_PST'].isna()]

    # Count rows before setting NaNs
    rows_before_setting_nan_excel = excel_df.shape[0]
    rows_before_setting_nan_json = json_df.shape[0]

    # Set invalid datetime conversions to None
    excel_df['ORDER_TIME_PST'] = excel_df['ORDER_TIME_PST'].where(pd.notnull(excel_df['ORDER_TIME_PST']), None)
    json_df['ORDER_TIME_PST'] = json_df['ORDER_TIME_PST'].where(pd.notnull(json_df['ORDER_TIME_PST']), None)

    # Define the time range
    start_time = pd.to_datetime("05:00:00", format='%H:%M:%S').time()
    end_time = pd.to_datetime("12:00:00", format='%H:%M:%S').time()

    # Filter data within the specified time range
    within_time_range_excel_df = excel_df[
        (excel_df['ORDER_TIME_PST'] >= start_time) & (excel_df['ORDER_TIME_PST'] <= end_time)]
    within_time_range_json_df = json_df[
        (json_df['ORDER_TIME_PST'] >= start_time) & (json_df['ORDER_TIME_PST'] <= end_time)]
    outside_time_range_excel_df = excel_df[
        (excel_df['ORDER_TIME_PST'] < start_time) | (excel_df['ORDER_TIME_PST'] > end_time)]
    outside_time_range_json_df = json_df[
        (json_df['ORDER_TIME_PST'] < start_time) | (json_df['ORDER_TIME_PST'] > end_time)]

    # Count rows within and outside the time range
    within_time_excel = within_time_range_excel_df.shape[0]
    within_time_json = within_time_range_json_df.shape[0]
    outside_time_excel = outside_time_range_excel_df.shape[0]
    outside_time_json = outside_time_range_json_df.shape[0]

    print(f"Number of rows within the time range in Excel DataFrame: {within_time_excel}")
    print(f"Number of rows within the time range in JSON DataFrame: {within_time_json}")
    print(f"Number of rows outside the time range in Excel DataFrame: {outside_time_excel}")
    print(f"Number of rows outside the time range in JSON DataFrame: {outside_time_json}")


if __name__ == "__main__":
    main()

# Final Result
# all valid order timings are within the time range specified