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

    # Check for missing data -- Point 2

    # Check for missing values in both DataFrames
    print("\nMissing values in Excel DataFrame:")
    print(excel_df.isnull().sum())

    print("\nMissing values in JSON DataFrame:")
    print(json_df.isnull().sum())


if __name__ == "__main__":
    main()

# Final Result
# 38 rows in the excel file have n/a as the order quantity