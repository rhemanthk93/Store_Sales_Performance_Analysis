import pandas as pd
import os


def process_excel_data():
    # Define the base directory correctly
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Define the file paths
    excel_filepath = os.path.join(basedir, '..', 'raw_data_source', 'dataset1.xlsx')

    # Load data into a DataFrame
    excel_df = pd.read_excel(excel_filepath)

    # Step 1: Rename columns for consistency
    excel_df.rename(columns={'ORDER_TIME  (PST)': 'ORDER_TIME_PST'}, inplace=True)

    # Step 2: Pad and convert ORDER_TIME_PST column
    excel_df['ORDER_TIME_PST'] = excel_df['ORDER_TIME_PST'].astype(str).str.zfill(6)
    excel_df['ORDER_TIME_PST'] = pd.to_datetime(excel_df['ORDER_TIME_PST'], format='%H%M%S', errors='coerce').dt.time

    # Step 3: Handle invalid times by setting them to None
    excel_df['ORDER_TIME_PST'] = excel_df['ORDER_TIME_PST'].where(pd.notnull(excel_df['ORDER_TIME_PST']), None)

    # Step 4: Fill missing ORDER_QTY values with 0 before casting to int
    excel_df['ORDER_QTY'] = excel_df['ORDER_QTY'].fillna(0).astype(int)

    # Step 5: Cast columns to correct data types
    excel_df['ORDER_ID'] = excel_df['ORDER_ID'].astype(str)
    excel_df['CITY_DISTRICT_ID'] = excel_df['CITY_DISTRICT_ID'].astype(str)
    excel_df['RPTG_AMT'] = excel_df['RPTG_AMT'].astype(float)
    excel_df['CURRENCY_CD'] = excel_df['CURRENCY_CD'].astype(str)
    excel_df['ORDER_QTY'] = excel_df['ORDER_QTY'].astype(int)

    # Step 6: Add a data_source column
    excel_df['data_source'] = 'Excel'

    # Display the resulting DataFrame
    print(excel_df.head())

    return excel_df


def main():
    excel_df = process_excel_data()


if __name__ == "__main__":
    main()
