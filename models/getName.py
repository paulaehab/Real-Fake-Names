
import time
from fastapi.responses import JSONResponse
from Helpers import load_model , load_tokenizer ,text_padding ,normalize_arabic
import re
# load machine learning model 
my_model = load_model('./machine_models/normalized_model.h5')

# load my tokenizer 
tokenizer = load_tokenizer('./machine_models/normalized_tokenizer.pickle')



def get_name(name):
    # start to calculate running time 
    start_time = time.time()
    # call function to normalize tha arabic text
    name = normalize_arabic(name)
    
    normalized_name = list(name)

    # tokenize the input text 
    text_tokenized= tokenizer.texts_to_sequences(normalized_name)
    # add padding to the text 
    text_sequeced = text_padding(text_tokenized)
    # make model prediction 
    prediction_result=my_model.predict(text_sequeced)

    # calculate the full time of running
    fulltime =round(time.time() - start_time,2)


    # check my threshold confidence 
    if prediction_result[0] > 0.30:

        final= {
            "status":"Name is Real",
            "confidence":str(prediction_result[0]),
            "time taken to run":str(fulltime)
        }
        
        return JSONResponse(final)
    else:

        final= {
            "status":"Name is Fake",
            "confidence":str(prediction_result[0]),
            "time taken to run":str(fulltime)
        }
        
        return JSONResponse(final)
        
           

    

    