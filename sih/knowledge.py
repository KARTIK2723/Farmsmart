import google.generativeai as genai
import faiss
import numpy as np
import os

# Configure API key
genai.configure(api_key=os.getenv("AIzaSyDRKZHxENN204iyEPEy-RyVuIVak2Jl2Ss"))

# Use the correct embedding model
embedding_model = "models/embedding-001"

# Example documents
documents = [
    "FarmSmart helps farmers improve crop yield using AI-based recommendations.",
    "Our platform suggests irrigation schedules based on weather forecasts.",
    "We provide personalized fertilizer recommendations for different soil types.",
    "FarmSmart also tracks pest infestations and suggests eco-friendly solutions."
]

# Save docs
with open("documents.txt", "w", encoding="utf-8") as f:
    for doc in documents:
        f.write(doc + "\n")

# Create embeddings
embeddings = []
for doc in documents:
    result = genai.embed_content(model=embedding_model, content=doc)
    embeddings.append(result["embedding"])

embeddings = np.array(embeddings, dtype=np.float32)

# Create FAISS index
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)
faiss.write_index(index, "farm_index.faiss")

print("✅ Knowledge base created: farm_index.faiss + documents.txt")
