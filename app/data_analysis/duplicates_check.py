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
    # Define the base directory correctly
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Define the file paths
    excel_filepath = os.path.join(basedir, '..', 'raw_data_source', 'dataset1.xlsx')
    json_filepath = os.path.join(basedir, '..', 'raw_data_source', 'dataset2.json')

    # Load data into data frames
    excel_df = load_excel_data(excel_filepath)
    json_df = load_json_data(json_filepath)

    # ----------------------------------------------------------------------------------------------------------------

    # Check for duplicates in each DataFrame

    duplicate_orders_excel = excel_df[excel_df.duplicated('ORDER_ID', keep=False)]
    duplicate_orders_json = json_df[json_df.duplicated('ORDER_ID', keep=False)]

    # Print duplicates if any
    print("Duplicate Orders in Excel DataFrame:")
    print(duplicate_orders_excel)

    print("\nDuplicate Orders in JSON DataFrame:")
    print(duplicate_orders_json)


if __name__ == "__main__":
    main()

# Final Result
# No duplicates