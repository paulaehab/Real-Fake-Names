import streamlit as st 
import pandas as pd 
import numpy as np 
import time
from keras_preprocessing.sequence import pad_sequences
import keras
import pickle
# import the model 
my_model = keras.models.load_model('../machine_models/normalized_model.h5')


# import the tokenizer 
with open('../machine_models/normalized_tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# set title to the streamlit
st.title('check name is fake or real')

# field to upload text 
text_uploader = st.text_input("Write the name here ")

if text_uploader is not None:
    # add button to predict 
    pred_button = st.button("check the name")


    # check if the predict button pressed 
    if pred_button:
        # split the uploaded text to list of 3 words 
        text=text_uploader.split("*")

        #start to calculate the time
        start_time = time.time()

        # tokenize the text 
        text_tokenized= tokenizer.texts_to_sequences(text)
        # add padding to text
        text_sequeced = pad_sequences(text_tokenized, padding='post',maxlen=3,truncating='post')
        # make prediction
        result=my_model.predict(text_sequeced)

        #end the time and calulate all the time
        fulltime =time.time() - start_time

        #check the confidence of the model
        if result[0] > 0.30:
            st.write("name is Real and confidance is: " , result[0])
            st.write("The runtime is: " ,round(fulltime,3))
        else:
            st.write("name is Fake and confidance is: " , result[0])
            st.write("The runtime is: " ,round(fulltime,3))

    
