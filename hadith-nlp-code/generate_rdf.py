import pandas as pd
from tqdm import tqdm

def get_ttl_string(hid, list1, ttl_strings, objprop="containsMentionOf"):
    if len(list1) > 0:
        #print(hid, list1)
        if None in list1:
            list1.remove(None)

        if len(list1) > 0:
            comma_separated_string = ', :'.join(list1)
            # Create a TTL string for the row
            ttl = f":{hid} :{objprop} :{comma_separated_string} ."
            # Append the TTL string to the list
            ttl_strings.append(ttl)

    return ttl_strings


def get_ttl_al_string(hid, heavenlist, helllist, ttl_strings):
    if len(heavenlist) > 0:
        #print(hid, list1)
        #comma_separated_string = ', '.join(list1)
        # Create a TTL string for the row
        ttl = f":{hid} :discussesTopic :Heaven ."
        # Append the TTL string to the list
        ttl_strings.append(ttl)

    if len(helllist) > 0:
        #print(hid, list1)
        #comma_separated_string = ', '.join(list1)
        # Create a TTL string for the row
        ttl = f":{hid} :discussesTopic :Hell ."
        # Append the TTL string to the list
        ttl_strings.append(ttl)

    return ttl_strings


def get_ayat_ttl_string(hid, ayat_list, ttl_strings):
    if len(ayat_list) > 0:
        # Convert each tuple to the desired string format
        string_list = [':CH{:03d}_V{:03d}'.format(chapter, verse) for chapter, verse in ayat_list]

        #print(hid, list1)
        comma_separated_string = ', '.join(string_list)
        # Create a TTL string for the row
        ttl = f":{hid} :containsMentionOfVerse {comma_separated_string} ."
        # Append the TTL string to the list
        ttl_strings.append(ttl)

    return ttl_strings

# Custom function to convert Eastern Arabic numerals to integers
def arabic_to_int(arabic_numeral):
    numeral_dict = {'۰': 0, '۱': 1, '۲': 2, '۳': 3, '۴': 4, '۵': 5, '۶': 6, '۷': 7, '۸': 8, '۹': 9}
    #print(arabic_numeral)
    if 'م' in arabic_numeral or 'b'  in arabic_numeral or 'm' in arabic_numeral:
        return -1
    # elif arabic_numeral == '~32oo~':
    #     return 3200

    result = 0
    arabic_numeral = arabic_numeral[1:-1]
    for numeral in arabic_numeral:
        result = result * 10 + numeral_dict[numeral]

    return result

def get_similar_hd_ttl_string(hid, row, ttl_strings, label):

    strong = eval(row['ar_0.9'])
    similar = eval(row['ar_0.8'])
    similar.extend(eval(row['ar_0.7']))
    similar.extend(eval(row['ar_rest']))

    if len(strong) > 0:

        # Convert each tuple to the desired string format
        string_list = [f":{label}-HD{hnum:04d}".format(label, hnum) for hnum in strong]

        #print(string_list, hid)
        if hid in string_list:
            string_list.remove(hid)
        #string_list.remove(hid)

        if len(string_list) > 0:
            #print(hid, list1)
            comma_separated_string = ', '.join(string_list)
            # Create a TTL string for the row
            ttl = f":{hid} :isStronglySimilar {comma_separated_string} ."
            # Append the TTL string to the list
            ttl_strings.append(ttl)

    if len(similar) > 0:
        # Convert each tuple to the desired string format
        string_list = [f":{label}-HD{hnum:04d}".format(label, hnum) for hnum in similar]

        #print(hid, list1)
        comma_separated_string = ', '.join(string_list)
        # Create a TTL string for the row
        ttl = f":{hid} :isSimilar {comma_separated_string} ."
        # Append the TTL string to the list
        ttl_strings.append(ttl)

    return ttl_strings

def turtlfy_collection(collection="sb",save_path="results/ttl"):
    label = "SB"
    if collection == "sb":
        label = "SB"
    elif collection == "maj":
        label = "IM"
    elif collection == "ms":
        label = "SM"
    elif collection == "nis":
        label = "SN"
    elif collection == "tir":
        label = "JT"
    elif collection == "sad":
        label = "SD"

    # Read the DataFrame from the file
    df = pd.read_excel("results/"+collection+"/identified_entities/locations.xlsx")  # Change the file path as needed

    ttl_strings = []

    # Add prefixes
    prefixes = """@base <http://semantichadith.com/ontology> .
        @prefix : <http://www.semantichadith.com/ontology/> .
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix qur: <http://quranontology.com/Resource/> .
        @prefix wiki: <https://www.wikidata.org/wiki/> ."""

    ttl_strings.append(prefixes)

    df_angels = pd.read_excel("results/"+collection+"/identified_entities/angels.xlsx")
    df_prophets = pd.read_excel("results/"+collection+"/identified_entities/prophets.xlsx")
    df_clans = pd.read_excel("results/"+collection+"/identified_entities/clans.xlsx")
    df_crimes = pd.read_excel("results/"+collection+"/identified_entities/crimes.xlsx")
    df_holybooks = pd.read_excel("results/"+collection+"/identified_entities/holybooks.xlsx")
    df_afterlife = pd.read_excel("results/"+collection+"/identified_entities/afterlife.xlsx")
    df_poi = pd.read_excel("results/"+collection+"/identified_entities/pillarsofislam.xlsx")

    if label == "SB":
        df_caliphs = pd.read_excel("results/" + collection + "/identified_entities/caliphs.xlsx")

        df_ayat = pd.read_excel("results/"+collection+"/identified_entities/ayat.xlsx")

        df_concepts = pd.read_excel("results/"+collection+"/identified_entities/concepts.xlsx")

        df_plants = pd.read_excel("results/"+collection+"/identified_entities/plants.xlsx")
        df_animals = pd.read_excel("results/"+collection+"/identified_entities/animals.xlsx")
        df_sim = pd.read_csv("results/"+collection+"/mukarrat_similarity.csv")

    #index = 0
    with tqdm(total=len(df), desc=f'Generating turtle') as pbar:

        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():

            # Extract the prophet name and additional parameters
            hnum = row['hadith_number']
            if label == "JT":
                hnum = arabic_to_int(hnum)
                if hnum == -1:
                    continue
            hid = label + "-HD" + f"{hnum:04d}"

            location = eval(row['locations'])
            ttl_strings = get_ttl_string(hid, location, ttl_strings)
            # if len(location) > 0:
            #     #print(hid,location)
            #     comma_separated_string = ', '.join(location)
            #     # Create a TTL string for the row
            #     ttl = f":{hid} :containsMentionOf :{comma_separated_string} ."
            #     # Append the TTL string to the list
            #     ttl_strings.append(ttl)

            angels = eval(df_angels.iloc[index, 1])
            ttl_strings = get_ttl_string(hid, angels, ttl_strings)


            prophets = eval(df_prophets.iloc[index, 1])
            ttl_strings = get_ttl_string(hid, prophets, ttl_strings)


            crimes = eval(df_crimes.iloc[index, 1])
            ttl_strings = get_ttl_string(hid, crimes, ttl_strings, objprop="discussesTopic")

            clans = eval(df_clans.iloc[index, 1])
            ttl_strings = get_ttl_string(hid, clans, ttl_strings)

            hbooks = eval(df_holybooks.iloc[index, 1])
            ttl_strings = get_ttl_string(hid, hbooks, ttl_strings)

            pois = eval(df_poi.iloc[index, 1])
            ttl_strings = get_ttl_string(hid, pois, ttl_strings, objprop="discussesTopic")

            hvn = eval(df_afterlife.iloc[index, 1])
            hl = eval(df_afterlife.iloc[index, 2])
            ttl_strings = get_ttl_al_string(hid, hvn, hl, ttl_strings)

            if label == "SB":
                caliphs = eval(df_caliphs.iloc[index, 1])
                ttl_strings = get_ttl_string(hid, caliphs, ttl_strings)

                plants = eval(df_plants.iloc[index, 1])
                ttl_strings = get_ttl_string(hid, plants, ttl_strings)

                animals = eval(df_animals.iloc[index, 1])
                ttl_strings = get_ttl_string(hid, animals, ttl_strings)

                concepts = eval(df_concepts.iloc[index, 1])
                ttl_strings = get_ttl_string(hid, concepts, ttl_strings, objprop="discussesTopic")


                ayts = eval(df_ayat.iloc[index, 1])
                ttl_strings = get_ayat_ttl_string(hid, ayts, ttl_strings)


                hds = df_sim.iloc[index]
                ttl_strings = get_similar_hd_ttl_string(hid, hds, ttl_strings,label)


            # if len(angels) > 0:
            #     print(hid,angels)
            #     comma_separated_string = ', '.join(angels)
            #     # Create a TTL string for the row
            #     ttl = f":{hid} :containsMentionOf :{comma_separated_string} ."
            #     # Append the TTL string to the list
            #     ttl_strings.append(ttl)



            index += 1

            pbar.update(1)

        # Write all TTL strings to a single file
    with open(save_path + "/" + label + '.ttl', 'w') as file:
        file.write('\n\n'.join(ttl_strings))

    #print('\n\n'.join(ttl_strings))


def tutlfy_csv(class_name='Animal',path="dictionaries/animals.csv",save_path="results"):
    #import pandas as pd

    # Read the CSV file
    df = pd.read_csv(path)

    ttl_strings = []

    # Add prefixes
    prefixes = """@base <http://semantichadith.com/ontology> .
    @prefix : <http://www.semantichadith.com/ontology/> .
    @prefix owl: <http://www.w3.org/2002/07/owl#> .
    @prefix qur: <http://quranontology.com/Resource/> .
    @prefix wiki: <https://www.wikidata.org/wiki/> ."""

    ttl_strings.append(prefixes)

    # Iterate over each row
    for index, row in df.iterrows():
        # Get the ID value
        animal_id = row['ID']

        # Create a TTL string for the row
        ttl = f":{animal_id} a :{class_name} ."

        # Append the TTL string to the list
        ttl_strings.append(ttl)

    # Write all TTL strings to a single file
    with open(save_path+"/"+class_name+'s.ttl', 'w') as file:
        file.write('\n\n'.join(ttl_strings))

    print('\n\n'.join(ttl_strings))
        # # Write the TTL to a file
        # with open(f'{animal_id}.ttl', 'w') as file:
        #     file.write(ttl)



def turtlfy_mappping_qur_to_id(save_path="results/ttl"):
    # Read the DataFrame from the file
    df = pd.read_excel("mappings/qur-to-hadith.xlsx", sheet_name=1)
    ttl_strings = []

    # Add prefixes
    prefixes = """@base <http://semantichadith.com/ontology> .
            @prefix : <http://www.semantichadith.com/ontology/> .
            @prefix owl: <http://www.w3.org/2002/07/owl#> .
            @prefix qur: <http://quranontology.com/Resource/> .
            @prefix wiki: <https://www.wikidata.org/wiki/> ."""

    ttl_strings.append(prefixes)

    for index, row in df.iterrows():
        # Get the ID value
        id = row['ID']
        topic = df.iloc[index, 0].split("/")[-1]

        # Create a TTL string for the row
        ttl = f":{id} rdfs:seeAlso qur:{topic} ."

        # Append the TTL string to the list
        ttl_strings.append(ttl)

    # Write all TTL strings to a single file
    with open(save_path + "/seeAlso-qur.ttl", 'w') as file:
        file.write('\n\n'.join(ttl_strings))

    print('\n\n'.join(ttl_strings))

def turtlfy_mappping_book_to_id(save_path="results/ttl"):
    # Read the DataFrame from the file
    df = pd.read_excel("mappings/qur-to-hadith.xlsx", sheet_name=0)
    ttl_strings = []

    # Add prefixes
    prefixes = """@base <http://semantichadith.com/ontology> .
            @prefix : <http://www.semantichadith.com/ontology/> .
            @prefix owl: <http://www.w3.org/2002/07/owl#> .
            @prefix qur: <http://quranontology.com/Resource/> .
            @prefix wiki: <https://www.wikidata.org/wiki/> ."""

    ttl_strings.append(prefixes)
    print(df.keys())
    for index, row in df.iterrows():
        # Get the ID value
        id = row['mentionsID']
        #topic = df.iloc[index, 0].split("/")[-1]
        # print(row['Hadith'])
        rang = row['Hadith'].split('-')


        istopic = row['isTopic']

        hds = []

        start =int(rang[0])
        end =int(rang[1])
        for hnum in range(start, end+1):
            hid = ":SB-HD" + f"{hnum:04d}"
            hds.append(hid)

        comma_separated_string = ', '.join(hds)
        # Create a TTL string for the row

        if pd.isna(istopic):# is None:
            ttl = f":{id} :mentionedIn {comma_separated_string} ."
        else:
            ttl = f":{id} :discussedIn {comma_separated_string} ."

        # Append the TTL string to the list
        ttl_strings.append(ttl)

    # Write all TTL strings to a single file
    with open(save_path + "/mentionedIn.ttl", 'w') as file:
        file.write('\n\n'.join(ttl_strings))

    print('\n\n'.join(ttl_strings))


def turtlfy_mapping_hadith_book_topic_qur(save_path="results/ttl"):
    # Read the DataFrame from the file
    df = pd.read_excel("mappings/qur-topics-bukhari-books.xlsx")
    ttl_strings = []

    # Add prefixes
    prefixes = """@base <http://semantichadith.com/ontology> .
                @prefix : <http://www.semantichadith.com/ontology/> .
                @prefix owl: <http://www.w3.org/2002/07/owl#> .
                @prefix qur: <http://quranontology.com/Resource/> .
                @prefix wiki: <https://www.wikidata.org/wiki/> ."""

    ttl_strings.append(prefixes)
    print(df.keys())
    for index, row in df.iterrows():


        # Get the ID value
        id = row['instance-IDs']
        istopic = row['istopic']
        topic = df.iloc[index, 0].split("/")[-1]

        # Create a TTL string for the row
        ttl = f":{id} rdfs:seeAlso qur:{topic} ."

        ttl_strings.append(ttl)

        rngs = row['hadith-numbers'].split(',')
        hds = []
        for rng in rngs:


            rang = rng.split("-")

            start = int(rang[0])
            end = int(rang[1])
            for hnum in range(start, end + 1):
                hid = ":SB-HD" + f"{hnum:04d}"
                hds.append(hid)


        comma_separated_string = ', '.join(hds)

        if pd.isna(istopic):# is None:
            ttl = f":{id} :discussedIn {comma_separated_string} ."
        else:
            ttl = f":{id} :mentionedIn {comma_separated_string} ."

        # Append the TTL string to the list
        ttl_strings.append(ttl)

    # Write all TTL strings to a single file
    with open(save_path + "/booktotopic.ttl", 'w') as file:
        file.write('\n\n'.join(ttl_strings))

    print('\n\n'.join(ttl_strings))


#tutlfy_csv(class_name='Plant',path="dictionaries/plants.csv")
#turtlfy_collection()

#turtlfy_mappping_qur_to_id()
#turtlfy_mappping_book_to_id()
turtlfy_mapping_hadith_book_topic_qur()