import pandas as pd
import tqdm
from pyarabic.araby import strip_tashkeel
from utility import tarabic_name, hadith_number_name, strip_punctuation, english_name

# Load the dictionary of animals from a CSV file
ANIMALS_DICTIONARY_PATH = 'dictionaries/animals.csv'
df_animals = pd.read_csv(ANIMALS_DICTIONARY_PATH)

# Function to find animals mentioned in a single hadith
def find_animals_in_one_hadith(ar_text, en_text, df=df_animals):
    """
    Identifies animals mentioned in a single hadith using Arabic and English patterns.

    Args:
        ar_text (str): The Arabic text of the hadith.
        en_text (str): The English translation of the hadith.
        df (pd.DataFrame): The DataFrame containing animal patterns and IDs.

    Returns:
        list: A list of IDs corresponding to animals mentioned in the hadith.
    """
    # Preprocess Arabic and English texts
    ar_text = strip_punctuation(ar_text)
    en_text = strip_punctuation(en_text)
    ar_text = strip_tashkeel(ar_text)

    animals_list = []

    # Iterate through the animal dictionary to find matches
    for _, row in df.iterrows():
        # Check for matches in the English text
        en_patterns = row['en'].split('-')  # Split patterns for matching
        is_match_en = any(pattern.lower() in en_text.lower() for pattern in en_patterns)

        if is_match_en:
            animals_list.append(row['ID'])

    return animals_list

# Function to find animals mentioned in all hadith
def find_animals_mentioned_in_all_hadith(hadith_df, save_result=False, save_file_path=""):
    """
    Identifies animals mentioned in all hadith within the dataset.

    Args:
        hadith_df (pd.DataFrame): DataFrame containing hadith texts in Arabic and English.
        save_result (bool, optional): Whether to save the results to an Excel file. Defaults to False.
        save_file_path (str, optional): File path to save the results. Defaults to "".

    Returns:
        pd.DataFrame: DataFrame with hadith numbers and corresponding animal mentions.
    """
    all_animals = []
    all_mentioned_ids = []
    all_hadith_numbers = []

    # Iterate through the hadith dataset with a progress bar
    with tqdm.tqdm(total=len(hadith_df), desc="Extracting animals") as pbar:
        for _, row in hadith_df.iterrows():
            # Extract Arabic and English text
            arabic_text = row[tarabic_name]
            english_text = row[english_name]

            # Find animals mentioned in the current hadith
            animals_in_hadith = find_animals_in_one_hadith(arabic_text, english_text)

            # Append results
            all_animals.append(animals_in_hadith)
            all_mentioned_ids.extend(animals_in_hadith)
            all_hadith_numbers.append(row[hadith_number_name])

            pbar.update(1)

    # Log summary statistics
    print(f"Total hadith processed: {len(all_animals)}")
    print(f"Total unique animals mentioned: {len(set(all_mentioned_ids))}")
    print(f"Unique animal IDs: {set(all_mentioned_ids)}")

    # Create a DataFrame to store results
    result_df = pd.DataFrame({
        "hadith_number": all_hadith_numbers,
        "animals": all_animals,
    })

    # Save results to an Excel file if requested
    if save_result and save_file_path:
        result_df.to_excel(save_file_path, index=False)
        print(f"Results saved to {save_file_path}")

    return result_df
