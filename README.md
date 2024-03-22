# Flipkart-Sentiment-Analysis-app 📊

## 📋Overview
This project focuses on sentiment analysis of real-time product reviews from Flipkart, with a specific emphasis on the "YONEX MAVIS 350 Nylon Shuttle" product. The goal is to extract meaningful insights from customer sentiments to drive actionable strategies for product enhancement and customer satisfaction.

## 🔍Dataset 
**Source:** Real-time data from Flipkart     
**Size:** 8,518 reviews           
**Attributes:** Reviewer Name,Place of Review, Rating, Review Title, Up votes, Down votes, Month, Review Text.     

## ⛏️Data Preprocessing
**Text Cleaning:** Special characters, punctuation, and stopwords were stripped from the review text.               
**Text Normalization:** Lemmatization and stemming techniques were employed to condense words to their base forms.                         
**Numerical Feature Extraction:** Bag-of-Words (BoW), TF-IDF techniques were used to extract numerical features from the text data.             

## 🤖Modeling Approach
**Model Selection:** Various machine learning models were trained and evaluated using the processed text data.                       
**Evaluation Metric:** F1-Score was used as the evaluation metric to gauge model performance in sentiment classification.                             

## 📈Business Impact
The insights derived from this sentiment analysis project have significant implications for business decision-making, including:
- Understanding customer sentiments at scale.          
- Making data-driven decisions to enhance product offerings.        
- Optimizing customer experiences and satisfaction.                 

## 📊Usage
To use the sentiment analysis app:
- Clone this repository to your local machine.                  
- Install the required dependencies using pip install -r requirements.txt.               
- Run the Flask application using python app.py.                          
- Access the application at http://localhost:5000/ in your web browser.             

## 📝License
This project is licensed under the MIT License - see the LICENSE file for details.

