import pandas as pd
from tqdm import tqdm
from pyarabic.araby import strip_tashkeel
from utility import tarabic_name, hadith_number_name, strip_punctuation, english_name

# Load the dictionary of prophets
PROPHETS_DICTIONARY_PATH = 'dictionaries/prophets.xlsx'
df_prophets = pd.read_excel(PROPHETS_DICTIONARY_PATH)


def find_muhammad(ar_text):
    """
    Checks if the honorific phrase for Prophet Muhammad (PBUH) is present in the Arabic text.

    Args:
        ar_text (str): Arabic text of the hadith.

    Returns:
        bool: True if the phrase is found, False otherwise.
    """
    pattern = strip_tashkeel("صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ")
    ar_text = strip_tashkeel(ar_text)
    return pattern in ar_text


def find_prophets_in_one_hadith(ar_text, en_text, collection="sb", df=df_prophets):
    """
    Identifies mentions of prophets in a single hadith using Arabic and English patterns.

    Args:
        ar_text (str): Arabic text of the hadith.
        en_text (str): English text of the hadith.
        collection (str, optional): Collection type. Defaults to "sb".
        df (pd.DataFrame): DataFrame containing patterns and IDs for prophets.

    Returns:
        list: A list of IDs corresponding to prophets mentioned in the hadith.
    """
    # Preprocess Arabic text
    ar_text = strip_tashkeel(strip_punctuation(ar_text))

    prophets_list = []

    for _, row in df.iterrows():
        ar_patterns = strip_tashkeel(row['ar']).split(',')

        if collection == "sb":  # Handle the "sb" collection case
            en_patterns = row['en'].split(',')
            flag = any(pattern.lower() in en_text.lower() for pattern in en_patterns)
            flag = flag and any(pattern in ar_text for pattern in ar_patterns)
        else:  # Handle other collections
            flag = row['ID'] != "Adam" and any(pattern in ar_text for pattern in ar_patterns)

        if flag:
            prophets_list.append(row['ID'])

    return prophets_list


def find_prophets_mentioned_in_all_hadith(hadith_df, save_result=False, collection="sb"):
    """
    Identifies mentions of prophets across all hadith in the dataset.

    Args:
        hadith_df (pd.DataFrame): DataFrame containing hadith texts in Arabic and English.
        save_result (bool, optional): Whether to save the results to an Excel file. Defaults to False.
        collection (str, optional): Name of the collection (used for saving results). Defaults to "sb".

    Returns:
        pd.DataFrame: DataFrame with hadith numbers and corresponding prophet mentions.
    """
    all_prophets = []
    all_prophet_ids = []
    all_hadith_numbers = []

    # Iterate through the hadith dataset with a progress bar
    with tqdm(total=len(hadith_df), desc="Extracting mentions of prophets") as pbar:
        for _, row in hadith_df.iterrows():
            # Extract Arabic and English text
            arabic_text = row[tarabic_name]
            english_text = row[english_name]

            # Find prophets mentioned in the current hadith
            prophets_in_hadith = find_prophets_in_one_hadith(arabic_text, english_text, collection)

            # Append results
            all_prophets.append(prophets_in_hadith)
            all_prophet_ids.extend(prophets_in_hadith)
            all_hadith_numbers.append(row[hadith_number_name])

            pbar.update(1)

    # Log summary statistics
    print(f"Total hadith processed: {len(all_prophets)}")
    print(f"Total unique prophets mentioned: {len(set(all_prophet_ids))}")
    print(f"Unique prophet IDs: {set(all_prophet_ids)}")

    # Create a DataFrame to store results
    result_df = pd.DataFrame({
        "hadith_number": all_hadith_numbers,
        "prophets": all_prophets,
    })

    # Save results to an Excel file if requested
    if save_result:
        save_path = f"results/{collection}/prophets.xlsx"
        result_df.to_excel(save_path, index=False)
        print(f"Results saved to {save_path}")

    return result_df
