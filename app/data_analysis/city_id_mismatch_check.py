import pandas as pd
import os


def load_json_data(filepath):
    df = pd.read_json(filepath)
    return df


def main():
    # Define the base directory correctly
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Define the file paths
    excel_filepath = os.path.join(basedir, '..', 'raw_data_source', 'dataset1.xlsx')
    json_filepath = os.path.join(basedir, '..', 'raw_data_source', 'dataset2.json')

    # Load data into data frames
    json_df = load_json_data(json_filepath)
    excel_df = pd.read_excel(excel_filepath, sheet_name='DATA')
    mapping_df = pd.read_excel(excel_filepath, sheet_name='CITY_DISTRICT_MAP')

    # Preprocess Excel Data
    excel_df.rename(columns={'ORDER_TIME  (PST)': 'ORDER_TIME_PST'}, inplace=True)
    excel_df['ORDER_TIME_PST'] = excel_df['ORDER_TIME_PST'].astype(str).str.zfill(6)
    excel_df['ORDER_TIME_PST'] = pd.to_datetime(excel_df['ORDER_TIME_PST'], format='%H%M%S', errors='coerce').dt.time
    excel_df['ORDER_QTY'] = excel_df['ORDER_QTY'].fillna(0).astype(int)
    excel_df['ORDER_ID'] = excel_df['ORDER_ID'].astype(str)
    excel_df['CITY_DISTRICT_ID'] = excel_df['CITY_DISTRICT_ID'].astype(str)
    excel_df['RPTG_AMT'] = excel_df['RPTG_AMT'].astype(float)
    excel_df['CURRENCY_CD'] = excel_df['CURRENCY_CD'].astype(str)
    excel_df['ORDER_QTY'] = excel_df['ORDER_QTY'].astype(int)
    excel_df['data_source'] = 'Excel'

    # Preprocess JSON Data
    json_df['ORDER_TIME_PST'] = pd.to_datetime(json_df['ORDER_TIME_PST'], format='%H%M%S', errors='coerce').dt.time
    json_df['ORDER_ID'] = json_df['ORDER_ID'].astype(str)
    json_df['SHIP_TO_DISTRICT_NAME'] = json_df['SHIP_TO_DISTRICT_NAME'].astype(str)
    json_df['SHIP_TO_CITY_CD'] = json_df['SHIP_TO_CITY_CD'].astype(str)
    json_df['RPTG_AMT'] = json_df['RPTG_AMT'].astype(float)
    json_df['CURRENCY_CD'] = json_df['CURRENCY_CD'].astype(str)
    json_df['ORDER_QTY'] = json_df['ORDER_QTY'].astype(int)
    json_df['data_source'] = 'JSON'

    # Ensure CITY_DISTRICT_ID in mapping_df is a string
    mapping_df['CITY_DISTRICT_ID'] = mapping_df['CITY_DISTRICT_ID'].astype(str)

    # Merge mapping dataframe with Excel DataFrame
    excel_df = pd.merge(excel_df, mapping_df, how='left', on='CITY_DISTRICT_ID')

    # Merge mapping dataframe with JSON DataFrame
    json_df = pd.merge(json_df, mapping_df, how='left', left_on=['SHIP_TO_CITY_CD', 'SHIP_TO_DISTRICT_NAME'],
                       right_on=['SHIP_TO_CITY_CD', 'SHIP_TO_DISTRICT_NAME'])

    # Combine DataFrames
    combined_df = pd.concat([excel_df, json_df], ignore_index=True)

    # Check for NaN values
    nan_columns = combined_df.columns[combined_df.isna().any()].tolist()

    print("\nColumns in Combined DataFrame with NaN values:")
    print(combined_df[nan_columns].isna().sum())

    # Print values that don't match for Excel DataFrame
    excel_missing = combined_df[(combined_df['data_source'] == 'Excel') & (combined_df['CITY_DISTRICT_ID'].isna())]
    print("\nMissing CITY_DISTRICT_ID in Excel DataFrame:")
    print(excel_missing[['ORDER_ID', 'CITY_DISTRICT_ID', 'SHIP_TO_CITY_CD', 'SHIP_TO_DISTRICT_NAME']].drop_duplicates())

    # Print values that don't match for JSON DataFrame
    json_missing = combined_df[(combined_df['data_source'] == 'JSON') & (combined_df['CITY_DISTRICT_ID'].isna())]
    print("\nMissing CITY_DISTRICT_ID in JSON DataFrame:")
    print(json_missing[['ORDER_ID', 'CITY_DISTRICT_ID', 'SHIP_TO_CITY_CD', 'SHIP_TO_DISTRICT_NAME']].drop_duplicates())


if __name__ == "__main__":
    main()
