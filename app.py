import streamlit as st
import pickle
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

#transforming text
def transform_text(text):
    text = text.lower()#lowercase
    text = nltk.word_tokenize(text)#tokenization
    
    y=[]
    for i in text:
        if i.isalnum(): #removing speacial characters
            y.append(i)
    text = y[:]
    y.clear()
    
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
            
    text = y[:]
    y.clear()
    
    for i in text: #stemming
        y.append(ps.stem(i))
        
    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.title("Email/SMS spam Classifier")
input_sms = st.text_area("Enter the Message..")

if st.button('Predict'):



    #1.preprocess

    transformed_sms  = transform_text(input_sms)

    #2.vectorize

    vector_input = tfidf.transform([transformed_sms])

    #3.predict

    result = model.predict(vector_input)[0]

    #4.Display

    if result == 1:
        st.header("SPAM !!! Message.")
    else:
        st.header("It's not Spam message..")