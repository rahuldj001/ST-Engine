from sentence_transformers import SentenceTransformer
import os

model_name = "sentence-transformers/all-MiniLM-L6-v2"
print(f"Loading model: {model_name}")

try:
    model = SentenceTransformer(model_name)
    print("Model loaded successfully!")
    vector = model.encode("test").tolist()
    print(f"Vector generated with dimension: {len(vector)}")
except Exception as e:
    print(f"Error loading model: {e}")
