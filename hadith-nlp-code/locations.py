import pandas as pd
import tqdm
from pyarabic.araby import strip_tashkeel
from NERModelLoader import nlp
from utility import (
    strip_punctuation,
    Resolve_Entities,
    tarabic_name,
    hadith_number_name,
    clean_arabic_text,
)

# Utility function to get the location ID based on an Arabic name
def get_location_id(arabic_name):
    """
    Retrieves the location ID from a CSV file based on the provided Arabic name.

    Args:
        arabic_name (str): The Arabic name to search for in the locations dictionary.

    Returns:
        int or None: The location ID if found; otherwise, None.
    """
    df = pd.read_csv("dictionaries/locations.csv")
    for _, row in df.iterrows():
        # Split the 'alternatives' column into a list of possible names
        string_list = row["alternatives"].split("-")
        # Check if any alternative matches the Arabic name
        if any(substring in arabic_name for substring in string_list):
            return row["id"]
    return None


# Function to find locations mentioned in a single hadith
def find_location_in_one_hadith(arabic_text):
    """
    Identifies locations mentioned in a single hadith.

    Args:
        arabic_text (str): The text of the hadith in Arabic.

    Returns:
        set: A set of unique location IDs mentioned in the hadith.
    """
    # Preprocess the Arabic text
    arabic_text = strip_punctuation(arabic_text)
    arabic_text = strip_tashkeel(arabic_text)
    arabic_text = clean_arabic_text(arabic_text)

    # Extract entities using the NER model
    doc = nlp(arabic_text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    resolved_entities = Resolve_Entities(entities)

    # Collect location IDs for entities labeled as "LOC"
    locations = [get_location_id(entity) for entity, label in resolved_entities if label == "LOC"]
    return set(locations)


# Function to find locations mentioned in all hadith in a dataset
def find_locations_mentioned_in_all_hadith(hadith_df, save_result=False, collection="sb"):
    """
    Identifies locations mentioned in all hadith in the provided DataFrame.

    Args:
        hadith_df (pd.DataFrame): DataFrame containing hadith texts.
        save_result (bool, optional): Whether to save the result to an Excel file. Defaults to False.
        collection (str, optional): The collection name to use for saving results. Defaults to "sb".

    Returns:
        pd.DataFrame: DataFrame with hadith numbers and their corresponding locations.
    """
    all_locations = []
    all_hadith_numbers = []

    # Iterate through the hadith dataset with a progress bar
    with tqdm.tqdm(total=len(hadith_df), desc="Extracting locations") as pbar:
        for _, row in hadith_df.iterrows():
            arabic_text = row[tarabic_name]  # Extract Arabic text column
            hadith_number = row[hadith_number_name]  # Extract hadith number

            # Find locations for the current hadith
            locations = find_location_in_one_hadith(arabic_text)

            # Append results
            all_locations.append(locations)
            all_hadith_numbers.append(hadith_number)

            pbar.update(1)

    # Create a DataFrame to store results
    result_df = pd.DataFrame({
        "hadith_number": all_hadith_numbers,
        "locations": all_locations,
    })

    # Save results to an Excel file if requested
    if save_result:
        save_path = f"results/{collection}/locations.xlsx"
        result_df.to_excel(save_path, index=False)
        print(f"Results saved to {save_path}")

    return result_df
