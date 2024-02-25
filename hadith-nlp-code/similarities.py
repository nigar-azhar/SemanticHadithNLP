import pandas as pd
import tqdm
from pyarabic.araby import strip_tashkeel
import re
from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances, cosine_similarity
import ast
#from scipy.spatial.distance import minkowski, jaccard, hamming, jensenshannon
import numpy as np
from sentence_transformers import SentenceTransformer, util
from utility import tarabic_name, hadith_number_name, strip_punctuation, english_name, play_default_sound, \
    save_matrix_to_csv

modelPath = "trained_models/transformer_models/"

# Load pre-trained BERT model
english_model = SentenceTransformer(modelPath+"en")#('paraphrase-MiniLM-L6-v2')
english_model.save(modelPath+"en")
arabic_model = SentenceTransformer(modelPath+"ar")#('asafaya/bert-base-arabic')
arabic_model.save(modelPath+"ar")

def get_english_encoding(sentence):
    #sentence = str(sentence)
    #print(sentence)
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', sentence)
    embedding = english_model.encode(cleaned_text, convert_to_tensor=True)
    return embedding

def get_arabic_encoding(sentence):
    #sentence = str(sentence)
    #print(sentence)
    cleaned_text = strip_tashkeel(sentence)
    embedding = arabic_model.encode(cleaned_text, convert_to_tensor=True)
    return embedding





def encode_all_hadith(hadith_df, save_result=False, save_file_path=""):
    all_similarities = []
    issues = []
    all_encodings = []
    try:
        with tqdm.tqdm(total=len(hadith_df), desc=f'Generating encodings') as pbar:
            # Iterate over each row in the DataFrame
            for index, row in hadith_df.iterrows():
                # Iterate over the values in the row until NaN is encountered
                # l1 = []
                hid = int(row[hadith_number_name])

                ar_text = row[tarabic_name]
                en_text = row[english_name]

                ar_text = strip_punctuation(ar_text)
                ar_text = strip_tashkeel(ar_text)

                en_text = strip_punctuation(en_text)

                eng_hid_encoding = get_english_encoding(en_text)
                ar_hid_encoding = get_arabic_encoding(ar_text)

                all_encodings.append([hid, ar_hid_encoding.tolist(), eng_hid_encoding.tolist()])

                pbar.update(1)
    finally:
        play_default_sound()

    # Column names
    column_names = ['hadith_number', 'ar_encodings', 'eng_encodings']

    # Create a DataFrame
    result_df = pd.DataFrame(all_encodings, columns=column_names)

    if save_result:
        # Write to CSV
        result_df.to_excel(save_file_path, index=False)

    return result_df


def calculate_cosine_similarity(file_path="results/buhkari_encodings.xlsx"):
    df_encodings=pd.read_excel(file_path)
    # # Extract vectors from DataFrame
    # Assuming df is your DataFrame and encodings_column is the column containing string representations of lists
    df_encodings['ar_encodings'] = df_encodings['ar_encodings'].apply(ast.literal_eval)
    df_encodings['eng_encodings'] = df_encodings['eng_encodings'].apply(ast.literal_eval)
    # Extract tensors from DataFrame
    ar_vectors = np.array(df_encodings['ar_encodings'].tolist(), dtype=float)#np.array(df_encodings['ar_encodings'])
    eng_vectors = np.array(df_encodings['eng_encodings'].tolist(), dtype=float)#np.array(df_encodings['eng_encodings'])

    # Cosine Similarity
    cosine_similarity_matrix_ar = cosine_similarity(ar_vectors)
    cosine_similarity_matrix_ar = np.round(cosine_similarity_matrix_ar, 5)
    save_matrix_to_csv(cosine_similarity_matrix_ar, 'cosine_similarity_arabic.csv')
    play_default_sound()
    cosine_similarity_matrix_eng = cosine_similarity(eng_vectors)
    cosine_similarity_matrix_eng = np.round(cosine_similarity_matrix_eng, 5)
    save_matrix_to_csv(cosine_similarity_matrix_eng, 'cosine_similarity_english.csv')
    play_default_sound()



def calculate_euclidean_similarity(file_path="results/buhkari_encodings.xlsx"):
    df_encodings=pd.read_excel(file_path)
    # # Extract vectors from DataFrame
    # Assuming df is your DataFrame and encodings_column is the column containing string representations of lists
    df_encodings['ar_encodings'] = df_encodings['ar_encodings'].apply(ast.literal_eval)
    df_encodings['eng_encodings'] = df_encodings['eng_encodings'].apply(ast.literal_eval)
    # Extract tensors from DataFrame
    ar_vectors = np.array(df_encodings['ar_encodings'].tolist(), dtype=float)#np.array(df_encodings['ar_encodings'])
    eng_vectors = np.array(df_encodings['eng_encodings'].tolist(), dtype=float)#np.array(df_encodings['eng_encodings'])

    # Euclidean Distance
    euclidean_dist_matrix_ar = euclidean_distances(ar_vectors)
    euclidean_dist_matrix_ar = np.round(euclidean_dist_matrix_ar)
    save_matrix_to_csv(euclidean_dist_matrix_ar, 'euclidean_distance_arabic.csv')
    play_default_sound()
    euclidean_dist_matrix_eng = euclidean_distances(eng_vectors)
    euclidean_dist_matrix_eng = np.round(euclidean_dist_matrix_eng)
    save_matrix_to_csv(euclidean_dist_matrix_eng, 'euclidean_distance_english.csv')
    play_default_sound()

def calculate_euclidean_similarity(file_path="results/buhkari_encodings.xlsx"):
    df_encodings=pd.read_excel(file_path)
    # # Extract vectors from DataFrame
    # Assuming df is your DataFrame and encodings_column is the column containing string representations of lists
    df_encodings['ar_encodings'] = df_encodings['ar_encodings'].apply(ast.literal_eval)
    df_encodings['eng_encodings'] = df_encodings['eng_encodings'].apply(ast.literal_eval)
    # Extract tensors from DataFrame
    ar_vectors = np.array(df_encodings['ar_encodings'].tolist(), dtype=float)#np.array(df_encodings['ar_encodings'])
    eng_vectors = np.array(df_encodings['eng_encodings'].tolist(), dtype=float)#np.array(df_encodings['eng_encodings'])

    # Euclidean Distance
    euclidean_dist_matrix_ar = euclidean_distances(ar_vectors)
    euclidean_dist_matrix_ar = np.round(euclidean_dist_matrix_ar)
    save_matrix_to_csv(euclidean_dist_matrix_ar, 'euclidean_distance_arabic.csv')
    play_default_sound()
    euclidean_dist_matrix_eng = euclidean_distances(eng_vectors)
    euclidean_dist_matrix_eng = np.round(euclidean_dist_matrix_eng)
    save_matrix_to_csv(euclidean_dist_matrix_eng, 'euclidean_distance_english.csv')
    play_default_sound()


def calculate_manhattan_similarity(file_path="results/buhkari_encodings.xlsx"):
    df_encodings=pd.read_excel(file_path)
    # # Extract vectors from DataFrame
    # Assuming df is your DataFrame and encodings_column is the column containing string representations of lists
    df_encodings['ar_encodings'] = df_encodings['ar_encodings'].apply(ast.literal_eval)
    df_encodings['eng_encodings'] = df_encodings['eng_encodings'].apply(ast.literal_eval)
    # Extract tensors from DataFrame
    ar_vectors = np.array(df_encodings['ar_encodings'].tolist(), dtype=float)#np.array(df_encodings['ar_encodings'])
    eng_vectors = np.array(df_encodings['eng_encodings'].tolist(), dtype=float)#np.array(df_encodings['eng_encodings'])

    # Manhattan Distance
    manhattan_dist_matrix_ar = manhattan_distances(ar_vectors)
    manhattan_dist_matrix_ar = np.round(manhattan_dist_matrix_ar)
    save_matrix_to_csv(manhattan_dist_matrix_ar, 'manhattan_distance_arabic.csv')
    play_default_sound()
    manhattan_dist_matrix_eng = manhattan_distances(eng_vectors)
    manhattan_dist_matrix_eng = np.round(manhattan_dist_matrix_eng)
    save_matrix_to_csv(manhattan_dist_matrix_eng, 'manhattan_distance_english.csv')
    play_default_sound()

def find_similar_hadith(measure="cosine"):
    # Read the CSV file containing the similarity matrix
    df_ar = pd.read_csv("results/similarity_measures/"+measure+'_distance_arabic.csv', header=None)  # Adjust the filename as per your actual file
    df_en = pd.read_csv("results/similarity_measures/" + measure + '_distance_english.csv',
                        header=None)  # Adjust the filename as per your actual file



    alist = []
    with tqdm.tqdm(total=len(df_en), desc=f'Getting similar '+measure) as pbar:
        # Iterate through the elements of the matrix to check for values greater than 0.9
        for i in range(df_ar.shape[0]):
            plist =[]
            for j in range(i, df_ar.shape[1]):
                similarity_value_ar = df_ar.iloc[i, j]
                similarity_value_en = df_en.iloc[i, j]
                if similarity_value_ar > 0.9 and similarity_value_en > 0.9:
                    plist.append(j+1)
                    #print(f"Similarity value at position ({i}, {j}) is greater than 0.9: {similarity_value}")

            alist.append([i+1,plist])
            pbar.update(1)

        # Column names
        column_names = ['hadith_number', 'similar']

        # Create a DataFrame
        result_df = pd.DataFrame(alist, columns=column_names)
        # Save the DataFrame to a CSV file
        result_df.to_csv("results/similar_hadith_"+measure+".csv", index=False)

def find_similarity_values_mukarrat_hadith(df, measure="cosine"):
    # Read the CSV file containing the similarity matrix
    df_ar = pd.read_csv("results/sb/similarity_measures/"+measure+'_similarity_arabic.csv', header=None)  # Adjust the filename as per your actual file
    df_en = pd.read_csv("results/sb/similarity_measures/" + measure + '_similarity_english.csv',
                        header=None)  # Adjust the filename as per your actual file



    alist = []
    with tqdm.tqdm(total=len(df_en), desc=f'Getting similar '+measure) as pbar:
        # Iterate through the elements of the matrix to check for values greater than 0.9
        sims_ar = []
        sims_en = []
        for i in range(df.shape[0]):
            plist =[]
            list_9=[]
            list_8=[]
            list_7=[]
            list_6b=[]
            mukararat_str = df.iloc[i,5]
            # Remove "~" from the string
            mukararat_str = mukararat_str.replace(",~", "~")
            mukararat_str = mukararat_str.replace("~", "")

            # Split the string by commas and convert each part to an integer
            mukararat_list = [int(num.strip()) for num in mukararat_str.split(",")]

            for j in mukararat_list:
                if j!=0 and j<=7563 and j!=i:
                    similarity_value_ar = df_ar.iloc[i, j-1]
                    similarity_value_en = df_en.iloc[i, j-1]
                    sims_ar.append(similarity_value_ar)
                    sims_en.append(similarity_value_en)
                    #if similarity_value_ar > 0.9 and similarity_value_en > 0.9:
                    plist.append((j,similarity_value_ar,similarity_value_en))
                    if similarity_value_ar >= 0.9:
                        list_9.append(j)
                    elif similarity_value_ar >= 0.8:
                        list_8.append(j)
                    elif similarity_value_ar >= 0.7:
                        list_7.append(j)
                    else:
                        list_6b.append(j)

                        #print(f"Similarity value at position ({i}, {j}) is greater than 0.9: {similarity_value}")

            alist.append([i+1,plist,list_9,list_8,list_7,list_6b])
            pbar.update(1)

        # Column names
        column_names = ['hadith_number', 'similarityvalues','ar_0.9','ar_0.8','ar_0.7','ar_rest']

        # Create a DataFrame
        result_df = pd.DataFrame(alist, columns=column_names)
        # Save the DataFrame to a CSV file
        result_df.to_csv("results/sb/mukarrat_similarity.csv", index=False)

        # Calculate the histogram
        hist, bins = np.histogram(sims_ar, bins=np.arange(0, 1.1, 0.1))

        # Prepare the data to write to file
        data_to_write = [f"Bin {bins[i]:.1f}-{bins[i + 1]:.1f}: {hist[i]}\n" for i in range(len(bins) - 1)]

        # Define the file path
        file_path = "results/sb/similarity_frequency_m_ar-2.txt"

        # Write the data to file
        with open(file_path, "w") as file:
            file.writelines(data_to_write)

        print(f"Frequency data saved to {file_path}")

        # Calculate the histogram
        hist, bins = np.histogram(sims_en, bins=np.arange(0, 1.1, 0.1))

        # Prepare the data to write to file
        data_to_write = [f"Bin {bins[i]:.1f}-{bins[i + 1]:.1f}: {hist[i]}\n" for i in range(len(bins) - 1)]

        # Define the file path
        file_path = "results/sb/similarity_frequency_m_en-2.txt"

        # Write the data to file
        with open(file_path, "w") as file:
            file.writelines(data_to_write)

        print(f"Frequency data saved to {file_path}")


def find_similarity_values_all_hadith(measure="cosine"):
    # Read the CSV file containing the similarity matrix
    df_ar = pd.read_csv("results/sb/similarity_measures/"+measure+'_similarity_arabic.csv', header=None)  # Adjust the filename as per your actual file
    df_en = pd.read_csv("results/sb/similarity_measures/" + measure + '_similarity_english.csv',
                        header=None)  # Adjust the filename as per your actual file



    alist = []
    with tqdm.tqdm(total=len(df_en), desc=f'Getting similar '+measure) as pbar:
        # Iterate through the elements of the matrix to check for values greater than 0.9
        sims_ar = []
        sims_en = []
        for i in range(df_ar.shape[0]):
            #plist =[]
            list_9=[]
            list_8=[]
            list_7=[]
            list_6b=[]
            #mukararat_str = df.iloc[i,5]
            # Remove "~" from the string
            # mukararat_str = mukararat_str.replace(",~", "~")
            # mukararat_str = mukararat_str.replace("~", "")
            #
            # # Split the string by commas and convert each part to an integer
            # mukararat_list = [int(num.strip()) for num in mukararat_str.split(",")]

            for j in range(i+1, df_ar.shape[1]):
                if  j<=7563:
                    similarity_value_ar = df_ar.iloc[i, j]
                    similarity_value_en = df_en.iloc[i, j]
                    sims_ar.append(similarity_value_ar)
                    sims_en.append(similarity_value_en)
                    #if similarity_value_ar > 0.9 and similarity_value_en > 0.9:
                    #plist.append((j,similarity_value_ar,similarity_value_en))
                    if similarity_value_ar >= 0.9:
                        list_9.append(j+1)
                    elif similarity_value_ar >= 0.8:
                        list_8.append(j+1)
                    elif similarity_value_ar >= 0.7:
                        list_7.append(j+1)
                    else:
                        list_6b.append(j+1)
                        #print(f"Similarity value at position ({i}, {j}) is greater than 0.9: {similarity_value}")

            alist.append([i+1,list_9,list_8,list_7])
            pbar.update(1)

        # Column names
        column_names = ['hadith_number','ar_0.9','ar_0.8','ar_0.7']#,'ar_rest']

        # Create a DataFrame
        result_df = pd.DataFrame(alist, columns=column_names)
        # Save the DataFrame to a CSV file
        result_df.to_csv("results/sb/all_9_8_7_r_similarity-2.csv", index=False)

        # Calculate the histogram
        hist, bins = np.histogram(sims_ar, bins=np.arange(0, 1.1, 0.1))

        # Prepare the data to write to file
        data_to_write = [f"Bin {bins[i]:.1f}-{bins[i + 1]:.1f}: {hist[i]}\n" for i in range(len(bins) - 1)]

        # Define the file path
        file_path = "results/sb/all_similarity_frequency_m_ar-2.txt"

        # Write the data to file
        with open(file_path, "w") as file:
            file.writelines(data_to_write)

        print(f"Frequency data saved to {file_path}")

        # Calculate the histogram
        hist, bins = np.histogram(sims_en, bins=np.arange(0, 1.1, 0.1))

        # Prepare the data to write to file
        data_to_write = [f"Bin {bins[i]:.1f}-{bins[i + 1]:.1f}: {hist[i]}\n" for i in range(len(bins) - 1)]

        # Define the file path
        file_path = "results/sb/all_similarity_frequency_m_en-2.txt"

        # Write the data to file
        with open(file_path, "w") as file:
            file.writelines(data_to_write)

        print(f"Frequency data saved to {file_path}")

#find_similarity_values_mukarrat_hadith()
#find_similarity_values_all_hadith()