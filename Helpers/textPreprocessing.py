from keras_preprocessing.sequence import pad_sequences

# make paading ro text 
def text_padding(text):
    return pad_sequences(text, padding='post',maxlen=3,truncating='post')