import json
import matplotlib.pyplot as plt
import pandas as pd

# Load the metrics
with open("trained_models/finetune/camel/training_metrics_with_classes_camel.json"
          , "r", encoding="utf-8") as f:
    metrics = json.load(f)


def convert_classification_report_to_df(classification_report):
    """
    Converts a string classification report to a pandas DataFrame.
    Args:
        classification_report (str): The classification report string.
    Returns:
        pd.DataFrame: DataFrame with columns ['Class', 'Precision', 'Recall', 'F1-Score', 'Support'].
    """
    # Process the string into lines
    lines = classification_report.strip().split("\n")

    # Skip the header line and extract data
    data = []
    for line in lines[2:]:  # Skip the first two lines (header and empty)
        # Split the line into parts: last 4 columns are metrics, rest is the class name
        parts = line.rsplit(maxsplit=4)
        if len(parts) >= 5:
            class_name = parts[0].strip()
            metrics = parts[1:]  # Precision, Recall, F1-Score, Support
            data.append([class_name] + metrics)

    # Create a DataFrame
    df = pd.DataFrame(data, columns=["Class", "Precision", "Recall", "F1-Score", "Support"])

    # Convert numeric columns to appropriate types
    df["Precision"] = pd.to_numeric(df["Precision"], errors="coerce")
    df["Recall"] = pd.to_numeric(df["Recall"], errors="coerce")
    df["F1-Score"] = pd.to_numeric(df["F1-Score"], errors="coerce")
    df["Support"] = pd.to_numeric(df["Support"], errors="coerce")
    # Assuming df is the DataFrame created earlier
    classes_to_remove = ["DATE", "DAY", "TIME", "PARA"]

    # Filter the DataFrame to exclude the specified classes
    df = df.loc[~df["Class"].isin(classes_to_remove)].reset_index(drop=True)

    return df


def extract_metric_over_epochs(metrics, metric_name):
    """
    Extracts a given metric (Precision, Recall, F1-Score) for all classes across all epochs.
    Args:
        metrics: List of epoch-wise classification reports.
        metric_name: Metric to extract ('Precision', 'Recall', or 'F1-Score').
    Returns:
        A dictionary where keys are class names and values are lists of the metric across epochs.
    """
    class_metrics_over_epochs = {}

    i=0

    for epoch_data in metrics:
        class_metrics = epoch_data["class_metrics"]

        df = convert_classification_report_to_df(class_metrics)



        # Append metrics for each class
        for _, row in df.iterrows():
            class_name = row["Class"]
            if class_name not in class_metrics_over_epochs:
                class_metrics_over_epochs[class_name] = []
            class_metrics_over_epochs[class_name].append(row[metric_name])
        i+=1
        if i>15:
            break

    return class_metrics_over_epochs


def plot_metric_over_epochs(metrics, metric_name, title):
    """
    Plots the given metric (Precision, Recall, F1-Score) over epochs for all classes.
    Args:
        metrics: List of epoch-wise classification reports.
        metric_name: Metric to plot ('Precision', 'Recall', or 'F1-Score').
        title: Title for the plot.
    """
    class_metrics_over_epochs = extract_metric_over_epochs(metrics, metric_name)

    # Classes to emphasize
    aggregate_classes = {"micro avg", "macro avg", "weighted avg"}

    plt.figure(figsize=(15, 8))

    for class_name, values in class_metrics_over_epochs.items():
        if class_name in aggregate_classes:
            # Bold and dark lines for aggregate metrics
            plt.plot(
                range(1, len(values) + 1),
                values,
                label=class_name,
                linewidth=1,
                marker="o"
            )
        else:
            # Lighter lines for individual classes
            plt.plot(
                range(1, len(values) + 1),
                values,
                label=class_name,
                linewidth=1,
                linestyle="--",
                alpha=0.5
            )

    plt.xlabel("Epoch")
    plt.ylabel(metric_name)
    plt.title(title)
    plt.legend(loc="upper left", bbox_to_anchor=(1.05, 1), fontsize="small")
    plt.tight_layout()
    plt.show()


# Example: Plot precision, recall, and F1-score
plot_metric_over_epochs(metrics, "Precision", "Precision Over Epochs for All Classes")
plot_metric_over_epochs(metrics, "Recall", "Recall Over Epochs for All Classes")
plot_metric_over_epochs(metrics, "F1-Score", "F1-Score Over Epochs for All Classes")
