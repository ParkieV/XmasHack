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
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
from backend.config import BASE_DIR

def text_class_preprocess(class_name):
    class_name = class_name.replace("Договоры для акселератора/", "")
    return class_name

def lemmatize(doc):
    stopwords_ru = stopwords.words("russian")
    morph = MorphAnalyzer()
    patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-…]+"
    doc = re.sub(patterns, ' ', doc)
    tokens = []
    for token in doc.split():
        if token and token not in stopwords_ru:
            token = token.strip()
            token = morph.normal_forms(token)[0]
            
            tokens.append(token)
    doc_text = ' '.join([token for token in tokens])
    return doc_text

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
    text = lemmatize(text)
    return text

def clf_documents(train_dataset):
    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(BASE_DIR + "/ml/vocabulary.pkl", "rb")))
    tfidf = transformer.fit_transform(loaded_vec.transform(train_dataset.file_body.values))
    data = tfidf.todense().tolist()
    names = transformer.get_feature_names_out()
    word_df = pd.DataFrame(data, columns = names)
    new_clf = pickle.load(open(BASE_DIR + "/ml/clf.pkl", "rb"))
    return new_clf.predict(word_df), new_clf.predict_proba(word_df), word_df.index

def results(train_dataset):
    CLASS_CODE_REVERSE = {1: "Договоры оказания услуг", 2: "Договоры аренды", 3: "Договоры купли-продажи", 4: "Договоры поставки", 5:"Договоры подряда"}
    y_pred, probabilities, y_index = clf_documents(train_dataset)
    file_id = train_dataset['file_id'].values
    data = {
        "file_id": [file_id[i] for i in y_index],
        "file_class":[CLASS_CODE_REVERSE[i] for i in y_pred],
        "probabilities": {
            "Договоры оказания услуг": [probability[0] for probability in probabilities],
            "Договоры аренды": [probability[1] for probability in probabilities],
            "Договоры купли-продажи": [probability[2] for probability in probabilities],
            "Договоры поставки": [probability[3] for probability in probabilities],
            "Договоры подряда": [probability[4] for probability in probabilities]}
    }

    return data

def predict_docs_class(file = None):
    CLASS_CODE = {"Договоры оказания услуг": 1, "Договоры аренды": 2, "Договоры купли-продажи": 3, "Договоры поставки": 4, "Договоры подряда": 5}
    PATH = BASE_DIR + "/ml/data.json"
    #train_dataset = pd.read_json(PATH).T
    #print(train_dataset)
    train_dataset = pd.DataFrame.from_dict(file, orient='columns').T
    print(train_dataset)
    train_dataset["file_class"] = train_dataset["file_class"].apply(text_class_preprocess)
    train_dataset["file_class"] = train_dataset["file_class"].map(CLASS_CODE)
    train_dataset["file_body"] = train_dataset["file_body"].apply(text_preprocess)
    return results(train_dataset)
