import pandas as pd
from tqdm import tqdm
from pyarabic.araby import strip_tashkeel
from utility import tarabic_name, hadith_number_name, strip_punctuation, clean_arabic_text

# Load the dictionary of holy books
HOLYBOOKS_DICTIONARY_PATH = 'dictionaries/holybooks.xlsx'
df_holybooks = pd.read_excel(HOLYBOOKS_DICTIONARY_PATH)


def find_holybooks_in_one_hadith(ar_text, df=df_holybooks):
    """
    Identifies mentions of holy books in a single hadith using Arabic patterns.

    Args:
        ar_text (str): The Arabic text of the hadith.
        df (pd.DataFrame): DataFrame containing patterns for holy books.

    Returns:
        list: A list of IDs corresponding to holy books mentioned in the hadith.
    """
    # Preprocess Arabic text
    ar_text = clean_arabic_text(strip_tashkeel(strip_punctuation(ar_text)))

    holybooks_list = []

    # Check for matches in the Arabic patterns
    for _, row in df.iterrows():
        ar_patterns = strip_tashkeel(row['ar']).split(',')
        if any(pattern in ar_text for pattern in ar_patterns):
            holybooks_list.append(row['ID'])

    return holybooks_list


def find_holybooks_mentioned_in_all_hadith(hadith_df, save_result=False, collection="sb"):
    """
    Identifies mentions of holy books in all hadith within the dataset.

    Args:
        hadith_df (pd.DataFrame): DataFrame containing hadith texts in Arabic.
        save_result (bool, optional): Whether to save the results to an Excel file. Defaults to False.
        collection (str, optional): Name of the collection (used for saving results). Defaults to "sb".

    Returns:
        pd.DataFrame: DataFrame with hadith numbers and corresponding holy book mentions.
    """
    all_holybooks = []
    all_mentioned_ids = []
    all_hadith_numbers = []

    # Iterate through the hadith dataset with a progress bar
    with tqdm(total=len(hadith_df), desc="Extracting mentions of holy books") as pbar:
        for _, row in hadith_df.iterrows():
            # Extract Arabic text
            arabic_text = row[tarabic_name]

            # Find holy books mentioned in the current hadith
            holybooks_in_hadith = find_holybooks_in_one_hadith(arabic_text)

            # Append results
            all_holybooks.append(holybooks_in_hadith)
            all_mentioned_ids.extend(holybooks_in_hadith)
            all_hadith_numbers.append(row[hadith_number_name])

            pbar.update(1)

    # Log summary statistics
    print(f"Total hadith processed: {len(all_holybooks)}")
    print(f"Total unique holy books mentioned: {len(set(all_mentioned_ids))}")
    print(f"Unique holy book IDs: {set(all_mentioned_ids)}")

    # Create a DataFrame to store results
    result_df = pd.DataFrame({
        "hadith_number": all_hadith_numbers,
        "holy_books": all_holybooks,
    })

    # Save results to an Excel file if requested
    if save_result:
        save_path = f"results/{collection}/holybooks.xlsx"
        result_df.to_excel(save_path, index=False)
        print(f"Results saved to {save_path}")

    return result_df
