import re
import pandas as pd

import tqdm

from utility import english_name, hadith_number_name


# def extract_coordinates_values(text):
#
#     #matches = re.findall(r'\((\d+\.\d+)\)', text)
#     matches = re.findall(r'(\d+\.\d+(?:-\d+)?)', text)
#     return matches if matches else []

def extract_coordinates_values(text):
    matches = re.findall(r'(\d+\.\d+(?:-\d+)?)', text)#re.findall(r'(\d+\.\d+(?:-\d+\.\d+)?)', text)
    if not matches:
        return []
    coordinates = []
    #print(matches)
    for match in matches:
        parts = match.split('-')

        if len(parts) == 1:
            integers = match.split('.')
            #print(integers)
            coordinates.append((int(integers[0]), int(integers[1])))
        else:
            #print(parts)
            integers = match.split('.')
            surah = int(integers[0])
            ayat_range = integers[1]
            #75.16-17)
            ayat_range = ayat_range.split('-')
            start = int(ayat_range[0])
            end = int(ayat_range[1])
            #print(ayat_range)
            for fractional in range(start, end + 1):
                coordinates.append((surah, fractional))
    return coordinates

def find_ayat_mentioned_in_all_hadith(hadith_df, save_result=False, collection="sb"):
    all_ayat= []
    ac = []
    all_hnum = []
    with tqdm.tqdm(total=len(hadith_df), desc=f'Getting ayat') as pbar:

        for index, row in hadith_df.iterrows():
            # print(index)

            #arabic_text = row[tarabic_name]
            en_text=row[english_name]
            plist = extract_coordinates_values(en_text)

            all_ayat.append(plist)
            ac.extend(plist)
            all_hnum.append(row[hadith_number_name])



            pbar.update(1)
    #print(len(all_ayat),len(ac))
    #print(set(ac))
    result_df = pd.DataFrame({'hadith_number': all_hnum, 'ayat': all_ayat})
    if save_result:
        result_df.to_excel("results/" + collection + "/verses.xlsx", index=False)

    return result_df

