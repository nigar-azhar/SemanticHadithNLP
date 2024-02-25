from NERModelLoader import nlp
from utility import strip_punctuation, Resolve_Entities, tarabic_name, hadith_number_name
from pyarabic.araby import strip_tashkeel
import tqdm
import pandas as pd

# def get_location_id(arabic_name):
#     df = pd.read_csv("dictionaries/locations")
#     #ent = 'عرفة'
#     for index, row in df.iterrows():
#         string_list = row['alternatives'].split('-')
#         if any(substring in arabic_name for substring in string_list):
#             return row['id']


def find_heaven_and_hell_in_one_hadith(arabic_text):

    p_mentions = []
    h_mentions = []
    arabic_text = strip_punctuation(arabic_text)

    arabic_text = strip_tashkeel(arabic_text)

    # Process the text with the NER model
    doc = nlp(arabic_text)

    # Extract entities from the processed document
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    resolved_entities = Resolve_Entities(entities)

    # Iterate over resolved entities and update DataFrame columns
    for entity, label in resolved_entities:
        if label == "PARA":
            p_mentions.append("Heaven")
        elif label == "HELL":
            h_mentions.append("Hell")

    #print(locations)
    p_mentions = set(p_mentions)
    h_mentions = set(h_mentions)
    return p_mentions, h_mentions


def find_heaven_and_hell_mentioned_in_all_hadith(hadith_df, save_result=False, collection="sb"):
    all_p = []
    all_h = []
    all_hnum = []
    with tqdm.tqdm(total=len(hadith_df), desc=f'Getting heaven and hell') as pbar:

        for index, row in hadith_df.iterrows():
            # print(index)

            arabic_text = row[tarabic_name]

            p_mentions, h_mentions = find_heaven_and_hell_in_one_hadith(arabic_text)

            all_p.append(p_mentions)
            all_h.append(h_mentions)
            all_hnum.append(row[hadith_number_name])



            pbar.update(1)
    #print(len(all_hnum),len(all_locations))
    #print(all_locations)
    result_df = pd.DataFrame({'hadith_number': all_hnum, 'HEAVEN': all_p, 'HELL':all_h})
    if save_result:
        result_df.to_excel("results/" + collection + "/afterlife.xlsx", index=False)

    return result_df
    #all_locations = set(all_locations)
    #print(all_locations)

