from googletrans import Translator
import time


def get_unique_values(df, column_name):
    unique_values = df[column_name].unique()
    unique_values_list = unique_values.tolist()
    print(f"Number of unique values in column '{column_name}': {len(unique_values_list)}")
    return unique_values_list


def translate_individual(unique_values_list, src, dest):
    translator = Translator()
    translation_dict = {}

    for value in unique_values_list:
        if value is not None:
            retries = 0
            success = False
            while retries < 5 and not success:
                try:
                    translation = translator.translate(value, src=src, dest=dest)
                    translation_dict[translation.origin] = translation.text
                    print(f"Successfully translated {value} to {translation.text}")
                    success = True
                except Exception as e:
                    retries += 1
                    sleep_time = 10 * retries
                    print(f"Error: {e}. Retrying in {sleep_time} seconds... (Attempt {retries}/5)")
                    time.sleep(sleep_time)
                    if retries == 5:
                        print("Max retries reached. Skipping translation for:", value)

    return translation_dict


def apply_translation(df, column_name, translation_dict):
    df[column_name] = df[column_name].map(translation_dict).fillna(df[column_name])
    return df


def translate(df, column_to_translate, src, dest):
    # Translate the specified column
    unique_values_list = get_unique_values(df, column_to_translate)
    translation_dict = translate_individual(unique_values_list, src=src, dest=dest)
    translated_df = apply_translation(df, column_to_translate, translation_dict)
    return translated_df
