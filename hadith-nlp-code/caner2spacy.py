import pandas as pd
import json


def convert_to_spacy_format(df):
    """
    Convert a token-label DataFrame into SpaCy NER format.
    Args:
        df: DataFrame with 'tokens' and 'labels' columns.
    Returns:
        List of tuples in SpaCy NER format.
    """
    train_data = []
    sentence_tokens = []
    sentence_labels = []
    token_count = 0  # Counter to track sentence length

    for _, row in df.iterrows():
        token = str(row['tokens'])
        label = row['labels']

        sentence_tokens.append(token)
        sentence_labels.append(label)
        token_count += 1

        # Check for sentence boundary conditions
        if token == "." or token == "؟" or (token_count > 10 and label == "O"):
            if sentence_tokens:  # Process the accumulated sentence
                text = " ".join(sentence_tokens)
                entities = []
                current_position = 0

                for token, label in zip(sentence_tokens, sentence_labels):
                    start = text.find(token, current_position)
                    end = start + len(token)
                    current_position = end

                    if label != "O":  # Ignore "O" labels
                        entities.append((start, end, label))

                train_data.append((text, {"entities": entities}))
                sentence_tokens = []
                sentence_labels = []
                token_count = 0  # Reset token counter for the next sentence

    # Handle the last sentence if not ended with a boundary
    if sentence_tokens:
        text = " ".join(sentence_tokens)
        entities = []
        current_position = 0
        for token, label in zip(sentence_tokens, sentence_labels):
            start = text.find(token, current_position)
            end = start + len(token)
            current_position = end
            if label != "O":
                entities.append((start, end, label))
        train_data.append((text, {"entities": entities}))

    return train_data


# Load your dataset
# Assuming your DataFrame is loaded as `df`
cleaned_canner_path = "training_dataset/customized-caner.xlsx"
df_caner = pd.read_excel(cleaned_canner_path)
df_caner.head()
df = df_caner.rename(columns={"Word": "tokens", "Acutal": "labels"}).copy()
# df = pd.read_csv("your_dataset.csv")

# Convert to SpaCy format
train_data = convert_to_spacy_format(df)

# Example output
#for data in train_data[:3]:  # Print first 3 examples
print(len(train_data))


# Convert and write JSON object to file
with open("training_dataset/customized-caner.json", "w") as outfile:
    json.dump(train_data, outfile)