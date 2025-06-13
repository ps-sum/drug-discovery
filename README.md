# AI Drug-Target Interaction Predictor

This project is an AI-powered system to predict drug-target interactions using SMILES strings and protein sequences. It utilizes a machine learning model trained on known interaction data to return a predicted KIBA score, indicating the strength of molecular binding. The frontend is a modern web interface connected to a Flask API backend.

Live demo: https://drug-discovery-2t0j.onrender.com/

---

## Key Features

- Flask backend with REST API architecture
- Trained Random Forest model using scikit-learn
- RDKit-based SMILES fingerprinting
- Protein k-mer sequence encoding
- Responsive frontend with disease-protein dropdowns
- JSON API for interaction prediction
- Preloaded disease-to-protein map
- Easy to deploy on Render or locally

---

## Tech Stack

**Backend**
- Python 3.11+
- Flask + Flask-CORS
- scikit-learn, joblib, numpy
- RDKit for chemical structure handling

**Frontend**
- Vanilla HTML, CSS, JavaScript
- SMILES Drawer for structure rendering
- Fetch API for async interaction

**Deployment**
- Render (live deployment)
  https://drug-discovery-2t0j.onrender.com/
- Optionally Dockerizable

---

## Frontend Features

- Drug input in SMILES format
- Protein sequence input or autofill from disease-protein mapping
- Live prediction on click
- KIBA score with binding strength classification (strong, moderate, weak)
- Dynamic dropdowns populated via API
- Canvas-based SMILES rendering
- Works without any build tools

---

## Prerequisites

- Python 3.11+
- pip (Python package manager)
- Git
- Virtual environment (recommended)

---
