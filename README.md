# NFL Big Data Bowl 2025: Play Type Classification

## Table of Contents

- [NFL Big Data Bowl 2025: Play Type Classification](#nfl-big-data-bowl-2025-play-type-classification)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Football Concepts for Context](#football-concepts-for-context)
  - [Data Exploration and Preprocessing](#data-exploration-and-preprocessing)
    - [Dataset Files](#dataset-files)
    - [Key Steps](#key-steps)
  - [Feature Engineering](#feature-engineering)
  - [Model Building](#model-building)
    - [Models Implemented:](#models-implemented)
    - [Files:](#files)
  - [Results and Interpretations](#results-and-interpretations)
  - [How to Run the Project](#how-to-run-the-project)
    - [Prerequisites](#prerequisites)
    - [Steps:](#steps)
  - [Deliverables](#deliverables)
  - [Credits](#credits)

---

## Introduction

This project is part of the **NFL Big Data Bowl 2025** ([Kaggle link](https://www.kaggle.com/competitions/nfl-big-data-bowl-2025)). The objective is to classify play types — **Run** or **Pass** — using machine learning techniques on tracking data collected before the snap. This includes:

- Player movement metrics
- Pre-snap behaviors
- Derived position-based features

---

## Football Concepts for Context

To understand the dataset and predictions:

- **Pre-snap:** The phase before the play begins where players position themselves.
- **Line of Scrimmage:** The starting line for both teams.
- **Player Movement:** Focus on **WR** (Wide Receiver) and **RB** (Running Back), key indicators of play type.

---

## Data Exploration and Preprocessing

### Dataset Files

The project uses the following datasets:

1. **games.csv**: Game-level metadata
2. **plays.csv**: Play-by-play details
3. **players.csv**: Player-specific details
4. **tracking*week*[week].csv**: Real-time player tracking data
5. **combined_data.csv**: The cleaned and engineered dataset for model input.

### Key Steps

- Missing value removal
- Column filtering for relevant features
- Addressing class imbalance for _Run_ vs _Pass_

---

## Feature Engineering

The script [`create_combined_data.ipynb`](create_combined_data.ipynb) includes:

- Summation of player movement pre-snap
- Position-based distance calculations (`distance_WR`, `distance_RB`, etc.)
- Combining relevant datasets into `combined_data.csv`

---

## Model Building

### Models Implemented:

1. **Random Forest Classifier**
   - 100 trees, max depth = 12
   - Tuned using `TunedThresholdClassifierCV`
2. **Linear Regression**
   - Attempted but failed due to lack of trends.

### Files:

- [`final_model.ipynb`](final_model.ipynb): Final optimized Random Forest model
- [`previous_models.ipynb`](previous_models.ipynb): Earlier model experiments

---

## Results and Interpretations

- **Training Accuracy:** 86%
- **Test Accuracy:** 69%
- The model emphasizes _class-1 accuracy_ (predicting **pass plays**) due to higher consequence for misclassifications.

---

## How to Run the Project

### Prerequisites

- Python 3.x
- Required libraries: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `jupyter`

### Steps:

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/nfl-playtype-classifier.git
   cd nfl-playtype-classifier
   ```
2. Ensure the datasets are present:

   - `combined_data.csv`
   - Required input files (`games.csv`, `plays.csv`, etc.)
   - The input files can be downloaded directly from the kaggle website using the link above
     - Disclaimer: The input files are 8.17GB total and require a kaggle account

3. Run the feature engineering script:

   ```bash
   jupyter notebook create_combined_data.ipynb
   ```

4. Train and evaluate the model:
   ```bash
   jupyter notebook final_model.ipynb
   ```

---

## Deliverables

- **Classification Algorithm:** [final_model.ipynb](final_model.ipynb)
- **Feature Engineering Code:** [create_combined_data.ipynb](create_combined_data.ipynb)
- **Testing Statistics:** Included in the project report.
- **Documentation:** [`README.md`](README.md)

---

## Credits

- **Authors:** Abe Raouh and Benjamin Castle
- **Course:** CISC 5790
- **Instructor:** Dr. Zhao Yijun
