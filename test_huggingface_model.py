from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


# Hugging Face model
MODEL_NAME = "rehan-ml/scamshield-scam-detector"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading model...")
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

model.eval()

print("Model loaded successfully!")


def predict_job(text):

    # Convert text into tokens
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    # Disable gradient calculation
    with torch.no_grad():
        outputs = model(**inputs)

    # Convert logits into probabilities
    probabilities = torch.softmax(outputs.logits, dim=1)

    safe_probability = probabilities[0][0].item()
    scam_probability = probabilities[0][1].item()

    # Final prediction
    if scam_probability >= 0.5:
        prediction = "Potentially Fraudulent"
    else:
        prediction = "Likely Legitimate"

    return prediction, safe_probability, scam_probability


# ----------------------------------------
# TEST JOB
# ----------------------------------------

job = """
Administrative Assistant

We are currently looking for an administrative assistant
to work remotely.

The position offers flexible working hours and weekly payments.
Candidates do not need previous experience.

Selected applicants will be required to provide personal
information during the registration process. A small refundable
processing fee may be required before employment begins.

Interested candidates should contact the recruitment manager
for further instructions.
"""


prediction, safe_prob, scam_prob = predict_job(job)


print("\n========== RESULT ==========")
print("Prediction:", prediction)
print(f"Safe Probability: {safe_prob:.2%}")
print(f"Scam Probability: {scam_prob:.2%}")