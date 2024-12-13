import pandas as pd
import tqdm
from pyarabic.araby import strip_tashkeel
from NERModelLoader import nlp
from utility import strip_punctuation, Resolve_Entities, tarabic_name, hadith_number_name

# Load the dictionary of crimes
CRIMES_DICTIONARY_PATH = "dictionaries/crimes.csv"
crime_id_df = pd.read_csv(CRIMES_DICTIONARY_PATH)

# Function to get the crime ID based on Arabic name
def get_crime_id(arabic_name):
    """
    Retrieves the crime ID from the crimes dictionary based on the provided Arabic name.

    Args:
        arabic_name (str): The Arabic name to search for in the crimes dictionary.

    Returns:
        int or None: The crime ID if found; otherwise, None.
    """
    for _, row in crime_id_df.iterrows():
        # Split the 'alternatives' column into a list of possible names
        string_list = row["alternatives"].split('-')
        # Check if any alternative matches the Arabic name
        if any(substring in arabic_name for substring in string_list):
            return row["id"]
    return None

# Function to find crimes mentioned in a single hadith
def find_crime_in_one_hadith(arabic_text):
    """
    Identifies crimes mentioned in a single hadith using NER and a crimes dictionary.

    Args:
        arabic_text (str): The text of the hadith in Arabic.

    Returns:
        set: A set of unique crime IDs mentioned in the hadith.
    """
    # Preprocess Arabic text
    arabic_text = strip_punctuation(arabic_text)
    arabic_text = strip_tashkeel(arabic_text)

    # Extract entities using the NER model
    doc = nlp(arabic_text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    resolved_entities = Resolve_Entities(entities)

    # Identify and collect crime IDs
    crimes = set()
    for entity, label in resolved_entities:
        if label == "CRIME":
            crime_id = get_crime_id(entity)
            if crime_id is not None:
                crimes.add(crime_id)

    return crimes

# Function to find crimes mentioned in all hadith
def find_crimes_mentioned_in_all_hadith(hadith_df, save_result=False, collection="maj"):
    """
    Identifies crimes mentioned in all hadith within the dataset.

    Args:
        hadith_df (pd.DataFrame): DataFrame containing hadith texts in Arabic.
        save_result (bool, optional): Whether to save the results to an Excel file. Defaults to False.
        collection (str, optional): The collection name to use for saving results. Defaults to "maj".

    Returns:
        pd.DataFrame: DataFrame with hadith numbers and corresponding crime mentions.
    """
    all_crimes = []
    all_mentioned_crimes = []
    all_hadith_numbers = []

    # Iterate through the hadith dataset with a progress bar
    with tqdm.tqdm(total=len(hadith_df), desc="Extracting crimes") as pbar:
        for _, row in hadith_df.iterrows():
            # Extract Arabic text
            arabic_text = row[tarabic_name]

            # Find crimes mentioned in the current hadith
            crimes_in_hadith = find_crime_in_one_hadith(arabic_text)

            # Append results
            all_crimes.append(crimes_in_hadith)
            all_mentioned_crimes.extend(crimes_in_hadith)
            all_hadith_numbers.append(row[hadith_number_name])

            pbar.update(1)

    # Log summary statistics
    print(f"Total hadith processed: {len(all_crimes)}")
    print(f"Total unique crimes mentioned: {len(set(all_mentioned_crimes))}")
    print(f"Unique crime IDs: {set(all_mentioned_crimes)}")

    # Create a DataFrame to store results
    result_df = pd.DataFrame({
        "hadith_number": all_hadith_numbers,
        "crimes": all_crimes,
    })

    # Save results to an Excel file if requested
    if save_result:
        save_path = f"results/{collection}/crimes.xlsx"
        result_df.to_excel(save_path, index=False)
        print(f"Results saved to {save_path}")

    return result_df

