import pickle
import numpy as np
import tensorflow as tf

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


# ============================================================
# LOAD TOKENIZER
# ============================================================

print("Loading tokenizer...")

with open("model/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

print("Tokenizer loaded successfully!")


# ============================================================
# LOAD H5 MODEL
# ============================================================

print("Loading H5 model...")

model = load_model(
    "model/fake_job_lstm_model.h5"
)

print("H5 model loaded successfully!")

print("\nModel Summary:")
model.summary()


# ============================================================
# TEST JOB DESCRIPTION
# ============================================================

text = """
We are looking for a motivated employee to work remotely.
No previous experience is required.
You can earn $5000 per week.
Send your bank information to receive payment.
"""


# ============================================================
# TOKENIZE
# ============================================================

sequence = tokenizer.texts_to_sequences([text])

print("\nTokenized sequence:")
print(sequence)


# ============================================================
# PAD
# ============================================================

padded_sequence = pad_sequences(
    sequence,
    maxlen=200,
    padding="pre"
)

print("\nInput shape:")
print(padded_sequence.shape)


# ============================================================
# PREDICT
# ============================================================

prediction = model.predict(
    padded_sequence,
    verbose=0
)

print("\nRaw prediction:")
print(prediction)


# ============================================================
# RESULT
# ============================================================

probability = float(prediction[0][0])

print("\nProbability:", probability)

if probability > 0.7:

    print("Result: FRAUDULENT")

else:

    print("Result: LEGITIMATE")