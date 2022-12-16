import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')
import re
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

CLASS_CODE = {"Договоры оказания услуг": 1,
              "Договоры аренды": 2, 
              "Договоры купли-продажи": 3, 
              "Договоры поставки": 4, 
              "Договоры подряда": 5}

def text_class_preprocess(class_name):
    class_name = class_name.replace("Договоры для акселератора/", "")
    return class_name

def text_preprocess(text):
    text = text.replace("Evaluation Only. Created with Aspose.Words. Copyright 2003-2022 Aspose Pty Ltd.", "")
    text = text.replace("Created with an evaluation copy of Aspose.Words. To discover the full versions of our APIs please visit: https://products.aspose.com/words/", "")
    text = text.replace('\t', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace(u'\xa0', u' ')
    text = text.replace(u'\x07', u' ')
    text = text.replace(u'\x13', u' ')
    text = text.replace(u'\x14', u' ')
    text = text.replace(u'\x15', u' ')
    regular = r'[\*+\#+\№\"\-+\+\=+\?+\_+\«+\»+\!+\&\^\.+\;\,+\>+\(\)\/+\:\\+]'
    text = re.sub(regular, '', text)
    text = re.sub(r'(\d+\s\d+)|(\d+)','', text)
    return text

def lemmatize(doc):
    patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-…]+"
    stopwords_ru = stopwords.words("russian")
    morph = MorphAnalyzer()
    doc = re.sub(patterns, ' ', doc)
    tokens = []
    for token in doc.split():
        if token and token not in stopwords_ru:
            token = token.strip()
            token = morph.normal_forms(token)[0]
            
            tokens.append(token)
    doc_text = ' '.join([token for token in tokens])
    return doc_text

def data_preprocess(dataset):
    dataset["file_class"] = dataset["file_class"].apply(text_class_preprocess)
    dataset["file_class"] = dataset["file_class"].map(CLASS_CODE)
    dataset["file_body"] = dataset["file_body"].apply(text_preprocess)
    dataset["file_body"] = dataset["file_body"].apply(lemmatize)
    return dataset

def get_scores(data):
# загрузка и обработка датасета
    print(data)
    train_dataset = pd.read_json(data).T
    train_dataset = data_preprocess(train_dataset)

# модель tf-idf
    tfidf_vectorizer = TfidfVectorizer(preprocessor=text_preprocess)
    tfidf = tfidf_vectorizer.fit_transform(train_dataset.file_body.values)

# вывод из модели
    data = tfidf.todense().tolist()
    names = tfidf_vectorizer.get_feature_names_out()
    word_df = pd.DataFrame(data, columns = names)

# готовим выводы из модели
    pickled_model = pickle.load(open('model.pkl', 'rb'))

# получаем из заранее готовой модели вывод для фронта
    a = pickled_model.predict_proba(word_df)
    probabilities = [i for i in a]

    probabilities_1 = [i[0] for i in probabilities]
    probabilities_2 = [i[1] for i in probabilities]
    probabilities_3 = [i[2] for i in probabilities]
    probabilities_4 = [i[3] for i in probabilities]
    probabilities_5 = [i[4] for i in probabilities]

    answer = {
        'id':train_dataset.iloc[word_df.index]['file_id'],
        'Вероятность Договоры аренды' : probabilities_1,
        'Вероястность Договоры купли-продажи' : probabilities_2,
        'Вероястность Договоры оказания услуг' : probabilities_3,
        'Вероястность Договоры подряда' : probabilities_4,
        'Вероястность Договоры поставки' : probabilities_5
    }
    
    print(answer)
    return answer
