from NERModelLoader import nlp
from utility import strip_punctuation, Resolve_Entities, tarabic_name, hadith_number_name
from pyarabic.araby import strip_tashkeel
import tqdm
import pandas as pd

crime_id_df = pd.read_csv("dictionaries/crimes.csv")

def get_crime_id(arabic_name):

    for index, row in crime_id_df.iterrows():
        string_list = row['alternatives'].split('-')
        if any(substring in arabic_name for substring in string_list):
            return row['id']


def find_crime_in_one_hadith(arabic_text):

    crimes = []
    arabic_text = strip_punctuation(arabic_text)

    arabic_text = strip_tashkeel(arabic_text)

    # Process the text with the NER model
    doc = nlp(arabic_text)

    # Extract entities from the processed document
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    resolved_entities = Resolve_Entities(entities)

    # Iterate over resolved entities and update DataFrame columns
    for entity, label in resolved_entities:
        if label == "CRIME":
            cr = get_crime_id(entity)
            if cr is not None:
                crimes.append(cr)

    #print(locations)
    crimes = set(crimes)
    return crimes


def find_crimes_mentioned_in_all_hadith(hadith_df, save_result=False, collection="maj"):
    all_crimes= []
    ac = []
    all_hnum = []
    with tqdm.tqdm(total=len(hadith_df), desc=f'Getting crimes') as pbar:

        for index, row in hadith_df.iterrows():
            # print(index)

            arabic_text = row[tarabic_name]

            crimes = find_crime_in_one_hadith(arabic_text)

            all_crimes.append(crimes)
            ac.extend(crimes)
            all_hnum.append(row[hadith_number_name])



            pbar.update(1)
    print(len(all_crimes),len(all_crimes))
    print(set(ac))
    result_df = pd.DataFrame({'hadith_number': all_hnum, 'crimes': all_crimes})
    if save_result:
        result_df.to_excel("results/" + collection + "/crimes.xlsx", index=False)

    return result_df
    #all_locations = set(all_locations)
    #print(all_locations)

