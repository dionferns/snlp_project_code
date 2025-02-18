import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
# from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import nltk
import shutil
from part1 import get_embeddings
import os

nltk.download('punkt')
from nltk.tokenize import word_tokenize

def load_chunked_data(directory="chunked_data/"):
    """Load precomputed chunked embeddings from JSON file"""
    # with open(json_file, "r") as f:
    #     return json.load(f)
    current_dir = os.path.abspath(os.path.dirname(__file__))  # Ensure absolute path
# mkae sure the chunk id values are the same you got from the part
    folder_path = os.path.join(current_dir, directory)

    chunked_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                file_data = json.load(f)
                chunked_data.extend(file_data)  #for now the chunked data contains list of chunks along with thier embeddings, and they are not seperated yet into different files which we can do.
    return chunked_data

def cosine_retrieved_chunks(query,embed_model, chunked_data, top_k=3):
    """Find the most similar chunks to a query using cosine similarity"""
    
    # Convert stored embeddings to a NumPy array
    embedding_vectors = np.array([chunk["embedding"] for chunk in chunked_data])

    query_embedding = get_embeddings(query, embed_model)

    query_embedding = np.array(query_embedding).reshape(1, -1)
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

    bm25 = BM25Okapi(corpus)

    scores = bm25.get_scores(tokernized_query)

    top_indices = sorted(range(len(scores)), key=(lambda x: scores[x]), reverse=True )[:top_k]
    
    BM25_chunks = [chunked_data[i]  for i in top_indices]
    return BM25_chunks

def similarity_search_model(model,embed_model, query, chuncked_data, top_k):
    if model == "cosine":
        selected_chunks = cosine_retrieved_chunks(query,embed_model, chuncked_data, top_k=3)
    elif model == "BM25":
        selected_chunks = BM25_retrieved_chunks(query, chuncked_data, top_k)
    return selected_chunks

def duplicate_json_file(original_folder, duplicate_folder):
    current_dir = os.path.abspath(os.path.dirname(__file__))  # Ensure absolute path

    original_path = os.path.join(current_dir, original_folder)
    duplicated_path = os.path.join(current_dir, duplicate_folder)

    if os.path.exists(duplicated_path):
        shutil.rmtree(duplicated_path)
    shutil.copytree(original_path, duplicated_path)


def add_retrieved_chunks(duplicate_folder, chunked_data, embed_model,model, top_k):
    """Update the duplicated JSON file with retrieved chunks for each query."""
    current_dir = os.path.abspath(os.path.dirname(__file__))  # Ensure absolute path

    duplicate_folder_path = os.path.join(current_dir, duplicate_folder)

    for filename in os.listdir(duplicate_folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(duplicate_folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for test in data["tests"]:
                query_text = test["query"]

                retrieved_chunks = similarity_search_model(model, embed_model,query_text, chunked_data, top_k )

                retrieved_text = [{f"chunk_id_{chunk['chunk_id']}": chunk["text"]} for i,chunk in enumerate(retrieved_chunks)]

                test["retrieved_chunks"] = retrieved_text

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

if __name__ == "__main__":
    # Load the stored embeddings
    original_folder_ = "testtxtfiles"  # Folder containing JSON files
    duplicate_folder_ = "testtxtfiles_unranked"  # Duplicate folder

    chunked_data = load_chunked_data()

    # Example query
    query_text = "EXCLUSIONS AND EXEMPTIONS"
    model = "cosine"
    embed_model = "sbert"
    top_k = 3

    duplicate_json_file(original_folder_, duplicate_folder_)

    add_retrieved_chunks(duplicate_folder_, chunked_data, embed_model,model, top_k)



