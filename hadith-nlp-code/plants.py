import pandas as pd
from tqdm import tqdm
from pyarabic.araby import strip_tashkeel
from utility import tarabic_name, hadith_number_name, strip_punctuation, english_name

# Load the dictionary of plants
PLANTS_DICTIONARY_PATH = 'dictionaries/plants.csv'
df_plants = pd.read_csv(PLANTS_DICTIONARY_PATH)


def find_plants_in_one_hadith(ar_text, en_text, df=df_plants):
    """
    Identifies mentions of plants in a single hadith using English patterns.

    Args:
        ar_text (str): Arabic text of the hadith.
        en_text (str): English text of the hadith.
        df (pd.DataFrame): DataFrame containing patterns and IDs for plants.

    Returns:
        list: A list of IDs corresponding to plants mentioned in the hadith.
    """
    # Preprocess Arabic and English text
    ar_text = strip_tashkeel(strip_punctuation(ar_text))
    en_text = strip_punctuation(en_text)

    plant_list = []

    # Check for matches in the English patterns
    for _, row in df.iterrows():
        en_patterns = row['en'].split('-')
        if any(pattern.lower() in en_text.lower() for pattern in en_patterns):
            plant_list.append(row['ID'])

    return plant_list


def find_plants_mentioned_in_all_hadith(hadith_df, save_result=False, save_file_path=""):
    """
    Identifies mentions of plants across all hadith in the dataset.

    Args:
        hadith_df (pd.DataFrame): DataFrame containing hadith texts in Arabic and English.
        save_result (bool, optional): Whether to save the results to an Excel file. Defaults to False.
        save_file_path (str, optional): File path to save the results. Defaults to "".

    Returns:
        pd.DataFrame: DataFrame with hadith numbers and corresponding plant mentions.
    """
    all_plants = []
    all_plant_ids = []
    all_hadith_numbers = []

    # Iterate through the hadith dataset with a progress bar
    with tqdm(total=len(hadith_df), desc="Extracting mentions of plants") as pbar:
        for _, row in hadith_df.iterrows():
            # Extract Arabic and English text
            arabic_text = row[tarabic_name]
            english_text = row[english_name]

            # Find plants mentioned in the current hadith
            plants_in_hadith = find_plants_in_one_hadith(arabic_text, english_text)

            # Append results
            all_plants.append(plants_in_hadith)
            all_plant_ids.extend(plants_in_hadith)
            all_hadith_numbers.append(row[hadith_number_name])

            pbar.update(1)

    # Log summary statistics
    print(f"Total hadith processed: {len(all_plants)}")
    print(f"Total unique plants mentioned: {len(set(all_plant_ids))}")
    print(f"Unique plant IDs: {set(all_plant_ids)}")

    # Create a DataFrame to store results
    result_df = pd.DataFrame({
        "hadith_number": all_hadith_numbers,
        "plants": all_plants,
    })

    # Save results to an Excel file if requested
    if save_result and save_file_path:
        result_df.to_excel(save_file_path, index=False)
        print(f"Results saved to {save_file_path}")

    return result_df
