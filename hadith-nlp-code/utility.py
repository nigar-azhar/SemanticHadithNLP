#from pyarabic.araby import strip_tashkeel
import re
import string
import pandas as pd
import subprocess

hadith_number_name = '~hadith_number_roman~'
tarabic_name = '~arabic_t~'
english_name = '~english~'

# Function to remove English characters and extra double spaces from Arabic text
def clean_arabic_text(text):
    # Remove English characters
    text = re.sub(r'[a-zA-Z]', '', text)
    # Remove extra double spaces
    text = re.sub(r'\s+', ' ', text)
    return text

# Function to save matrix to CSV file
def save_matrix_to_csv(matrix, filename):
    pd.DataFrame(matrix).to_csv("results/similarity_measures/"+filename, index=False, header=False)


def play_default_sound():
    try:
        # Use subprocess to call the afplay command
        subprocess.run(["afplay", "/System/Library/Sounds/Ping.aiff"])

    except Exception as e:
        print(f"Error: {e}")

def strip_punctuation(text):
    translator = str.maketrans("", "", string.punctuation + '،'+'~')
    result = text.translate(translator)
    return result


def display_resolved_entities(resolved_entities):
    # Print the resolved entities
    for entity, label in resolved_entities:
        print(f"Entity: {entity}, Label: {label}")


def Resolve_Entities(entities, display=False):
    # Assuming that 'entities' is a list of (entity, label) tuples
    resolved_entities = []

    # Keep track of the current entity and label
    current_entity = ""
    current_label = ""
    prev_label = ""

    # Iterate through the entities
    for entity, label in entities:
        #print(entity,label)
        # Resolve B, I, and O tags
        if label.startswith("B-"):
            # If a new entity begins, add the current entity to the list
            if current_entity:
                if current_label == "":
                    lbl = prev_label
                else:
                    lbl = current_label
                resolved_entities.append((current_entity, lbl))
            current_entity = entity
            current_label = label[2:]  # Remove the 'B-' prefix
        elif label.startswith("I-"):

            # If the entity continues, append the current token to the current entity
            if label[2:] == current_label:
                current_entity += " " + entity
            else:
                if current_entity != "":
                    resolved_entities.append((current_entity, current_label))
                current_entity = entity
                current_label = label[2:]

        #             if current_label == "":
        #                 current_label = label[2:]  # Remove the 'I-' prefix
        elif label == "O":
            # If it's an 'O' tag, add the current entity to the list (if any)
            # if current_label == "CLAN" and current_entity in ['بني']:
            #     print("here", entity)
            #     current_entity += " " + entity
            #     resolved_entities.append((current_entity, current_label))

            if current_entity:
                if current_label == "":
                    lbl = prev_label
                else:
                    lbl = current_label
                resolved_entities.append((current_entity, lbl))
                current_entity = ""
                #                 prev_label = current_label
                current_label = ""
        # elif label != "MISC" or label != "ORG" or label != "PER":
        #     resolved_entities.append((entity, label))


    # Add the last entity if it exists
    if current_entity:
        resolved_entities.append((current_entity, current_label))

    if display == True:
        display_resolved_entities(resolved_entities)

    return resolved_entities
