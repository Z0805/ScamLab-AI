import pickle

MODEL_PATH = "scam_model.pkl"

# Load the trained ML model
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)


def predict_scam(text):
    """
    Predict whether a message is a scam using the trained ML model.
    """

    prediction = model.predict([text])[0]

    probability = model.predict_proba([text])[0]

    scam_probability = probability[1] * 100

    if prediction == 1:
        label = "SCAM"
    else:
        label = "NORMAL"

    return {
        "label": label,
        "scam_probability": round(scam_probability, 2)
    }