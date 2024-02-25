import pandas as pd
import tqdm
from pyarabic.araby import strip_tashkeel

from utility import tarabic_name, hadith_number_name, strip_punctuation, english_name

excel_file_path = 'dictionaries/plants.csv'

# Read the Excel file into a DataFrame
df_q = pd.read_csv(excel_file_path)






def find_plants_in_one_hadith(ar_text, en_text, df=df_q):
    ar_text = strip_punctuation(ar_text)
    en_text = strip_punctuation(en_text)
    ar_text = strip_tashkeel(ar_text)

    plist = []

    for index, row in df.iterrows():

        #flag = False

        # if row['ar']=='-':#'Dajjal' or row['ID']!='satan,iblis':
        #     #print(row)
        en_patterns = row['en'].split('-')
        flag = any(pattern.lower() in en_text.lower() for pattern in en_patterns)

        #else:
        # ar_patterns = strip_tashkeel(row['ar'])
        # ar_patterns = ar_patterns.split(',')
        # flag = flag or any(
        #     pattern in ar_text for pattern in ar_patterns)  # ar_text.contains('|'.join(ar_patterns), case=False)

        #flag = any(pattern.lower() in en_text.lower() for pattern in en_patterns)#en_text.contains('|'.join(en_patterns), case=False)


        if flag:
            plist.append(row['ID'])

    return plist


def find_plants_mentioned_in_all_hadith(hadith_df, save_result=False, save_file_path=""):
    all_c= []
    ac = []
    all_hnum = []
    with tqdm.tqdm(total=len(hadith_df), desc=f'Getting animals') as pbar:

        for index, row in hadith_df.iterrows():
            # print(index)

            arabic_text = row[tarabic_name]
            en_text=row[english_name]
            plist = find_plants_in_one_hadith(arabic_text,en_text)

            all_c.append(plist)
            ac.extend(plist)
            all_hnum.append(row[hadith_number_name])



            pbar.update(1)
    print(len(all_c),len(ac))
    print(set(ac))
    result_df = pd.DataFrame({'hadith_number': all_hnum, 'plants': all_c})
    if save_result:
        result_df.to_excel(save_file_path,index=False)

    return result_df

