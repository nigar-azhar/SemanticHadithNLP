import pandas as pd
import tqdm
from pyarabic.araby import strip_tashkeel
from utility import tarabic_name, hadith_number_name, strip_punctuation, english_name

# Load the dictionary of caliphs from an Excel file
CALIPHS_DICTIONARY_PATH = 'dictionaries/caliphs.xlsx'
df_caliphs = pd.read_excel(CALIPHS_DICTIONARY_PATH)

# Function to find caliphs mentioned in a single hadith
def find_caliphs_in_one_hadith(ar_text, en_text, df=df_caliphs):
    """
    Identifies caliphs mentioned in a single hadith using Arabic and English patterns.

    Args:
        ar_text (str): The Arabic text of the hadith.
        en_text (str): The English translation of the hadith.
        df (pd.DataFrame): The DataFrame containing caliph patterns and IDs.

    Returns:
        list: A list of IDs corresponding to caliphs mentioned in the hadith.
    """
    # Preprocess the Arabic text
    ar_text = strip_punctuation(ar_text)
    ar_text = strip_tashkeel(ar_text)

    caliphs_list = []

    # Iterate through the caliph dictionary to find matches
    for _, row in df.iterrows():
        # Extract and process patterns from the dictionary
        ar_patterns = strip_tashkeel(row['ar']).split(',')  # Arabic patterns
        en_patterns = row['en'].split(',')  # English patterns

        # Check for matches in both Arabic and English texts
        is_match_en = any(pattern.lower() in en_text.lower() for pattern in en_patterns)
        is_match_ar = any(pattern in ar_text for pattern in ar_patterns)

        if is_match_en and is_match_ar:
            caliphs_list.append(row['ID'])

    return caliphs_list

# Function to find caliphs mentioned in all hadith
def find_caliphs_mentioned_in_all_hadith(hadith_df, save_result=False, save_file_path=""):
    """
    Identifies caliphs mentioned in all hadith within the dataset.

    Args:
        hadith_df (pd.DataFrame): DataFrame containing hadith texts in Arabic and English.
        save_result (bool, optional): Whether to save the results to an Excel file. Defaults to False.
        save_file_path (str, optional): File path to save the results. Defaults to "".

    Returns:
        pd.DataFrame: DataFrame with hadith numbers and corresponding caliph mentions.
    """
    all_caliphs = []
    all_mentioned_ids = []
    all_hadith_numbers = []

    # Iterate through the hadith dataset with a progress bar
    with tqdm.tqdm(total=len(hadith_df), desc="Extracting caliphs") as pbar:
        for _, row in hadith_df.iterrows():
            # Extract Arabic and English text
            arabic_text = row[tarabic_name]
            english_text = row[english_name]

            # Find caliphs mentioned in the current hadith
            caliphs_in_hadith = find_caliphs_in_one_hadith(arabic_text, english_text)

            # Append results
            all_caliphs.append(caliphs_in_hadith)
            all_mentioned_ids.extend(caliphs_in_hadith)
            all_hadith_numbers.append(row[hadith_number_name])

            pbar.update(1)

    # Log summary statistics
    print(f"Total hadith processed: {len(all_caliphs)}")
    print(f"Total unique caliphs mentioned: {len(set(all_mentioned_ids))}")
    print(f"Unique caliph IDs: {set(all_mentioned_ids)}")

    # Create a DataFrame to store results
    result_df = pd.DataFrame({
        "hadith_number": all_hadith_numbers,
        "caliphs": all_caliphs,
    })

    # Save results to an Excel file if requested
    if save_result and save_file_path:
        result_df.to_excel(save_file_path, index=False)
        print(f"Results saved to {save_file_path}")

    return result_df
