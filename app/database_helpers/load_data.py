import pandas as pd
import os
from app import create_app, db
from app.models.order import Order
from app.utilities.translate import translate


def process_excel_data():
    # Define the base directory correctly
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Define the file paths
    excel_filepath = os.path.join(basedir, '..', 'raw_data_source', 'dataset1.xlsx')

    # Load data into DataFrames
    excel_df = pd.read_excel(excel_filepath, sheet_name='DATA')
    mapping_df = pd.read_excel(excel_filepath, sheet_name='CITY_DISTRICT_MAP')

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

    # Step 6: Merge with mapping DataFrame to get city and district names
    mapping_df['CITY_DISTRICT_ID'] = mapping_df['CITY_DISTRICT_ID'].astype(str)
    merged_df = pd.merge(excel_df, mapping_df, on='CITY_DISTRICT_ID', how='left')

    # Step 7: Add a data_source column
    merged_df['data_source'] = 'Excel'

    # # Display the resulting DataFrame
    # print(merged_df.head())
    #
    # # Print the columns to see if they have None or NaN values
    # print("\nColumns in Excel DataFrame with NaN values:")
    # print(merged_df.isna().sum())

    return merged_df


def process_json_data():
    # Define the base directory correctly
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Define the file paths
    json_filepath = os.path.join(basedir, '..', 'raw_data_source', 'dataset2.json')
    excel_filepath = os.path.join(basedir, '..', 'raw_data_source', 'dataset1.xlsx')

    # Load data into DataFrames
    json_df = pd.read_json(json_filepath)
    mapping_df = pd.read_excel(excel_filepath, sheet_name='CITY_DISTRICT_MAP')

    # Step 1: Convert ORDER_TIME_PST column
    json_df['ORDER_TIME_PST'] = pd.to_datetime(json_df['ORDER_TIME_PST'], format='%H%M%S', errors='coerce').dt.time

    # Step 2: Cast columns to correct data types
    json_df['ORDER_ID'] = json_df['ORDER_ID'].astype(str)
    json_df['SHIP_TO_DISTRICT_NAME'] = json_df['SHIP_TO_DISTRICT_NAME'].astype(str)
    json_df['SHIP_TO_CITY_CD'] = json_df['SHIP_TO_CITY_CD'].astype(str)
    json_df['RPTG_AMT'] = json_df['RPTG_AMT'].astype(float)
    json_df['CURRENCY_CD'] = json_df['CURRENCY_CD'].astype(str)
    json_df['ORDER_QTY'] = json_df['ORDER_QTY'].astype(int)

    # Step 3: Merge with mapping DataFrame to get CITY_DISTRICT_ID
    json_df = pd.merge(json_df, mapping_df, how='left',
                       left_on=['SHIP_TO_CITY_CD', 'SHIP_TO_DISTRICT_NAME'],
                       right_on=['SHIP_TO_CITY_CD', 'SHIP_TO_DISTRICT_NAME'])

    # Step 4: Add a data_source column
    json_df['data_source'] = 'JSON'

    # # Display the resulting DataFrame
    # print(json_df.head())
    #
    # # Print the columns to see if they have None or NaN values
    # print("\nColumns in Json DataFrame with NaN values:")
    # print(json_df.isna().sum())

    return json_df


def write_to_database(df):
    app = create_app()
    with app.app_context():
        for _, row in df.iterrows():
            new_order = Order(
                order_id=row['ORDER_ID'],
                order_time_pst=row['ORDER_TIME_PST'] if pd.notnull(row['ORDER_TIME_PST']) else None,
                city_district_id=row['CITY_DISTRICT_ID'] if 'CITY_DISTRICT_ID' in row and pd.notnull(
                    row['CITY_DISTRICT_ID']) else None,
                ship_to_district_name=row['SHIP_TO_DISTRICT_NAME'] if 'SHIP_TO_DISTRICT_NAME' in row and pd.notnull(
                    row['SHIP_TO_DISTRICT_NAME']) else None,
                ship_to_city_cd=row['SHIP_TO_CITY_CD'] if 'SHIP_TO_CITY_CD' in row and pd.notnull(
                    row['SHIP_TO_CITY_CD']) else None,
                rptg_amt=row['RPTG_AMT'],
                currency_cd=row['CURRENCY_CD'],
                order_qty=row['ORDER_QTY'],
                data_source=row['data_source']
            )
            db.session.add(new_order)
        db.session.commit()


def main():
    excel_df = process_excel_data()
    json_df = process_json_data()

    # Combine the DataFrames
    combined_df = pd.concat([excel_df, json_df], ignore_index=True)

    # Translate the columns
    combined_df = translate(combined_df, 'SHIP_TO_CITY_CD', src='zh-cn', dest='en')
    combined_df = translate(combined_df, 'SHIP_TO_DISTRICT_NAME', src='zh-cn', dest='en')

    write_to_database(combined_df)

    print("Successfully written data")


if __name__ == "__main__":
    main()
