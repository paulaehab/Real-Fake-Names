import argparse
from textPreprocessing import text_padding
from loadModel import load_model ,load_tokenizer
from normalizeText import normalize_arabic
import time

# load machine learning model 
my_model = load_model('../machine_models/normalized_model.h5')

# load my tokenizer 
tokenizer = load_tokenizer('../machine_models/normalized_tokenizer.pickle')

if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Text string to perform detection on")
    args = vars(ap.parse_args())

    name = normalize_arabic(args["text"])
    normalized_name = list(name)

    if name:

        start_time = time.time()
        # tokenize the text
        text_tokenized= tokenizer.texts_to_sequences(name)
        # mae padd sequence on tokenized text 
        text_sequeced = text_padding(text_tokenized)
        #make model prediction 
        prediction_result=my_model.predict(text_sequeced) 
        fulltime =round(time.time() - start_time,2)


        if prediction_result[0] > 0.30:


            final= {
                "status":"Name is Real",
                "confidence":str(prediction_result[0]),
                "time taken to run":str(fulltime)
            }
            
            print(final)
        else:

            final= {
                "status":"Name is Fake",
                "confidence":str(prediction_result[0]),
                "time taken to run":str(fulltime)
            }
            
            print(final)
    