import keras
import pickle
# load model function 
def load_model(path):
    my_model = keras.models.load_model(path)
    return my_model

# load pickel function 

def load_tokenizer(path):
    with open(path, 'rb') as handle:

        tokenizer = pickle.load(handle)
    return tokenizer