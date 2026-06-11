import pickle
import pandas as pd

# =========================
# Load Model
# =========================
with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

# mlflow
MODEL_VERSION ='1.0.0'

# Get class labels from model (important for matching probabilities to class names)
class_labels = model.classes_.tolist()

def predict_output(user_input: dict):

    df = pd.DataFrame([user_input])

    # predict the class
    predict_class = model.predict(df)[0]

    # get probabilities for all class
    probabilities = model.predict_proba(df)[0]
    confidance = max(probabilities)

    # create mapping: {class_name: probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))

    return{
        "predicted_catagory": predict_class,
        "confidance": round(confidance, 2),
        "class_probabilities": class_probs
    }

