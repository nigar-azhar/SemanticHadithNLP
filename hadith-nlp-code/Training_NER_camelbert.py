import spacy
from spacy.training.example import Example
from spacy.util import minibatch
from tqdm import tqdm
import random
import json
#from spacy_transformers import TransformersLanguage, TransformersWordPiecer, TransformersTok2Vec

from seqeval.metrics import classification_report, accuracy_score, f1_score

# Initialize a list to store metrics for each epoch
metrics_log = []

PRE_TRAINED_MODEL = "CAMeL-Lab/bert-base-arabic-camelbert-ca-ner"

# Load preprocessed training data
with open("training_dataset/customized-caner.json", "r", encoding="utf-8") as f:
    train_data = json.load(f)

# Split data into training and validation sets
train_size = int(0.8 * len(train_data))  # 80% for training
train_dataset = train_data[:train_size]
val_dataset = train_data[train_size:]  # 20% for validation

# Create a blank Arabic pipeline
nlp = spacy.blank("ar")

# Add the transformer component
transformer = nlp.add_pipe(
    "transformer",
    config={
        "model": {
            "@architectures": "spacy-transformers.TransformerModel.v3",
            "name": PRE_TRAINED_MODEL,  # The Hugging Face model name
            "tokenizer_config": {"use_fast": True},  # Use the fast tokenizer
            "transformer_config": {"output_hidden_states": True},  # Include hidden states
        }
    },
)

# Add the NER pipeline
ner = nlp.add_pipe("ner", last=True)

# Add labels to the NER model
for _, annotations in train_dataset:
    for ent in annotations["entities"]:
        ner.add_label(ent[2])

# Disable other pipelines during training
pipe_exceptions = ["transformer", "ner"]
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

# Begin training
optimizer = nlp.begin_training()
n_iter = 20  # Number of training iterations
batch_size = 32  # Adjust based on memory capacity


def evaluate_model(nlp, val_dataset):
    """
    Evaluate the SpaCy NER model on a validation set.
    Args:
        nlp: Trained SpaCy NER model.
        val_dataset: Validation data in SpaCy format.
    Returns:
        metrics: Dictionary with accuracy, precision, recall, and F1-score.
    """
    true_labels = []
    pred_labels = []

    for text, annotations in val_dataset:
        # True entities
        entities = annotations["entities"]
        true = ['O'] * len(text)  # Default to "O" (non-entity)
        for start, end, label in entities:
            for i in range(start, end):
                true[i] = label

        # Predicted entities
        doc = nlp(text)
        pred = ['O'] * len(text)  # Default to "O" (non-entity)
        for ent in doc.ents:
            for i in range(ent.start_char, ent.end_char):
                pred[i] = ent.label_

        # Align lengths
        min_len = min(len(true), len(pred))
        true_labels.append(true[:min_len])
        pred_labels.append(pred[:min_len])

    # Calculate metrics
    accuracy = accuracy_score(true_labels, pred_labels)
    f1 = f1_score(true_labels, pred_labels)
    report = classification_report(true_labels, pred_labels)
    return {
        "accuracy": accuracy,
        "f1": f1,
        "classification_report": report,
    }


print("Metrics before training:")
metrics = evaluate_model(nlp, val_dataset)
print(f"Epoch 0: Accuracy: {metrics['accuracy']:.4f}, F1-Score: {metrics['f1']:.4f}")
print(metrics["classification_report"])

print("Starting training...")
for epoch in range(n_iter):
    random.shuffle(train_dataset)
    losses = {}
    with nlp.select_pipes(disable=unaffected_pipes):
        with tqdm(total=len(train_dataset), desc=f"Epoch {epoch + 1}/{n_iter}") as pbar:
            for batch in minibatch(train_dataset, size=batch_size):
                examples = []
                for text, annotations in batch:
                    doc = nlp.make_doc(text)
                    examples.append(Example.from_dict(doc, annotations))

                # Update the model with the current batch
                nlp.update(
                    examples,
                    drop=0.2,  # Dropout for regularization
                    losses=losses,
                    sgd=optimizer,
                )
                pbar.update(len(batch))
    print(f"Epoch {epoch + 1}, Loss: {losses['ner']:.4f}")

    # Evaluate the model after each epoch
    metrics = evaluate_model(nlp, val_dataset)
    print(f"Epoch {epoch + 1} Accuracy: {metrics['accuracy']:.4f}, F1-Score: {metrics['f1']:.4f}")
    print(metrics["classification_report"])

    # Log metrics
    epoch_metrics = {
        "epoch": epoch + 1,
        "loss": losses["ner"],
        "accuracy": metrics["accuracy"],
        "f1_score": metrics["f1"],
        "class_metrics": metrics["classification_report"],  # Full classification report
    }
    metrics_log.append(epoch_metrics)

    # Save the trained model
    output_dir = f"trained_models/finetune/camel/{epoch+1}_caner_customized_ner_model"
    nlp.to_disk(output_dir)
    print(f"Model saved to {output_dir}")

# Save metrics to a JSON file
with open("trained_models/finetune/camel/training_metrics_with_classes_camel.json", "w", encoding="utf-8") as f:
    json.dump(metrics_log, f, ensure_ascii=False, indent=4)
