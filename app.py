from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os
import json


from utils import smiles_to_fingerprint, encode_sequence


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# Load disease-to-protein mapping
with open("disease_protein_map.json") as f:
   disease_protein_map = json.load(f)


# Load model and vectorizer
model = joblib.load("rf_model.pkl")
vectorizer = joblib.load("kmer_vectorizer.pkl")
expected_features = model.n_features_in_


print("✅ Vectorizer vocabulary size:", len(vectorizer.vocabulary_))


from flask import render_template

@app.route("/")
def mine():
    return render_template("mine.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/system")
def system():
    return render_template("system.html")


@app.route("/predict", methods=["POST"])
def predict():
   data = request.get_json()
   smiles = data.get("smiles")
   sequence = data.get("sequence")


   print("🔹 Received SMILES:", smiles)
   print("🔹 Received sequence:", sequence)


   if not smiles or not sequence:
       return jsonify({"error": "Both SMILES and sequence are required."}), 400


   fp = smiles_to_fingerprint(smiles)
   if fp is None:
       return jsonify({"error": "Invalid SMILES"}), 400


   print("🔸 Fingerprint shape:", fp.shape)
   print("🔸 Fingerprint sample:", fp[:10])


   try:
       kmers = encode_sequence(sequence)
       seq_vector = vectorizer.transform([kmers]).toarray()


       print("🔹 K-mer vector shape:", seq_vector.shape)
       print("🔹 K-mer vector sample:", seq_vector[0][:10])


       combined = np.hstack([fp.reshape(1, -1), seq_vector])
       current_features = combined.shape[1]
       print("🔷 Combined feature vector shape before adjustment:", current_features)


       if current_features > expected_features:
           combined = combined[:, :expected_features]
       elif current_features < expected_features:
           padding = np.zeros((1, expected_features - current_features))
           combined = np.hstack([combined, padding])


       print("✅ Final combined shape:", combined.shape)


       score = model.predict(combined)[0]
       print("✅ Predicted KIBA score:", score)


       return jsonify({"kiba_score": float(score)})


   except Exception as e:
       print("❌ Error during prediction:", str(e))
       return jsonify({"error": str(e)}), 500


# ✅ List all diseases
@app.route("/all-diseases", methods=["GET"])
def get_diseases():
   return jsonify({"diseases": list(disease_protein_map.keys())})


# ✅ Get proteins for a specific disease
@app.route("/proteins-for-disease", methods=["GET"])
def proteins_for_disease():
   disease = request.args.get("disease")
   proteins = disease_protein_map.get(disease, [])
   return jsonify({"proteins": proteins})


if __name__ == "__main__":
   port = int(os.environ.get("PORT", 8080))
   app.run(host="0.0.0.0", port=port)




