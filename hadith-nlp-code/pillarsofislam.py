import pandas as pd
from tqdm import tqdm
from pyarabic.araby import strip_tashkeel
from utility import tarabic_name, hadith_number_name, strip_punctuation, english_name, clean_arabic_text

# Load the dictionary for pillars of Islam
PILLARS_DICTIONARY_PATH = 'dictionaries/pillars-of-islam.xlsx'
df_pillars = pd.read_excel(PILLARS_DICTIONARY_PATH)


def find_pillars_in_one_hadith(ar_text, en_text, df=df_pillars):
    """
    Identifies mentions of pillars of Islam in a single hadith using Arabic patterns.

    Args:
        ar_text (str): Arabic text of the hadith.
        en_text (str): English text of the hadith.
        df (pd.DataFrame): DataFrame containing patterns and IDs for pillars of Islam.

    Returns:
        list: A list of IDs corresponding to pillars mentioned in the hadith.
    """
    # Preprocess Arabic text
    ar_text = clean_arabic_text(strip_tashkeel(strip_punctuation(ar_text)))

    pillars_list = []

    # Check for matches in the Arabic patterns
    for _, row in df.iterrows():
        ar_patterns = strip_tashkeel(row['ar']).split(',')
        if any(pattern in ar_text for pattern in ar_patterns):
            pillars_list.append(row['ID'])

    return pillars_list


def find_pillars_mentioned_in_all_hadith(hadith_df, save_result=False, collection="sb"):
    """
    Identifies mentions of pillars of Islam across all hadith in the dataset.

    Args:
        hadith_df (pd.DataFrame): DataFrame containing hadith texts in Arabic and English.
        save_result (bool, optional): Whether to save the results to an Excel file. Defaults to False.
        collection (str, optional): Name of the collection (used for saving results). Defaults to "sb".

    Returns:
        pd.DataFrame: DataFrame with hadith numbers and corresponding pillars of Islam mentions.
    """
    all_pillars = []
    all_pillars_flat = []
    all_hadith_numbers = []

    # Iterate through the hadith dataset with a progress bar
    with tqdm(total=len(hadith_df), desc="Extracting mentions of pillars of Islam") as pbar:
        for _, row in hadith_df.iterrows():
            # Extract Arabic and English text
            arabic_text = row[tarabic_name]
            english_text = row[english_name]

            # Find pillars mentioned in the current hadith
            pillars_in_hadith = find_pillars_in_one_hadith(arabic_text, english_text)

            # Append results
            all_pillars.append(pillars_in_hadith)
            all_pillars_flat.extend(pillars_in_hadith)
            all_hadith_numbers.append(row[hadith_number_name])

            pbar.update(1)

    # Log summary statistics
    print(f"Total hadith processed: {len(all_pillars)}")
    print(f"Total unique pillars mentioned: {len(set(all_pillars_flat))}")
    print(f"Unique pillar IDs: {set(all_pillars_flat)}")

    # Create a DataFrame to store results
    result_df = pd.DataFrame({
        "hadith_number": all_hadith_numbers,
        "pillars": all_pillars,
    })

    # Save results to an Excel file if requested
    if save_result:
        save_path = f"results/{collection}/pillarsofislam.xlsx"
        result_df.to_excel(save_path, index=False)
        print(f"Results saved to {save_path}")

    return result_df
