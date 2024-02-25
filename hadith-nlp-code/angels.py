import pandas as pd
import tqdm
from pyarabic.araby import strip_tashkeel

from utility import tarabic_name, hadith_number_name, strip_punctuation, english_name, clean_arabic_text

excel_file_path = 'dictionaries/angels.xlsx'

# Read the Excel file into a DataFrame
df_p = pd.read_excel(excel_file_path)




def find_angels_in_one_hadith(ar_text, en_text):
    ar_text = strip_punctuation(ar_text)
    ar_text = strip_tashkeel(ar_text)
    ar_text = clean_arabic_text(ar_text)

    plist = []

    for index, row in df_p.iterrows():
        ar_patterns = strip_tashkeel(row['ar'])
        ar_patterns = ar_patterns.split(',')

        en_patterns = row['en'].split(',')

        flag = any(pattern.lower() in en_text.lower() for pattern in en_patterns)#en_text.contains('|'.join(en_patterns), case=False)


        flag = flag and any(pattern in ar_text for pattern in ar_patterns)#ar_text.contains('|'.join(ar_patterns), case=False)
        if flag:
            plist.append(row['ID'])

    return plist


def find_angels_mentioned_in_all_hadith(hadith_df, save_result=False, collection="sb"):
    all_prophets= []
    ac = []
    all_hnum = []
    with tqdm.tqdm(total=len(hadith_df), desc=f'Getting angels') as pbar:

        for index, row in hadith_df.iterrows():
            # print(index)

            arabic_text = row[tarabic_name]
            en_text=row[english_name]
            plist = find_angels_in_one_hadith(arabic_text,en_text)

            all_prophets.append(plist)
            ac.extend(plist)
            all_hnum.append(row[hadith_number_name])



            pbar.update(1)
    print(len(all_prophets),len(ac))
    print(set(ac))
    result_df = pd.DataFrame({'hadith_number': all_hnum, 'angels': all_prophets})
    if save_result:
        result_df.to_excel("results/" + collection + "/angels.xlsx", index=False)

    return result_df

