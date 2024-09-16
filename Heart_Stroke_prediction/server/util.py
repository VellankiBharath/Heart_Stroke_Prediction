import json
import pickle
import numpy as np

__gender = None
__smoking_status = None
__data_columns = None
__SVM = None

def get_heart_stroke(smoking_status, gender, age, hypertension, heart_disease, avg_glucose_level, bmi):
    # Initialize feature array with zeros
    x = np.zeros(len(__data_columns))

    # Fill in the continuous features
    x[__data_columns.index('age')] = age
    x[__data_columns.index('hypertension')] = hypertension
    x[__data_columns.index('heart_disease')] = heart_disease
    x[__data_columns.index('avg_glucose_level')] = avg_glucose_level
    x[__data_columns.index('bmi')] = bmi

    # One-hot encode categorical features (gender and smoking status)
    if smoking_status in __smoking_status:
        x[__data_columns.index(smoking_status)] = 1
    else:
        raise ValueError(f"'{smoking_status}' is not a valid smoking status")

    if gender in __gender:
        x[__data_columns.index(gender)] = 1
    else:
        raise ValueError(f"'{gender}' is not a valid gender")

    # Perform the prediction using the loaded model
    return round(__SVM.predict([x])[0], 2)

def get_gender():
    return __gender

def get_smoking_status():
    return __smoking_status

def load_saved_artifacts():
    print("Loading saved artifacts: start")
    global __gender
    global __smoking_status
    global __data_columns
    global __SVM

    # Load columns.json
    with open('./artifacts/columns.json', 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __gender = __data_columns[:3]  # First 3 columns are for gender
        __smoking_status = __data_columns[3:7]  # Next 4 columns are for smoking status

    # Load the model pickle file
    with open('./artifacts/heart_stroke_prediction_model.pickle', 'rb') as f:
        __SVM = pickle.load(f)

    print("Loading saved artifacts...done")

if __name__ == "__main__":
    load_saved_artifacts()
    print(get_gender())
    print(get_smoking_status())
    print(get_heart_stroke('smokes', 'male', 20, 1, 0, 100.0, 40.0))
    print(get_heart_stroke('smokes', 'male', 50, 1, 1, 100.0, 50.0))
    print(get_heart_stroke('smokes', 'male', 80, 1, 1, 105.0, 100.0))
