import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split

from keras_preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras import layers
from keras.preprocessing.text import Tokenizer
from keras.layers import LSTM
from keras.callbacks import EarlyStopping
import keras
import re
from normalizeText import normalize_arabic
import pickle

# read the data 
data = pd.read_csv('../Data/final_names.csv')

# normlaize the arabic data 
data['name'] = data['name'].apply(lambda x:normalize_arabic(x) )

#split the data 

x= data['name']
y=data['status']
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.15, random_state=1000)

#intyialize the Tokenizer 
tok = Tokenizer(oov_token="<OOV>")
#fit the data on the text
tok.fit_on_texts(x)
# Tokenize the data 
X_train_tokenized = tok.texts_to_sequences(X_train)
X_test_tokenized = tok.texts_to_sequences(X_test)
# add one for the oov token 
vocab_size = len(tok.word_index) + 1  

#define the max length and embedding size 
max_len = 3
embdding_dim=20

# add padding to text 
X_train = pad_sequences(X_train_tokenized, padding='post',maxlen=max_len,truncating='post')
X_test = pad_sequences(X_test_tokenized, padding='post', maxlen=max_len,truncating='post')

# create the model 

dropout=0.4
model = Sequential()
model.add(layers.Embedding(input_dim=vocab_size,output_dim=embdding_dim,input_length=max_len))
model.add(LSTM(128, activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dropout(dropout))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

#define model checkpoint 
model_checkpoint_callback = keras.callbacks.ModelCheckpoint(
    save_weights_only=False,
    monitor='val_loss',
    save_best_only=True,
    filepath= 'model.h5')

#compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

## train the model 
history = model.fit(X_train, y_train,
                    epochs=20,
                    validation_data=(X_test, y_test),
                    batch_size=64,
                    callbacks=[model_checkpoint_callback])
loss, accuracy = model.evaluate(X_train, y_train, verbose=False)
print("Training Accuracy: {:.4f}".format(accuracy))
loss, accuracy = model.evaluate(X_test, y_test, verbose=False)
print("Testing Accuracy:  {:.4f}".format(accuracy))


# saving the tokenizer 
with open('../machine_models/normalized_tokenizer.pickle', 'wb') as handle:
    pickle.dump(tok, handle)
print('tokenizer saving is done ')


# save the model 
model.save('../machine_models/normalized_model.h5')
print('model saving is done ')