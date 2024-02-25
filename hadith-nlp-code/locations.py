from NERModelLoader import nlp
from utility import strip_punctuation, Resolve_Entities, tarabic_name, hadith_number_name, clean_arabic_text
from pyarabic.araby import strip_tashkeel
import tqdm
import pandas as pd

def get_location_id(arabic_name):
    df = pd.read_csv("dictionaries/locations.csv")
    #ent = 'عرفة'
    for index, row in df.iterrows():
        string_list = row['alternatives'].split('-')
        if any(substring in arabic_name for substring in string_list):
            return row['id']


def find_location_in_one_hadith(arabic_text):

    locations = []
    arabic_text = strip_punctuation(arabic_text)

    arabic_text = strip_tashkeel(arabic_text)
    arabic_text = clean_arabic_text(arabic_text)
    #print(arabic_text)

    # Process the text with the NER model
    doc = nlp(arabic_text)

    # Extract entities from the processed document
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    resolved_entities = Resolve_Entities(entities)

    # Iterate over resolved entities and update DataFrame columns
    for entity, label in resolved_entities:
        #print(entity, label)
        if label == "LOC":

            locations.append(get_location_id(entity))

    #print(locations)
    locations = set(locations)
    return locations


def find_locations_mentioned_in_all_hadith(hadith_df, save_result=False, collection="sb"):
    all_locations = []
    all_hnum = []
    with tqdm.tqdm(total=len(hadith_df), desc=f'Getting locations') as pbar:

        for index, row in hadith_df.iterrows():
            # print(index)

            arabic_text = row[tarabic_name]

            locations = find_location_in_one_hadith(arabic_text)


            all_locations.append(locations)
            all_hnum.append(row[hadith_number_name])



            pbar.update(1)
    print(len(all_hnum),len(all_locations))
    print(all_locations)
    result_df = pd.DataFrame({'hadith_number': all_hnum, 'locations': all_locations})
    if save_result:
        result_df.to_excel("results/"+collection+"/locations.xlsx",index=False)

    return result_df
    #all_locations = set(all_locations)
    #print(all_locations)

