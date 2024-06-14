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

    # Check for issues in the order time pst

    # Identify invalid time entries in the Excel DataFrame
    invalid_times_excel = excel_df[~excel_df['ORDER_TIME_PST'].astype(str).str.match(r'^\d{6}$')]
    invalid_times_excel_count = invalid_times_excel.shape[0]
    print("\nNumber of invalid ORDER_TIME_PST entries in Excel DataFrame:", invalid_times_excel_count)

    # Identify invalid time entries in the JSON DataFrame
    invalid_times_json = json_df[~json_df['ORDER_TIME_PST'].astype(str).str.match(r'^\d{6}$')]
    invalid_times_json_count = invalid_times_json.shape[0]
    print("Number of invalid ORDER_TIME_PST entries in JSON DataFrame:", invalid_times_json_count)


if __name__ == "__main__":
    main()

# Final Result
# all the time stamp formatting in the excel file are invalid
