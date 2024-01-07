# <img width="48" height="48" src="https://img.icons8.com/fluency/48/coffee-beans-.png" alt="coffee-beans-"/> Coffee Quality Dataset <img width="48" height="48" src="https://img.icons8.com/fluency/48/coffee-beans-.png" alt="coffee-beans-"/> 

Welcome to the Coffee Recommender System! This dataset contains information about various coffee blends, including detailed attributes, roaster information, objective free ratings.

## Table of Contents 

- [Overview](#overview)
- [Contents](#contents)
  - [Data Source](#data-source)
  - [Usage](#usage)
    - [Exploratory Data Analysis](#exploratory-data-analysis-eda)
- [Languages and Tools](#languages-and-tools)
    - [Python Dependencies](#python-dependencies)
- [Column Description](#column-descriptions)
  - [Coffee Description](#coffee-descriptions)
- [Limitations](#limitations)
- [Contributors](#contributors)
- [References](#references)

## Overview

This dataset is taken from [www.coffeereview.com](https://www.coffeereview.com/) and includes information relating to the coffee quality, rating, country of origin with text descriptions associated with coffee bean characteristics and origin. <br> 

This dataset considers 3282 unique coffees and recommends coffee based on the cosine similarity of the user input of the different coffee characteristics preferred: aroma, acidity, body, flavor and aftertaste. In future versions, it would be great to customise the recommendation system to the text description given in this dataset. However, overall this system is able to output the most similar coffees as per user preference. 

## Contents

Coding 
1. [`Coffee_analysis.ipynb`](https://github.com/cmorrow28/Project-4-Dream-Team/blob/main/Coding/Coffee_Analysis.ipynb) - Data Analysis and clean up
2. [`Data Engineering DB`](https://github.com/cmorrow28/Project-4-Dream-Team/blob/main/Coding/Data_Engineering.db) - Flask output for data retrieval 
3. [`New_test_Coffee_Analysis`](https://github.com/cmorrow28/Project-4-Dream-Team/blob/main/Coding/NEW_Test_Coffee_Analysis.ipynb)

Resources 
1. [`New_Coffee_Final.csv`](https://github.com/cmorrow28/Project-4-Dream-Team/blob/main/Resources/NEW_coffee_final.csv) - Completed cleaned dataset
2. [`coffee.csv`](https://github.com/cmorrow28/Project-4-Dream-Team/blob/main/Resources/coffee.csv) - Original CSV we obtained

Models
Saved `kmeans_model.joblib` and `pca_model.joblib` machine models 

## Data Source

The dataset was collected from [toferk GitHub](https://github.com/toferk/coffee-recommender/blob/master/data/coffee_clean.csv) and represents a diverse collection of high-quality coffee blends from various regions.

## Usage
### Exploratory Data Analysis (EDA)

Explore and analyze the dataset using your preferred data analysis tools. Visualize patterns, trends, and correlations among different features.

```python
# Example EDA code snippet
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
coffee_data = pd.read_csv('NEW_coffee_final.csv')

# Explore data
print(coffee_data.info())
print(coffee_data.describe())

# Visualize data
coffee_data['rating'].hist(bins=20, color='skyblue', edgecolor='black')
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.show()


``` 
## Languages and Tools
To explore and work with the Coffee Quality Dataset, you'll need the following languages and tools:

- **Python**: Most of the dataset manipulation, analysis, and machine learning tasks can be performed using Python.
- **Jupyter Notebooks**: We recommend using Jupyter Notebooks for interactive data exploration and analysis.

### Python Dependencies

You can install the required Python packages using the following command:

```bash
pip install -r requirements.txt
```

## Column Descriptions
The cleaned dataset includes the following columns:

- <b>slug:</b> Unique identifier for each coffee blend.
- <b>name:</b> Name of the coffee blend.
- <b>roaster:</b> Coffee roaster responsible for the blend.
- <b>roast:</b> Roast level of the coffee (e.g., light, medium, dark).
- <b>country_of_origin: </b>Country where the coffee beans are sourced.
- <b>desc_1: </b>Detailed description of the coffee blend.
- <b>desc_2: </b>Additional information about the coffee's origin.
- <b>rating:</b> Rating of the coffee blend.
- <b>aroma, acid, body, flavor, aftertaste:</b> Coffee quality attributes rated by users.

## Coffee Descriptions
A rating system of 1 (low) to 10 (high) for aroma, acidity, body, flavor and aftertaste, reflect both quantity (how intense) and quality (how pleasing.) <br>
Overall ratings provide a summary assessment of reviewed coffees and are based on a scale of 50 to 100. 
- Aroma
- Acidity
- Body
- Flavor
- Aftertaste
- Rating

<em>Aroma</em> <br>
A coffee’s “aroma” is its smell after water is added.

<em>Acidity</em><br> 
“Acidity” is a very desirable quality in a coffee, and is described as “brightness” when positive, or when contributing to a coffee’s flavor experience; on the other hand, acidity can be described as “sour” if it’s a negative experience. Good acidity is one that enhances a coffee’s other qualities, such as sweetness, and brings the coffee to life. If acidity is overpowering or the dominant note, it’s generally not a quality that is sought after. An exception could be Kenyan coffees, which are known for their intense acidity.

<em>Body</em><br>
This is a coffee’s texture or tactile qualities in the mouth. Body can be heavy, light, syrupy, silky, etc. Whether a coffee’s body is a negative or positive quality depends on how it interacts with a coffee’s other qualities. Both acidity and body are measured by intensity.

<em>Flavor</em><br>
“Flavor” encompasses a coffee’s principal character or its main flavor notes. Some might refer to this as the “mid-range” notes, in between a coffee’s “top” notes (which are usually brighter, acidic notes) and its lower “base” notes (which tend to be comprised of notes such as, chocolate, nut, or caramel).

<em>Aftertaste</em><br>
A coffee’s ”aftertaste” is evaluated based on the length that positive flavors linger on the palate after the coffee is spit out or swallowed. A short or unpleasant aftertaste isn’t desirable.

<em>Rating</em> <br>
The scale for the overall coffee ratings runs from 50 to 100, and reflects the reviewers’ overall subjective assessment of a coffee’s sensory profile as manifest in the five categories aroma, acidity, body and flavor and aftertaste. Overall ratings are interpreted as follows: 

| Rating Range | Description |
|--------------|-------------|
| 97+          | Means: “We have not tasted a coffee of this style as splendid as this one for a long, long time” |
| 95-96        | Perfect in structure, flawless, and shockingly distinctive and beautiful |
| 93-94        | Exceptional originality, beauty, individuality, and distinction, with no significant negative issues whatsoever |
| 91-92        | A very good to outstanding coffee with excitement and distinction in aroma and flavor – or an exceptional coffee that still perhaps has some issue that some consumers may object to but others will love – a big, slightly imbalanced acidity, for example, or an overly lush fruit |
| 89-90        | A very good coffee, drinkable, with considerable distinction and interest |
| 87-88        | An interesting coffee but either 1) distinctive yet mildly flawed, or 2) solid but not exciting |
| 85/86        | An acceptable, solid coffee, but nothing exceptional — the best high-end supermarket whole bean, for example |

## Limitations  
- Reduction in dataset due to null values
- Limitation of data analytics student compentency and understanding of systems
- Non-user review input
- Small scale dataset

## Contributors 
[Cayley Morrow](https://github.com/cmorrow28) <br> 
[Dominique Spencer](https://github.com/domspenc) <br> 
[Jesslyn Lengkong](https://github.com/jflengkong) 

## References
[1] [ScikitLearn](https://scikit-learn.org/stable/index.html)  <br> 
[2] [GitHub Icons](https://icons8.com/) <br> 
[3] [Matplotlib](https://matplotlib.org/) <br> 
[4] [ToFerk GitHub](https://github.com/toferk)  <br> 
[5] [Understanding Cosine Similatiry Math](https://www.learndatasci.com/glossary/cosine-similarity/)

For more detailed explanations of these components, refer to [Interpreting Reviews](https://www.coffeereview.com/interpret-coffee/)
https://www.coffeereview.com/ - 


