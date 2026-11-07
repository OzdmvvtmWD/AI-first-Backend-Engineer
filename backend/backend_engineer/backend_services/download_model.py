import os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    os.environ["SENTENCE_TRANSFORMERS_MODEL"],
    cache_folder=os.environ["SENTENCE_TRANSFORMERS_HOME"]
)

print("Embedding model downloaded successfully!")