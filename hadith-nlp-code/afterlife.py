import pandas as pd
import tqdm
from pyarabic.araby import strip_tashkeel
from NERModelLoader import nlp
from utility import strip_punctuation, Resolve_Entities, tarabic_name, hadith_number_name

# Function to find mentions of heaven and hell in a single hadith
def find_heaven_and_hell_in_one_hadith(arabic_text):
    """
    Identifies mentions of Heaven and Hell in a single hadith.

    Args:
        arabic_text (str): The Arabic text of the hadith.

    Returns:
        tuple: Sets containing mentions of "Heaven" and "Hell".
    """
    # Preprocess the Arabic text
    arabic_text = strip_punctuation(arabic_text)
    arabic_text = strip_tashkeel(arabic_text)

    # Extract entities using the NER model
    doc = nlp(arabic_text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    resolved_entities = Resolve_Entities(entities)

    # Initialize mention sets
    p_mentions = set()  # Heaven mentions
    h_mentions = set()  # Hell mentions

    # Process resolved entities
    for entity, label in resolved_entities:
        if label == "PARA":
            p_mentions.add("Heaven")
        elif label == "HELL":
            h_mentions.add("Hell")

    return p_mentions, h_mentions


# Function to find mentions of Heaven and Hell in all hadith
def find_heaven_and_hell_mentioned_in_all_hadith(hadith_df, save_result=False, collection="sb"):
    """
    Identifies mentions of Heaven and Hell in all hadith within a dataset.

    Args:
        hadith_df (pd.DataFrame): DataFrame containing hadith texts.
        save_result (bool, optional): Whether to save the results to an Excel file. Defaults to False.
        collection (str, optional): The collection name to use for saving results. Defaults to "sb".

    Returns:
        pd.DataFrame: DataFrame with hadith numbers and corresponding Heaven and Hell mentions.
    """
    all_heaven_mentions = []
    all_hell_mentions = []
    all_hadith_numbers = []

    # Iterate through the hadith dataset with a progress bar
    with tqdm.tqdm(total=len(hadith_df), desc="Extracting Heaven and Hell mentions") as pbar:
        for _, row in hadith_df.iterrows():
            arabic_text = row[tarabic_name]  # Extract Arabic text column
            hadith_number = row[hadith_number_name]  # Extract hadith number

            # Find Heaven and Hell mentions for the current hadith
            p_mentions, h_mentions = find_heaven_and_hell_in_one_hadith(arabic_text)

            # Append results
            all_heaven_mentions.append(p_mentions)
            all_hell_mentions.append(h_mentions)
            all_hadith_numbers.append(hadith_number)

            pbar.update(1)

    # Create a DataFrame to store results
    result_df = pd.DataFrame({
        "hadith_number": all_hadith_numbers,
        "HEAVEN": all_heaven_mentions,
        "HELL": all_hell_mentions,
    })

    # Save results to an Excel file if requested
    if save_result:
        save_path = f"results/{collection}/afterlife.xlsx"
        result_df.to_excel(save_path, index=False)
        print(f"Results saved to {save_path}")

    return result_df
