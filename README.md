# **SemanticHadithNLP**

This repository contains scripts and tools for analyzing similarity between Hadith texts, including Named Entity Recognition (NER), cosine similarity computation, and mapping Hadiths into a semantic knowledge graph. The goal is to process and identify meaningful patterns in Sahih al-Bukhari and other Hadith collections, such as Sahih Muslim, Ibn Maja, Sunan Abi Dawood, and Nisai.

---

## **Features**

- **Named Entity Recognition (NER):**
  - Utilize a custom-trained NER model to extract entities from Hadith texts, including:
    - Persons, Locations, Concepts, Crimes, and Islamic Elements (Pillars of Islam, Prophets, etc.).
  - Fine-tune and use transformer models like CAMeL-BERT or SpaCy.
- **Cosine Similarity Computation:**
  - Compute similarity scores between Hadiths using sentence embeddings with Sentence Transformers.
- **Domain-Specific Knowledge:**
  - Dictionaries provided for entities such as Prophets, Angels, Concepts, and Quranic verses for precise tagging and categorization.
- **Knowledge Graph Integration:**
  - Automatically generate RDF/Turtle files to map entities and relationships into a semantic knowledge graph.
- **Comprehensive Tools:**
  - Scripts to extract and analyze specific entity types, identify relationships, and validate results using domain knowledge.

---

## **Prerequisites**

- Python >= 3.8
- Required Python libraries (see `requirements.txt`):
  - `spacy`
  - `sentence-transformers`
  - `tqdm`
  - `pyarabic`
  - `numpy`
  - `pandas`
  - `scikit-learn`

---

## **Directory Structure**

```plaintext
SemanticHadithNLP/
│
├── data/                      # Additional datasets used for analysis or preprocessing
├── dictionaries/              # Predefined dictionaries for entity resolution
│   ├── angels.xlsx            # List of angel names and IDs
│   ├── animals.csv            # Animal-related entities
│   ├── caliphs.xlsx           # List of Caliph entities
│   ├── concepts.xlsx          # Islamic concepts and IDs
│   ├── crimes.csv             # Crime-related entities
│   ├── groupofpeople.xlsx     # Groups or clans mentioned in Hadith
│   ├── holybooks.xlsx         # Names of holy books
│   ├── pillars-of-islam.xlsx  # The five pillars of Islam
│   ├── plants.csv             # Plant-related entities
│   ├── prophets.xlsx          # List of prophets and associated entities
│
├── mappings/                  # Cross-references for Hadith to Quran and related topics
│   ├── qur-to-hadith.xlsx     # Mapping Quranic verses to Hadith IDs
│   ├── qur-topics-bukhari-books.xlsx  # Quran topics mapped to Bukhari chapters
│
├── results/                   # Outputs from NER, similarity analysis, and training
│   ├── identified_entities/   # Extracted entities from NER
│   ├── similarity_measures/   # Cosine similarity matrices
│   ├── ttl_files/             # Turtle files for knowledge graph integration
│   ├── sb/                    # Results specific to Sahih Bukhari
│
├── trained_models/            # Pretrained or fine-tuned models
│   ├── transformer_models/    # Arabic/English transformer models
│   ├── finetune/              # Fine-tuned NER models
│
├── training_dataset/          # Training datasets for NER
│   ├── customized-caner.json  # Dataset for fine-tuning the NER model
│
├── afterlife.py               # Script for analyzing entities related to Heaven and Hell
├── angels.py                  # Script for identifying angel-related entities
├── animals.py                 # Script for extracting animal mentions
├── ayat.py                    # Script for extracting Quranic verse mentions
├── caliphs.py                 # Script for identifying Caliphs in Hadith
├── caner2spacy.py             # Converter from CANER format to SpaCy-compatible format
├── concepts.py                # Extracts Islamic concepts
├── crimes.py                  # Identifies crime-related entities
├── generate_rdf.py            # Generates RDF/Turtle files for integration into a knowledge graph
├── groupofpeople.py           # Analyzes clans and group mentions in Hadith
├── holybooks.py               # Script for identifying mentions of holy books
├── locations.py               # Script for extracting locations mentioned in Hadith
├── main.py                    # Main script demonstrating full pipeline usage
├── ner_model_finetuning.py    # Fine-tuning SpaCy NER models
├── NERModelLoader.py          # Utility script for loading NER models
├── persons.py                 # Extracts mentions of persons
├── pillarsofislam.py          # Identifies mentions of the five pillars of Islam
├── plants.py                  # Script for extracting mentions of plants
├── prophets.py                # Identifies mentions of prophets in Hadith
├── similarities.py            # Script for computing and analyzing Hadith similarity
├── Training_NER_camelbert.py  # Fine-tuning code specific to CAMeL-BERT NER
├── utility.py                 # Utility functions for text preprocessing and model operations
├── visualize_training.py      # Script for visualizing training metrics
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## Usage

1. Clone this repository:

`https://github.com/nigar-azhar/SemanticHadithNLP.git`

`cd SemanticHadithNLP`

2. Install dependencies:

`pip install -r requirements.txt`


## **Preparing Data for Training**

Before training the NER model, the input data must be converted into a format compatible with SpaCy. The `caner2spacy.py` script helps in transforming the CANER dataset (or other compatible formats) into SpaCy's training format.

---

### **Usage of `caner2spacy.py`**

The script `caner2spacy.py` takes a xlsx file containing NER annotations in CANER format and converts it into a SpaCy-compatible format for training.

#### **Steps:**

1. Place your CANER-format dataset in the `training_dataset/` directory. 
   - Example file: `customized-caner.json`.

2. Run the `caner2spacy.py` script to perform the conversion:

   ```bash
   python caner2spacy.py --input "training_dataset/customized-caner.xlsx" --output "training_dataset/customized-caner.json" ```

3. Train or Fine-Tune NER Model
To train a custom NER model, edit and execute Training_NER_camelbert.py.


## **NER Expected Data Format**

For each Hadith collection, the input data is expected to be in the following format with specific column headers:

| **hadith_id** | **~hadith_number_roman~** | **~arabic_t~**                                                                                                                                                                                                                                                                                                                                                                                       | **~Tarabic~**                                                                                       | **~english~**                                                                                                                                                                                                         |
|---------------|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2             | 1                         | ~حَدَّثَنَا الْحُمَيْدِيُّ عَبْدُ اللَّهِ بْنُ الزُّبَيْرِ ، قَالَ : حَدَّثَنَا سُفْيَانُ ، قَالَ : حَدَّثَنَا يَحْيَى بْنُ سَعِيدٍ الْأَنْصَارِيُّ...~                                                                                                                                                                                                                       | ~إنما الأعمال بالنيات...~                                                                      | ~Narrated 'Umar bin Al-Khattab: I heard Allah's Apostle saying, "The reward of deeds depends upon the intentions..."~                                                                                          |
| 3             | 2                         | ~حَدَّثَنَا عَبْدُ اللَّهِ بْنُ يُوسُفَ ، قَالَ : أَخْبَرَنَا مَالِكٌ ، عَنْ هِشَامِ بْنِ عُرْوَةَ ، عَنْ أَبِيهِ ، عَنْ عَائِشَةَ أُمِّ الْمُؤْمِنِينَ...~                                                                                                                                                                                                                         | ~أحيانا يأتيني مثل صلصلة الجرس...~                                                             | ~Narrated 'Aisha: (the mother of the faithful believers) Al-Harith bin Hisham asked Allah's Apostle "O Allah's Apostle! How is the Divine Inspiration revealed to you?"~                                       |

### **Column Description**
- **hadith_id:** The unique identifier for the Hadith in the dataset.
- **~hadith_number_roman~:** The Hadith number in Roman numerals or standardized format.
- **~arabic_t~:** The original Arabic text with full punctuation.
- **~Tarabic~:** The stripped and cleaned Arabic text without punctuation or diacritics.
- **~english~:** The English translation of the Hadith.

---

## **Usage in NER Workflow**

1. Prepare your dataset in the above format for the collection of interest (e.g., Sahih al-Bukhari).
2. The columns are directly referenced in the `NER` pipeline scripts, ensuring the proper mapping of Arabic and English text during Named Entity Recognition processing.
3. Use the pre-trained or fine-tuned NER models (e.g., CAMeL-BERT) to extract entities such as persons, locations, and concepts.

---

4. Run the Main Workflow
The main.py script demonstrates the full workflow for:
- NER
- Cosine similarity computation

This script includes sample code to demonstrate the workflow of the NER and  Hadith similarity analysis. Adjust the code in `main.py` as needed for your specific use case.

5. Generate RDF/Turtle Files
To create knowledge graph data, use the generate_rdf.py script:

## Contributors
1. Nigar Azhar Butt
2. [Amna Binte Kamran](https://scholar.google.com/citations?user=RJoQH-IAAAAJ&hl=en&oi=ao)

## References
Kamran, A. B., Abro, B., & Basharat, A. (2023). SemanticHadith: An ontology-driven knowledge graph for the hadith corpus. Journal of Web Semantics, 78, 100797.

Salah, R. E., & Zakaria, L. Q. B. (2018, March). Building the classical Arabic named entity recognition corpus (CANERCorpus). In 2018 Fourth International Conference on Information Retrieval and Knowledge Management (CAMP) (pp. 1-8). IEEE.

## Contact

Contact nigar.azhar@isb.nu.edu.pk or amna.kamran@nu.edu.pk or amna.basharat@nu.edu.pk

Feel free to contact us in case of any confusions.
