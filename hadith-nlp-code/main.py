import pandas as pd

from angels import find_angels_mentioned_in_all_hadith
from animals import find_animals_mentioned_in_all_hadith
from ayat import find_ayat_mentioned_in_all_hadith
from caliphs import find_caliphs_mentioned_in_all_hadith
from concepts import find_concepts_mentioned_in_all_hadith
from crimes import find_crimes_mentioned_in_all_hadith
from generate_rdf import turtlfy_collection
from groupofpeople import find_clans_mentioned_in_all_hadith
from holybooks import find_holybooks_mentioned_in_all_hadith
from locations import find_locations_mentioned_in_all_hadith
from persons import find_persons_mentioned_in_all_hadith
from pillarsofislam import find_pillars_mentioned_in_all_hadith
from plants import find_plants_mentioned_in_all_hadith
from prophets import find_prophets_mentioned_in_all_hadith
from similarities import encode_all_hadith, calculate_cosine_similarity, calculate_euclidean_similarity, \
    calculate_manhattan_similarity, find_similar_hadith, find_similarity_values_mukarrat_hadith, \
    find_similarity_values_all_hadith
from afterlife import find_heaven_and_hell_mentioned_in_all_hadith


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print_hi('Graph')
    cols = ["sb","maj","ms","nis","tir","sad"]
    for col in cols:
        print(col)
        #simplified_hadith_df = pd.read_excel("data/simplified_"+col+"_db.xlsx")
        #find_locations_mentioned_in_all_hadith(simplified_hadith_df, True, collection=col)
        #find_holybooks_mentioned_in_all_hadith(simplified_hadith_df, True,collection=col)
        #find_prophets_mentioned_in_all_hadith(simplified_hadith_df, True,collection=col)
        #find_crimes_mentioned_in_all_hadith(simplified_hadith_df, True,collection=col)
        #find_pillars_mentioned_in_all_hadith(simplified_hadith_df, True,collection=col)
        #find_angels_mentioned_in_all_hadith(simplified_hadith_df, True,collection=col)
        #find_clans_mentioned_in_all_hadith(simplified_hadith_df, True, "results/"+col+"/clans.xlsx")
        #find_caliphs_mentioned_in_all_hadith(simplified_hadith_df, True, "results/"+col+"/caliphs.xlsx")

        #find_heaven_and_hell_mentioned_in_all_hadith(simplified_hadith_df, True, collection=col)

        #turtlfy_collection(collection=col)


    #find_clans_mentioned_in_all_hadith(simplified_hadith_df, True, "results/clans.xlsx")
    # find_angels_mentioned_in_all_hadith(simplified_hadith_df, True, collection="maj")
    #find_ayat_mentioned_in_all_hadith(simplified_hadith_df, True,collection="maj")
    # find_animals_mentioned_in_all_hadith(simplified_hadith_df, True, "results/sb/animals.xlsx")
    # find_plants_mentioned_in_all_hadith(simplified_hadith_df, True, "results/sb/plants.xlsx")
    #find_caliphs_mentioned_in_all_hadith(simplified_hadith_df, True, "results/caliphs.xlsx")
    #encode_all_hadith(simplified_hadith_df, True, "results/buhkari_encodings.xlsx")
    #calculate_cosine_similarity()
    #calculate_euclidean_similarity()
    #calculate_manhattan_similarity()
    #find_similar_hadith()
    #find_similar_hadith("euclidean")
    #find_similar_hadith("manhattan")
    #find_concepts_mentioned_in_all_hadith(simplified_hadith_df, True, "results/concepts.xlsx")

    #find_persons_mentioned_in_all_hadith(simplified_hadith_df, True, "results/persons-2.xlsx")
    #find_similarity_values_mukarrat_hadith(simplified_hadith_df)
    #find_similarity_values_all_hadith()

