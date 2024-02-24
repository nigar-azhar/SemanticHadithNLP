# SemanticHadithNLP

This repository contains scripts and tools for analyzing similarity between Hadith texts, including Named Entity Recognition (NER) and cosine similarity computation. The goal is to identify similar Hadiths within the Sahih al-Bukhari corpus and other selected collections, such as Sahih Muslim, Ibn Maja, Sunun Abi Dawood, and Nisai.

## Features

- **Named Entity Recognition (NER):** Utilize a custom-trained NER model to extract entities from Hadith texts, including persons, locations, events, and more.
- **Cosine Similarity Computation:** Compute cosine similarity scores between pairs of Hadith texts using pretrained Arabic sentence transformers.
- **Expert Validation:** Engage domain experts to validate identified similar Hadith pairs and provide feedback on their relevance.
- **Integration into Knowledge Graph:** Map similar Hadith pairs into a knowledge graph, augmenting mappings with additional properties for highly similar pairs.

## Prerequisites

- Python 3.x
- Spacy library for NER: `pip install spacy`
- Sentence Transformers library for similarity computation: `pip install sentence-transformers`

## Usage

1. Clone this repository:

`git clone https://github.com/your-username/hadith-similarity-analysis.git`

`cd hadith-similarity-analysis`

2. Install dependencies:

`pip install -r requirements.txt`

3. Run the main.py file:
This script includes sample code to demonstrate the workflow of the NER and  Hadith similarity analysis. Adjust the code in `main.py` as needed for your specific use case.

## Contributors
1. Nigar Azhar Butt
2. Amna Binte Kamran
