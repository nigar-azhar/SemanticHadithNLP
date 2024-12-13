import pandas as pd
from tqdm import tqdm
from pyarabic.araby import strip_tashkeel
from NERModelLoader import nlp
from utility import strip_punctuation, Resolve_Entities, tarabic_name, hadith_number_name


def find_persons_in_one_hadith(arabic_text):
    """
    Identifies mentions of persons (entities labeled as "PERS") in a single hadith using NER.

    Args:
        arabic_text (str): The Arabic text of the hadith.

    Returns:
        set: A set of unique person mentions in the hadith.
    """
    # Preprocess Arabic text
    arabic_text = strip_tashkeel(arabic_text)

    # Process the text with the NER model
    doc = nlp(arabic_text)

    # Extract entities and resolve them
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    resolved_entities = Resolve_Entities(entities)

    # Collect person entities
    persons = {entity for entity, label in resolved_entities if label == "PERS"}

    return persons


def find_persons_mentioned_in_all_hadith(hadith_df, save_result=False, save_file_path=""):
    """
    Identifies mentions of persons across all hadith in the dataset.

    Args:
        hadith_df (pd.DataFrame): DataFrame containing hadith texts in Arabic.
        save_result (bool, optional): Whether to save the results to an Excel file. Defaults to False.
        save_file_path (str, optional): File path to save the results. Defaults to "".

    Returns:
        pd.DataFrame: DataFrame with hadith numbers and corresponding person mentions.
    """
    all_persons = []
    all_person_mentions = []
    all_hadith_numbers = []

    # Iterate through the hadith dataset with a progress bar
    with tqdm(total=len(hadith_df), desc="Extracting mentions of persons") as pbar:
        for _, row in hadith_df.iterrows():
            # Extract Arabic text
            arabic_text = row.get(tarabic_name, "")

            # Find persons mentioned in the current hadith
            persons_in_hadith = find_persons_in_one_hadith(arabic_text)

            # Append results
            all_persons.append(persons_in_hadith)
            all_person_mentions.extend(persons_in_hadith)
            all_hadith_numbers.append(row.get(hadith_number_name, ""))

            pbar.update(1)

    # Log summary statistics
    print(f"Total hadith processed: {len(all_persons)}")
    print(f"Total unique persons mentioned: {len(set(all_person_mentions))}")
    print(f"Unique person names: {set(all_person_mentions)}")

    # Create a DataFrame to store results
    result_df = pd.DataFrame({
        "hadith_number": all_hadith_numbers,
        "persons": all_persons,
    })

    # Save results to an Excel file if requested
    if save_result and save_file_path:
        result_df.to_excel(save_file_path, index=False)
        print(f"Results saved to {save_file_path}")

    return result_df
