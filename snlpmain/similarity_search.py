import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from rankbm25 import BM250kapi
import nltk
from chunking import get_embeddings


nltk.download('punkt')
from nltk.tokenize import word_tokenize

# Load the same model
# model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

def load_chunked_data(json_file="chunked_embeddings.json"):
    """Load precomputed chunked embeddings from JSON file"""
    with open(json_file, "r") as f:
        return json.load(f)

def cosine_retrieved_chunks(query,embed_model, chunked_data, top_k=3):
    """Find the most similar chunks to a query using cosine similarity"""
    
    # Convert stored embeddings to a NumPy array
    embedding_vectors = np.array([chunk["embedding"] for chunk in chunked_data])


# get_embeddings(chunks, model_name)
    # Get embedding for query
    # query_embedding = model.encode([query], convert_to_numpy=True)

    query_embedding = get_embeddings(query, embed_model)
    # Compute cosine similarity
    similarities = cosine_similarity(query_embedding, embedding_vectors)[0]

    # Get top-k most similar chunks
    top_indices = np.argsort(similarities)[::-1][:top_k]

    # Retrieve the most similar chunks
    cosine_chunks = [chunked_data[i] for i in top_indices]

    return cosine_chunks

def BM25_retrieved_chunks(query, chunked_data, top_k):
    corpus = [word_tokenize(chunk["text"].lower()) for chunk in chunked_data]

    tokernized_query = word_tokenize(query.lower())

    bm25 = BM250kapi(corpus)

    scores = bm25.get_scores(tokernized_query)

    top_indices = sorted(range(len(scores)), key=(lambda x: scores[i]), reverse=True )[:top_k]
    
    BM25_chunks = [chunked_data[i] for i in top_indices]
    return BM25_chunks

def similarity_search_model(model,embed_model, query, chuncked_data, top_k):
    if model == "cosine":
        selected_chunks = cosine_retrieved_chunks(query,embed_model, chuncked_data, top_k=3)
    elif model == "BM25":
        selected_chunks = BM25_retrieved_chunks(query, chuncked_data, top_k)
    return selected_chunks



if __name__ == "__main__":
    # Load the stored embeddings
    chunked_data = load_chunked_data()

    # Example query
    query_text = "EXCLUSIONS AND EXEMPTIONS"


    model = "cosine"
    embed_model = "sbert"
    top_k = 3
    most_similar = similarity_search_model(model,embed_model, query_text, chunked_data, top_k)

    with open("most_similar(cosine).json", "w", encoding="utf-8") as f:
        json.dump(most_similar, f, indent=2)

    for i, chunk in enumerate(most_similar):
        print(f"Top {i+1} Similar Chunk:\n{chunk['text']}\n")



