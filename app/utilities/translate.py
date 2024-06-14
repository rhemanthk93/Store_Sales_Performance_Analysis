from googletrans import Translator


def get_unique_values(df, column_name):
    unique_values = df[column_name].unique()
    unique_values_list = unique_values.tolist()
    print(f"Number of unique values in column '{column_name}': {len(unique_values_list)}")
    return unique_values_list


def google_translate(word, code):
    translator = Translator()
    translator.raise_Exception = True
    translated = translator.translate(word, src=code, dest='en').text
    return translated


print(google_translate('乌当区', 'zh-cn'))
