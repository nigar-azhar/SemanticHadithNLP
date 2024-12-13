import pandas as pd
from tqdm import tqdm

# Utility functions
def append_ttl_string(hid, items, ttl_strings, objprop="containsMentionOf"):
    """
    Appends TTL strings for a list of items to the TTL collection.

    Args:
        hid (str): Hadith ID.
        items (list): List of items to include in the TTL string.
        ttl_strings (list): Existing TTL strings to append to.
        objprop (str): Object property for the TTL relation.

    Returns:
        list: Updated TTL strings.
    """
    if items:
        items = [item for item in items if item is not None]  # Remove None values
        if items:
            comma_separated_string = ', :'.join(items)
            ttl = f":{hid} :{objprop} :{comma_separated_string} ."
            ttl_strings.append(ttl)
    return ttl_strings


def append_afterlife_ttl(hid, heavenlist, helllist, ttl_strings):
    """
    Appends TTL strings for Heaven and Hell mentions.

    Args:
        hid (str): Hadith ID.
        heavenlist (list): List of Heaven mentions.
        helllist (list): List of Hell mentions.
        ttl_strings (list): Existing TTL strings to append to.

    Returns:
        list: Updated TTL strings.
    """
    if heavenlist:
        ttl_strings.append(f":{hid} :discussesTopic :Heaven .")
    if helllist:
        ttl_strings.append(f":{hid} :discussesTopic :Hell .")
    return ttl_strings


def append_ayat_ttl(hid, ayat_list, ttl_strings):
    """
    Appends TTL strings for Quranic ayat mentions.

    Args:
        hid (str): Hadith ID.
        ayat_list (list): List of Quranic ayat tuples (chapter, verse).
        ttl_strings (list): Existing TTL strings to append to.

    Returns:
        list: Updated TTL strings.
    """
    if ayat_list:
        formatted_ayat = [f":CH{chapter:03d}_V{verse:03d}" for chapter, verse in ayat_list]
        comma_separated_string = ', '.join(formatted_ayat)
        ttl_strings.append(f":{hid} :containsMentionOfVerse {comma_separated_string} .")
    return ttl_strings


def arabic_to_int(arabic_numeral):
    """
    Converts Eastern Arabic numerals to integers.

    Args:
        arabic_numeral (str): The Arabic numeral string.

    Returns:
        int: The integer equivalent.
    """
    numeral_dict = {'۰': 0, '۱': 1, '۲': 2, '۳': 3, '۴': 4, '۵': 5, '۶': 6, '۷': 7, '۸': 8, '۹': 9}
    if any(ch in arabic_numeral for ch in ['م', 'b', 'm']):
        return -1
    arabic_numeral = arabic_numeral[1:-1]
    return int(''.join(str(numeral_dict[ch]) for ch in arabic_numeral))


def append_similarity_ttl(hid, row, ttl_strings, label):
    """
    Appends TTL strings for similar hadith mentions.

    Args:
        hid (str): Hadith ID.
        row (pd.Series): Row containing similarity data.
        ttl_strings (list): Existing TTL strings to append to.
        label (str): Label prefix for Hadith IDs.

    Returns:
        list: Updated TTL strings.
    """
    strong = eval(row['ar_0.9'])
    similar = eval(row['ar_0.8']) + eval(row['ar_0.7']) + eval(row['ar_rest'])

    if strong:
        strong_ids = [f":{label}-HD{hnum:04d}" for hnum in strong if f":{label}-HD{hnum:04d}" != hid]
        if strong_ids:
            ttl_strings.append(f":{hid} :isStronglySimilar {', '.join(strong_ids)} .")

    if similar:
        similar_ids = [f":{label}-HD{hnum:04d}" for hnum in similar]
        ttl_strings.append(f":{hid} :isSimilar {', '.join(similar_ids)} .")

    return ttl_strings

# Main turtling functions
def turtlfy_collection(collection="sb", save_path="results/ttl"):
    """
    Converts a Hadith collection into TTL format.

    Args:
        collection (str): The collection name (e.g., "sb", "maj").
        save_path (str): Path to save the TTL file.

    Returns:
        None
    """
    label_mapping = {"sb": "SB", "maj": "IM", "ms": "SM", "nis": "SN", "tir": "JT", "sad": "SD"}
    label = label_mapping.get(collection, "SB")
    df = pd.read_excel(f"results/{collection}/identified_entities/locations.xlsx")

    ttl_strings = []
    prefixes = """@base <http://semantichadith.com/ontology> .
@prefix : <http://www.semantichadith.com/ontology/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix qur: <http://quranontology.com/Resource/> .
@prefix wiki: <https://www.wikidata.org/wiki/> ."""
    ttl_strings.append(prefixes)

    additional_files = {
        "angels": "angels.xlsx",
        "prophets": "prophets.xlsx",
        "clans": "clans.xlsx",
        "crimes": "crimes.xlsx",
        "holybooks": "holybooks.xlsx",
        "afterlife": "afterlife.xlsx",
        "pillarsofislam": "pillarsofislam.xlsx",
        "caliphs": "caliphs.xlsx",
        "plants": "plants.xlsx",
        "animals": "animals.xlsx",
        "concepts": "concepts.xlsx",
        "ayat": "ayat.xlsx",
        "similarity": "mukarrat_similarity.csv"
    }

    # Load additional data
    additional_data = {key: pd.read_excel(f"results/{collection}/identified_entities/{file}")
                       for key, file in additional_files.items() if file.endswith('.xlsx')}
    additional_data["similarity"] = pd.read_csv(f"results/{collection}/mukarrat_similarity.csv")

    with tqdm(total=len(df), desc=f"Generating TTL for {label}") as pbar:
        for index, row in df.iterrows():
            hnum = row['hadith_number']
            if label == "JT":
                hnum = arabic_to_int(hnum)
                if hnum == -1:
                    continue
            hid = f"{label}-HD{hnum:04d}"

            location = eval(row['locations'])
            ttl_strings = append_ttl_string(hid, location, ttl_strings)

            for key, data in additional_data.items():
                if key in ["similarity"]:
                    ttl_strings = append_similarity_ttl(hid, data.iloc[index], ttl_strings, label)
                else:
                    entities = eval(data.iloc[index, 1])
                    ttl_strings = append_ttl_string(hid, entities, ttl_strings, objprop="discussesTopic" if key in ["crimes", "concepts"] else "containsMentionOf")

            ttl_strings = append_afterlife_ttl(hid, eval(additional_data["afterlife"].iloc[index, 1]), eval(additional_data["afterlife"].iloc[index, 2]), ttl_strings)
            ttl_strings = append_ayat_ttl(hid, eval(additional_data["ayat"].iloc[index, 1]), ttl_strings)

            pbar.update(1)

    with open(f"{save_path}/{label}.ttl", 'w') as file:
        file.write('\n\n'.join(ttl_strings))


#turtlfy_mapping_hadith_book_topic_qur()