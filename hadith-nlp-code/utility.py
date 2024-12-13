import re
import string
import pandas as pd
import subprocess

# Constants for column names
hadith_number_name = '~hadith_number_roman~'
tarabic_name = '~arabic_t~'
english_name = '~english~'

# Function to clean Arabic text
def clean_arabic_text(text):
    """
    Removes English characters and extra spaces from Arabic text.
    Args:
        text (str): Input Arabic text.
    Returns:
        str: Cleaned Arabic text.
    """
    text = re.sub(r'[a-zA-Z]', '', text)  # Remove English characters
    text = re.sub(r'\s+', ' ', text)      # Remove extra spaces
    return text


# Function to save a matrix to a CSV file
def save_matrix_to_csv(matrix, filename):
    """
    Saves a matrix as a CSV file.
    Args:
        matrix (list): List of lists representing the matrix.
        filename (str): Filename for the CSV file.
    """
    pd.DataFrame(matrix).to_csv(f"results/similarity_measures/{filename}", index=False, header=False)


# Function to play a default sound
def play_default_sound():
    """
    Plays a default system sound. Only works on macOS systems with afplay utility.
    """
    try:
        subprocess.run(["afplay", "/System/Library/Sounds/Ping.aiff"])
    except Exception as e:
        print(f"Error: {e}")


# Function to remove punctuation and unwanted characters
def strip_punctuation(text):
    """
    Removes punctuation and specific unwanted characters from the text.
    Args:
        text (str): Input text.
    Returns:
        str: Text without punctuation.
    """
    translator = str.maketrans("", "", string.punctuation + '،' + '~')
    return text.translate(translator)


# Function to display resolved entities
def display_resolved_entities(resolved_entities):
    """
    Displays resolved entities for debugging or logging purposes.
    Args:
        resolved_entities (list): List of tuples (entity, label).
    """
    for entity, label in resolved_entities:
        print(f"Entity: {entity}, Label: {label}")


# Function to resolve entities with B, I, O tagging
def Resolve_Entities(entities, display=False):
    """
    Resolves entities based on B-, I-, and O- tagging schemes.
    Args:
        entities (list): List of tuples (entity, label).
        display (bool): If True, resolved entities are printed.
    Returns:
        list: List of resolved entities as tuples (entity, label).
    """
    resolved_entities = []
    current_entity = ""
    current_label = ""
    prev_label = ""

    for entity, label in entities:
        # Handle B- prefix: Start of a new entity
        if label.startswith("B-"):
            if current_entity:  # Save the previous entity if it exists
                lbl = prev_label if not current_label else current_label
                resolved_entities.append((current_entity, lbl))
            current_entity = entity
            current_label = label[2:]  # Remove 'B-' prefix

        # Handle I- prefix: Continuation of the same entity
        elif label.startswith("I-"):
            if label[2:] == current_label:
                current_entity += " " + entity
            else:  # Handle mismatch or new entity start
                if current_entity:
                    resolved_entities.append((current_entity, current_label))
                current_entity = entity
                current_label = label[2:]

        # Handle O label: End of the current entity
        elif label == "O":
            if current_entity:
                lbl = prev_label if not current_label else current_label
                resolved_entities.append((current_entity, lbl))
                current_entity = ""
                current_label = ""

    # Add the last entity if it exists
    if current_entity:
        resolved_entities.append((current_entity, current_label))

    # Display entities if requested
    if display:
        display_resolved_entities(resolved_entities)

    return resolved_entities
