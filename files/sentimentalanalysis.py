# -*- coding: utf-8 -*-
"""SentimentalAnalysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wy0nM_NdmFYmK3El1h1M-6aQN-ftmn_O
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import string
import nltk
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm, tqdm_notebook
tqdm.pandas()

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

data = pd.read_csv("data.csv")
data.shape

data.head()

data.tail(15)

data.info()

# Display summary statistics
print(data.describe())

data.isnull().sum()

data.dropna(subset=['Review text'], inplace=True)

data['Review text'].isnull().sum()

data.isnull().sum()

df = data[['Review text', 'Ratings']]
df.rename(columns={'Review text': 'Text'}, inplace=True)

df.shape

df.count()

df.nunique()

df['Ratings'].value_counts()

# Assuming dataset is already loaded
sns.countplot(data=data, y='Ratings', hue='Ratings', palette = 'viridis')
plt.title('Distribution of Ratings')
plt.xlabel('Emotion')
plt.ylabel('Count')
plt.show()

# Visualize distributions and relationships
sns.pairplot(data)
plt.show()

! pip install scikit-learn imbalanced-learn

from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings('ignore')

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

def classify_review(rating):
    if rating >= 3:
        return "Positive"
    else:
        return "Negative"

# Apply the classification function to the Ratings column
df['Sentiment'] = df['Ratings'].apply(classify_review)
print(df)

sns.countplot(data=df, x='Sentiment', hue='Sentiment', palette = 'viridis')
plt.title('Distribution of Ratings')
plt.xlabel('Sentiments')
plt.ylabel('Count')
plt.show()







"""## Identify input and output"""

#input data
X = df[['Text']]

# output data
y = df['Sentiment']

from sklearn.model_selection import train_test_split

# Split data into train and test sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Display the shape of the train and test sets
print("Train set shape:", X_train.shape)
print("Test set shape:", X_test.shape)

"""## Data Preprocessing"""

import re

# Data preprocessing function
def preprocess_text(text):
    # remove special characters
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^A-Za-z0-9]', ' ', text)
    text = re.sub(r'READ MORE', '', text)

    # Lowercase
    text = text.lower()

    # Remove punctuations
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Tokenization
    words = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(words)

"""### Data Preprocessing on Train data"""

from wordcloud import WordCloud
import matplotlib.pyplot as plt

def display_wordcloud(data):
    wc = WordCloud(background_color='black',
               width=1600,
               height=800).generate(' '.join(data))
    plt.figure(1,figsize=(20, 15))
    plt.imshow(wc)
    plt.axis('off')
    plt.show()

display_wordcloud(X_train['Text'])

display_wordcloud(X_train.Text[y_train=='Positive'])

display_wordcloud(X_train.Text[y_train=='Negative'])

X_train_prep = X_train['Text'].progress_apply(lambda x: preprocess_text(x))
X_train_prep.head()

"""### Data Preprocessing on Test data"""

X_test_prep = X_test['Text'].progress_apply(lambda x: preprocess_text(x))
X_test_prep.head()

"""#### Bag Of Words"""

vectorizer = CountVectorizer(max_features=5000)

"""##### ***BOW on "Train data"***"""

X_train_bow = vectorizer.fit_transform(X_train_prep)
print("Shape of input data:", X_train_bow.shape)
print("Total unique words:", len(vectorizer.vocabulary_))
print("Type of train features:", type(X_train_bow))

# Words to array
X_train_bow.toarray()

"""##### ***BOW on "Test data"***"""

X_test_bow = vectorizer.transform(X_test_prep)
print(X_test_bow.shape)

"""#### **Tf-Idf**"""

tfidf_vectorizer = TfidfVectorizer()

X_train_tfidf = tfidf_vectorizer.fit_transform(X_train_prep).toarray()

print(X_train_tfidf.shape)
X_train_tfidf[:5]

X_test_tfidf = tfidf_vectorizer.transform(X_test_prep).toarray()
X_test_tfidf.shape

X_test_tfidf[:5]

"""## Model Building on Train Data"""

import joblib
from joblib import Memory

import os
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from sklearn.model_selection import GridSearchCV
from sklearn import metrics
import warnings
warnings.filterwarnings('ignore')



"""##### BOW"""

# Commented out IPython magic to ensure Python compatibility.
cachedir = '.cache'
memory = Memory(location=cachedir, verbose=0)

pipelines = {
    'naive_bayes': Pipeline([
        ('vectorization', CountVectorizer()),
        ('classifier', MultinomialNB())
    ], memory=memory),
    'logistic_regression': Pipeline([
        ('vectorization', CountVectorizer()),
        ('classifier', LogisticRegression())
    ], memory=memory),
    'decision_tree': Pipeline([
        ('vectorization', CountVectorizer()),
        ('classifier', DecisionTreeClassifier())
    ], memory=memory),
    'svc': Pipeline([
    ('vectorization', CountVectorizer()),
    ('classifier', SVC(kernel='linear')),
    ],memory=memory)
}

# Define parameter grid for each algorithm
param_grids = {
    'naive_bayes': [
        {
            'vectorization': [CountVectorizer()],
            'vectorization__max_features' : [1000, 1500, 2000, 5000],
            'classifier__alpha' : [1, 10]
        }
    ],
    'logistic_regression': [
        {
            'vectorization': [CountVectorizer()],
            'vectorization__max_features' : [1000, 1500, 2000, 5000],
            'classifier__C': [0.1, 1, 10],
            'classifier__penalty': ['elasticnet'],
            'classifier__l1_ratio': [0.4, 0.5, 0.6],
            'classifier__solver': ['saga'],
            'classifier__class_weight': ['balanced']
        }
    ],
    'decision_tree': [
        {
            'vectorization': [CountVectorizer()],
            'vectorization__max_features' : [1000, 1500, 2000, 5000],
            'classifier__max_depth': [None, 5, 10]
        }
    ],
    'svc':[
        {
            'vectorization': [CountVectorizer()],
            'vectorization__max_df': [0.5, 0.75, 1.0],
            'vectorization__ngram_range': [(1, 1), (1, 2), (2, 2)],
            'classifier__C': [0.1, 1, 10],
        }
    ]

}

# Perform GridSearchCV for each algorithm
best_models = {}

for algo in pipelines.keys():
    print("*"*10, algo, "*"*10)
    grid_search = GridSearchCV(estimator=pipelines[algo],
                               param_grid=param_grids[algo],
                               cv=5,
                               scoring='accuracy',
                               return_train_score=True,
                               verbose=1
                              )

#     %time grid_search.fit(X_train_prep, y_train)

    best_models[algo] = grid_search.best_estimator_

    print('Score on Test Data: ', grid_search.score(X_test_prep, y_test))
    print("\n")

import os
from sklearn import metrics

for name, model in best_models.items():
    print("*" * 10, name, "*" * 10)

    joblib.dump(model, f'{name}.pkl')
    model = joblib.load(f'{name}.pkl')

    y_train_pred = model.predict(X_train_prep)
    train_accuracy = metrics.accuracy_score(y_train, y_train_pred)
    train_f1 = metrics.f1_score(y_train, y_train_pred, average='weighted')
    print("Train Accuracy Score:", train_accuracy)
    print("Train F1 Score:", train_f1)

    y_test_pred = model.predict(X_test_prep)
    test_accuracy = metrics.accuracy_score(y_test, y_test_pred)
    test_f1 = metrics.f1_score(y_test, y_test_pred, average='weighted')
    print("Test Accuracy Score:", test_accuracy)
    print("Test F1 Score:", test_f1)

    print("Model Size:", os.path.getsize(f'{name}.pkl'), "Bytes")
    print("\n")

! pip install scikit-learn imbalanced-learn





"""#### **Tfidf**"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

def multinomial_naive_bayes(X_train, y_train, X_test, y_test):
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB())
    ])

    params = {
        'tfidf__max_df': [0.25, 0.5, 0.75, 1.0],
        'tfidf__min_df': [1, 5],
        'tfidf__ngram_range': [(1, 1), (1, 2)],
        'clf__alpha': [0.1, 0.5, 1.0]
    }

    grid_search = GridSearchCV(pipeline, params, cv=3, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    train_score = best_model.score(X_train, y_train)
    test_score = best_model.score(X_test, y_test)

    print("\nMultinomial Naive Bayes:")

    # Print the scores
    print("Train Score:", train_score)
    print("Test Score:", test_score)

    y_pred = best_model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save the best model
    joblib.dump(best_model, 'best_multinomial_nb_tfidf.pkl')


def support_vector_machine(X_train, y_train, X_test, y_test):
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', SVC(kernel='linear'))
    ])

    params = {
        'tfidf__max_df': [0.25, 0.5, 0.75, 1.0],
        'tfidf__min_df': [1, 5],
        'tfidf__ngram_range': [(1, 1), (1, 2)],
        'clf__C': [0.1, 1.0, 10.0]
    }

    grid_search = GridSearchCV(pipeline, params, cv=3, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    train_score = best_model.score(X_train, y_train)
    test_score = best_model.score(X_test, y_test)

    print("\nSupport Vector Machine:")

    # Print the scores
    print("Train Score:", train_score)
    print("Test Score:", test_score)

    y_pred = best_model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save the best model
    joblib.dump(best_model, 'best_svc_tfidf.pkl')


def decision_tree(X_train, y_train, X_test, y_test):
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', DecisionTreeClassifier())
    ])

    params = {
        'tfidf__max_df': [0.25, 0.5, 0.75, 1.0],
        'tfidf__min_df': [1, 5],
        'tfidf__ngram_range': [(1, 1), (1, 2)],
        'clf__max_depth': [None, 5, 10, 20]
    }

    grid_search = GridSearchCV(pipeline, params, cv=3, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    train_score = best_model.score(X_train, y_train)
    test_score = best_model.score(X_test, y_test)

    print("\nDecision Tree:")
    # Print the scores
    print("Train Score:", train_score)
    print("Test Score:", test_score)


    y_pred = best_model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save the best model
    joblib.dump(best_model, 'best_dt_tfidf.pkl')


def random_forest(X_train, y_train, X_test, y_test):
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', RandomForestClassifier())
    ])

    params = {
        'tfidf__max_df': [0.25, 0.5, 0.75, 1.0],
        'tfidf__min_df': [1, 5],
        'tfidf__ngram_range': [(1, 1), (1, 2)],
        'clf__n_estimators': [50, 100, 200],
        'clf__max_depth': [None, 5, 10, 20]
    }

    grid_search = GridSearchCV(pipeline, params, cv=3, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    train_score = best_model.score(X_train, y_train)
    test_score = best_model.score(X_test, y_test)

    print("\nRandom Forest:")

    # Print the scores
    print("Train Score:", train_score)
    print("Test Score:", test_score)


    y_pred = best_model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save the best model
    joblib.dump(best_model, 'best_rf_tfidf.pkl')


def logistic_regression(X_train, y_train, X_test, y_test):
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression())
    ])

    params = {
        'tfidf__max_df': [0.25, 0.5, 0.75, 1.0],
        'tfidf__min_df': [1, 5],
        'tfidf__ngram_range': [(1, 1), (1, 2)],
        'clf__C': [0.1, 1.0, 10.0],
        'clf__penalty': ['l1', 'l2']
    }

    grid_search = GridSearchCV(pipeline, params, cv=3, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    train_score = best_model.score(X_train, y_train)
    test_score = best_model.score(X_test, y_test)

    print("\nLogistic Regression:")
    # Print the scores
    print("Train Score:", train_score)
    print("Test Score:", test_score)


    y_pred = best_model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save the best model
    joblib.dump(best_model, 'best_logistic_tfidf.pkl')


def k_neighbors(X_train, y_train, X_test, y_test):
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', KNeighborsClassifier())
    ])

    params = {
        'tfidf__max_df': [0.25, 0.5, 0.75, 1.0],
        'tfidf__min_df': [1, 5],
        'tfidf__ngram_range': [(1, 1), (1, 2)],
        'clf__n_neighbors': [3, 5, 10]
    }

    grid_search = GridSearchCV(pipeline, params, cv=3, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    train_score = best_model.score(X_train, y_train)
    test_score = best_model.score(X_test, y_test)

    print("\nK-Neighbors:")

    # Print the scores
    print("Train Score:", train_score)
    print("Test Score:", test_score)

    y_pred = best_model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save the best model
    joblib.dump(best_model, 'best_k_neighbors_tfidf.pkl')

# Commented out IPython magic to ensure Python compatibility.
# %time multinomial_naive_bayes(X_train_prep, y_train, X_test_prep, y_test)

support_vector_machine(X_train_prep, y_train, X_test_prep, y_test)

decision_tree(X_train_prep, y_train, X_test_prep, y_test)

random_forest(X_train_prep, y_train, X_test_prep, y_test)

logistic_regression(X_train_prep, y_train, X_test_prep, y_test)

k_neighbors(X_train_prep, y_train, X_test_prep, y_test)

# Load the desired model for prediction
load_model = joblib.load('best_rf_tfidf.pkl')

# Example new text
new_text = "damaged product, returning it"

# Preprocess the new text
preprocessed_text = preprocess_text(new_text)

# Use the loaded model to predict the emotion label
predicted_label = load_model.predict([preprocessed_text])[0]

# Output the predicted label
print("Predicted emotion label:", predicted_label)

"""#### **To balanced dataset**

from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report

from imblearn.over_sampling import SMOTE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd


# Step 1: Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(df['Text'], df['Sentiment'], test_size=0.2, random_state=42)

# Step 2: TF-IDF vectorization on train and test sets separately
tfidf_vectorizer = TfidfVectorizer()
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Now you can proceed with your modeling steps using X_resampled and y_resampled for training, and X_test_tfidf and y_test for testing


# Step 3: Class balancing on train data only
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train_tfidf, y_train)

from collections import Counter

# Count the occurrences of each class label before and after SMOTE
class_distribution_before = Counter(y_train)
class_distribution_after = Counter(y_train_balanced)

print("Class Distribution Before SMOTE:", class_distribution_before)
print("Class Distribution After SMOTE:", class_distribution_after)
"""

# Commented out IPython magic to ensure Python compatibility.
"""from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from tqdm import tqdm

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier


# Define a memory object to cache intermediate results
cachedir = '.cache'
memory = Memory(location=cachedir, verbose=0)

pipelines = {
    'naive_bayes': Pipeline([
        ('vectorization', CountVectorizer()),
        ('classifier', MultinomialNB())
    ], memory=memory),
    'decision_tree': Pipeline([
        ('vectorization', CountVectorizer()),
        ('classifier', DecisionTreeClassifier())
    ], memory=memory),
    'logistic_regression': Pipeline([
        ('vectorization', CountVectorizer()),
        ('classifier', LogisticRegression())
    ], memory=memory)
    'random_forest': Pipeline([
        ('vectorization', CountVectorizer()),
        ('classifier', RandomForestClassifier())
    ], memory=memory),
    'knn': Pipeline([
        ('vectorization', CountVectorizer()),
        ('classifier', KNeighborsClassifier())
    ], memory=memory),
    'sgd_classifier': Pipeline([
        ('vectorization', CountVectorizer()),
        ('classifier', SGDClassifier())
    ], memory=memory)
}

# Define parameter grid for each algorithm
param_grids = {
    'naive_bayes': [
        {
            'vectorization': [CountVectorizer()],
            'vectorization__max_features' : [1000, 1500, 2000, 5000],
            'classifier__alpha' : [1, 10]
        }
    ],
    'decision_tree': [
        {
            'vectorization': [CountVectorizer(), TfidfVectorizer()],
            'vectorization__max_features' : [1000, 1500, 2000, 5000],
            'classifier__max_depth': [None, 5, 10]
        }
    ],
    'logistic_regression': [
        {
            'vectorization': [CountVectorizer(), TfidfVectorizer()],
            'vectorization__max_features' : [1000, 1500, 2000, 5000],
            'classifier__C': [0.1, 1, 10],
            'classifier__penalty': ['elasticnet'],
            'classifier__l1_ratio': [0.4, 0.5, 0.6],
            'classifier__solver': ['saga'],
            'classifier__class_weight': ['balanced']
        }
    ]
}


########################################################################
# Add additional pipelines for different classification models
pipelines.update({

})

# Add parameter grids for additional classification models
param_grids.update({
    'random_forest': [
        {
            'vectorization': [CountVectorizer(), TfidfVectorizer()],
            'vectorization__max_features' : [1000, 1500, 2000, 5000],
            'classifier__n_estimators': [100, 200, 300],
            'classifier__max_depth': [None, 5, 10]
        }
    ],
    'knn': [
        {
            'vectorization': [CountVectorizer(), TfidfVectorizer()],
            'vectorization__max_features' : [1000, 1500, 2000, 5000],
            'classifier__n_neighbors': [3, 5, 7],
            'classifier__weights': ['uniform', 'distance']
        }
    ],
    'sgd_classifier': [
        {
            'vectorization': [CountVectorizer(), TfidfVectorizer()],
            'vectorization__max_features' : [1000, 1500, 2000, 5000],
            'classifier__alpha': [0.0001, 0.001, 0.01],
            'classifier__penalty': ['l2', 'l1', 'elasticnet'],
            'classifier__class_weight': ['balanced', None]
        }
    ]
})

# Perform GridSearchCV for each algorithm
best_models = {}

for algo in pipelines.keys():
    print("*"*10, algo, "*"*10)
    grid_search = GridSearchCV(estimator=pipelines[algo],
                               param_grid=param_grids[algo],
                               cv=5,
                               scoring='f1',
                               return_train_score=True,
                               verbose=1
                              )

#     %time grid_search.fit(X_train_clean, y_train)

    best_models[algo] = grid_search.best_estimator_

    print('Score on Test Data: ', grid_search.score(X_test_clean, y_test))
"""

! pip --version

! pip scikit-learn --version

