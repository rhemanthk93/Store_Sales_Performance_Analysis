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

    # Check for order ids that don't exist in the other -- Point 4

    # Ensure ORDER_ID columns are of the same data type (string) and strip any whitespaces
    excel_df['ORDER_ID'] = excel_df['ORDER_ID'].astype(str).str.strip()
    json_df['ORDER_ID'] = json_df['ORDER_ID'].astype(str).str.strip()

    # Extract the Order IDs
    excel_order_ids = set(excel_df['ORDER_ID'])
    json_order_ids = set(json_df['ORDER_ID'])

    # Identify order IDs that are in Excel but not in JSON
    only_in_excel = excel_order_ids - json_order_ids

    # Identify order IDs that are in JSON but not in Excel
    only_in_json = json_order_ids - excel_order_ids

    # Identify common order IDs
    common_order_ids = excel_order_ids & json_order_ids

    # Print the total number of unique order IDs in each DataFrame
    print("\nTotal number of unique Order IDs in Excel DataFrame:", len(excel_order_ids))
    print("\nTotal number of unique Order IDs in JSON DataFrame:", len(json_order_ids))

    # Print the number of unique order IDs that are only in one DataFrame
    print("\nNumber of Order IDs only in Excel DataFrame:", len(only_in_excel))
    print("\nNumber of Order IDs only in JSON DataFrame:", len(only_in_json))

    # Print the number of common order IDs
    print("\nNumber of common Order IDs in both DataFrames:", len(common_order_ids))

    # Check for mismatches and overlaps
    if only_in_excel:
        print("\nOrder IDs only in Excel DataFrame detected.")
    else:
        print("\nNo unique Order IDs only in Excel DataFrame.")

    if only_in_json:
        print("\nOrder IDs only in JSON DataFrame detected.")
    else:
        print("\nNo unique Order IDs only in JSON DataFrame.")

    if common_order_ids:
        print("\nCommon Order IDs exist between both datasets.")
    else:
        print("\nNo common Order IDs between the datasets.")


if __name__ == "__main__":
    main()

# Final Result
# No common order ids in both data sets
