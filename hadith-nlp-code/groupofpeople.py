import pandas as pd
from tqdm import tqdm
from pyarabic.araby import strip_tashkeel
from utility import tarabic_name, hadith_number_name, strip_punctuation, english_name

# File paths for clan dictionaries
CLAN_DICTIONARY_PATHS = [
    'dictionaries/qo-group-of-people.xlsx',
    'dictionaries/new-group-of-people.xlsx',
]

# Load clan dictionaries into DataFrames
clan_dictionaries = [pd.read_excel(path) for path in CLAN_DICTIONARY_PATHS]


def find_clans_in_one_hadith(ar_text, en_text, dfs):
    """
    Identifies clans mentioned in a single hadith using Arabic and English patterns.

    Args:
        ar_text (str): The Arabic text of the hadith.
        en_text (str): The English translation of the hadith.
        dfs (list of pd.DataFrame): List of DataFrames containing clan patterns and IDs.

    Returns:
        list: A list of IDs corresponding to clans mentioned in the hadith.
    """
    # Preprocess Arabic text
    ar_text = strip_punctuation(ar_text)
    ar_text = strip_tashkeel(ar_text)

    clan_list = []

    # Iterate through each clan dictionary
    for df in dfs:
        for _, row in df.iterrows():
            # Extract patterns from the dictionary
            ar_patterns = strip_tashkeel(row['ar']).split(',')
            en_patterns = row['en'].split(',')

            # Check for matches in both Arabic and English texts
            is_match_ar = any(pattern in ar_text for pattern in ar_patterns)
            is_match_en = any(pattern.lower() in en_text.lower() for pattern in en_patterns)

            # Append ID if both Arabic and English patterns match
            if is_match_ar and is_match_en:
                clan_list.append(row['ID'])

    return clan_list


def find_clans_mentioned_in_all_hadith(hadith_df, save_result=False, save_file_path=""):
    """
    Identifies clans mentioned in all hadith within the dataset.

    Args:
        hadith_df (pd.DataFrame): DataFrame containing hadith texts in Arabic and English.
        save_result (bool, optional): Whether to save the results to an Excel file. Defaults to False.
        save_file_path (str, optional): File path to save the results. Defaults to "".

    Returns:
        pd.DataFrame: DataFrame with hadith numbers and corresponding clan mentions.
    """
    all_clans = []
    all_clan_ids = []
    all_hadith_numbers = []

    # Iterate through the hadith dataset with a progress bar
    with tqdm(total=len(hadith_df), desc="Extracting clan mentions") as pbar:
        for _, row in hadith_df.iterrows():
            # Extract Arabic and English text
            arabic_text = row[tarabic_name]
            english_text = row[english_name]

            # Find clans mentioned in the current hadith
            clans_in_hadith = find_clans_in_one_hadith(arabic_text, english_text, clan_dictionaries)

            # Append results
            all_clans.append(clans_in_hadith)
            all_clan_ids.extend(clans_in_hadith)
            all_hadith_numbers.append(row[hadith_number_name])

            pbar.update(1)

    # Log summary statistics
    print(f"Total hadith processed: {len(all_clans)}")
    print(f"Total unique clans mentioned: {len(set(all_clan_ids))}")
    print(f"Unique clan IDs: {set(all_clan_ids)}")

    # Create a DataFrame to store results
    result_df = pd.DataFrame({
        "hadith_number": all_hadith_numbers,
        "clans": all_clans,
    })

    # Save results to an Excel file if requested
    if save_result and save_file_path:
        result_df.to_excel(save_file_path, index=False)
        print(f"Results saved to {save_file_path}")

    return result_df
