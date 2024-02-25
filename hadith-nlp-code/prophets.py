import pandas as pd
import tqdm
from pyarabic.araby import strip_tashkeel

from utility import tarabic_name, hadith_number_name, strip_punctuation, english_name

excel_file_path = 'dictionaries/prophets.xlsx'

# Read the Excel file into a DataFrame
df_p = pd.read_excel(excel_file_path)

def find_muhammad(ar_text):
    ar_pattern = "صَلَّى اللَّهُ عَلَيْهِ وَسَلَّمَ";
    ar_pattern = strip_tashkeel(ar_pattern)
    return ar_pattern in ar_text


def find_prophets_in_one_hadith(ar_text, en_text, col="sb"):
    ar_text = strip_punctuation(ar_text)
    ar_text = strip_tashkeel(ar_text)

    plist = []

    # if find_muhammad(ar_text):
    #     plist.append('Muhammad')

    for index, row in df_p.iterrows():


        ar_patterns = strip_tashkeel(row['ar'])
        ar_patterns = ar_patterns.split(',')

        if col == "sb":

            en_patterns = row['en'].split(',')

            flag = any(pattern.lower() in en_text.lower() for pattern in en_patterns)#en_text.contains('|'.join(en_patterns), case=False)


            flag = flag and any(pattern in ar_text for pattern in ar_patterns)#ar_text.contains('|'.join(ar_patterns), case=False)
        else:
            if  row['ID'] == "Adam":
                flag = False
            else:
                flag = any(pattern in ar_text for pattern in ar_patterns)#ar_text.contains('|'.join(ar_patterns), case=False)

        if flag:
            plist.append(row['ID'])

    return plist


def find_prophets_mentioned_in_all_hadith(hadith_df, save_result=False, collection="sb"):
    all_prophets= []
    ac = []
    all_hnum = []
    with tqdm.tqdm(total=len(hadith_df), desc=f'Getting prophets') as pbar:

        for index, row in hadith_df.iterrows():
            # print(index)

            arabic_text = row[tarabic_name]
            en_text=row[english_name]
            plist = find_prophets_in_one_hadith(arabic_text,en_text,collection)

            all_prophets.append(plist)
            ac.extend(plist)
            all_hnum.append(row[hadith_number_name])



            pbar.update(1)
    print(len(all_prophets),len(ac))
    print(set(ac))
    result_df = pd.DataFrame({'hadith_number': all_hnum, 'prophets': all_prophets})
    if save_result:
        result_df.to_excel("results/" + collection + "/prophets.xlsx", index=False)

    return result_df

