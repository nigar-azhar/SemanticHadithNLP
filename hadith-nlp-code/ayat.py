import re
import pandas as pd
import tqdm
from utility import english_name, hadith_number_name

def extract_coordinates_values(text):
    """
    Extracts Quranic coordinates (surah and ayat) from a given text.

    Args:
        text (str): The text to search for coordinates.

    Returns:
        list: A list of tuples, where each tuple represents (surah, ayat).
    """
    # Match patterns like 75.16 or 75.16-17
    matches = re.findall(r'(\d+\.\d+(?:-\d+)?)', text)
    if not matches:
        return []

    coordinates = []

    for match in matches:
        parts = match.split('-')

        if len(parts) == 1:
            # Single ayah reference (e.g., 75.16)
            integers = match.split('.')
            coordinates.append((int(integers[0]), int(integers[1])))
        else:
            # Range of ayat (e.g., 75.16-17)
            integers = match.split('.')
            surah = int(integers[0])
            ayat_range = integers[1].split('-')
            start = int(ayat_range[0])
            end = int(ayat_range[1])

            # Add all ayat in the range
            for ayah in range(start, end + 1):
                coordinates.append((surah, ayah))

    return coordinates


def find_ayat_mentioned_in_all_hadith(hadith_df, save_result=False, collection="sb"):
    """
    Identifies Quranic ayat mentioned in all hadith within the dataset.

    Args:
        hadith_df (pd.DataFrame): DataFrame containing hadith texts in English.
        save_result (bool, optional): Whether to save the results to an Excel file. Defaults to False.
        collection (str, optional): The collection name to use for saving results. Defaults to "sb".

    Returns:
        pd.DataFrame: DataFrame with hadith numbers and corresponding ayat mentions.
    """
    all_ayat = []
    all_mentioned_coordinates = []
    all_hadith_numbers = []

    # Iterate through the hadith dataset with a progress bar
    with tqdm.tqdm(total=len(hadith_df), desc="Extracting ayat") as pbar:
        for _, row in hadith_df.iterrows():
            # Extract English text
            english_text = row[english_name]

            # Find ayat mentioned in the current hadith
            ayat_in_hadith = extract_coordinates_values(english_text)

            # Append results
            all_ayat.append(ayat_in_hadith)
            all_mentioned_coordinates.extend(ayat_in_hadith)
            all_hadith_numbers.append(row[hadith_number_name])

            pbar.update(1)

    # Log summary statistics
    print(f"Total hadith processed: {len(all_ayat)}")
    print(f"Total unique ayat mentioned: {len(set(all_mentioned_coordinates))}")
    print(f"Unique ayat coordinates: {set(all_mentioned_coordinates)}")

    # Create a DataFrame to store results
    result_df = pd.DataFrame({
        "hadith_number": all_hadith_numbers,
        "ayat": all_ayat,
    })

    # Save results to an Excel file if requested
    if save_result:
        save_path = f"results/{collection}/verses.xlsx"
        result_df.to_excel(save_path, index=False)
        print(f"Results saved to {save_path}")

    return result_df
