import os 
import json
from sentence_transformers import SentenceTransformer
import numpy as np
import re
# import openai

# Load model
# model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

supported_models = {
    "sbert": "sentence-transformers/all-mpnet-base-v2",
    "distilled_sbert": "sentence-transformers/all-MiniLM-L6-v2",
    "gte_large": "thenlper/gte-large",
    "openai": "text-embedding-3-large"  
}

def load_embedding_model(model_name):
    if model_name in ["sbert", "distilled_sbert", "gte_large"]:
        return SentenceTransformer(supported_models[model_name])
    elif model_name == "openai":
        return None
    else:
        raise ValueError(f"Model '{model_name} not supported")
    

def naive_chunking(text, chunk_size, overlap):
    "Function to chunk the text"
    start = 0
    chunks = []
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def get_embeddings(chunks, model_name):
    if model_name in ["sbert", "distilled_sbert", "gte_large"]:
        model = load_embedding_model(model_name)
        return model.encode(chunks, convet_to_numpy=True)
    
    # elif model_name == "openai":
    #     # Use OpenAI API for embeddings
    #     openai.api_key = "your_openai_api_key"  # Replace with your actual API key
    #     response = openai.Embedding.create(input=chunks, model="text-embedding-3-large")
    #     return np.array([data["embedding"] for data in response["data"]])

    else:
        raise ValueError(f"Model '{model_name}' not supported.")
    

# def embed_chunks(chunks):
#     embeddings = model.encode(chunks, convert_to_numpy=True)
#     return embeddings

def save_chunks_to_txt(chunks, file_name,output_folder_json ):
    """
    Save chunked text to a specific folder.

    :param chunks: List of chunked text.
    :param file_name: Name of the output file (without extension).
    :param output_folder: Directory where files will be saved.
    """

    # Ensure the output folder exists
    # os.makedirs(output_folder_txt, exist_ok=True)  # Creates folder if it doesn’t exist
    os.makedirs(output_folder_json, exist_ok=True)  # Creates folder if it doesn’t exist

    # Define full file paths
    # text_file_path = os.path.join(output_folder_txt, f"{file_name}.txt")
    json_file_path = os.path.join(output_folder_json, f"{file_name}.json")

    # Save text file
    # with open(text_file_path, "w", encoding="utf-8") as f:
    #     for i, chunk in enumerate(chunks):
    #         f.write(f"Chunk {i+1}:\n")
    #         f.write(chunk + "\n\n")
    # print(f"Chunks saved in txt format: {text_file_path}")

    # Save JSON file
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    # print(f"Chunks saved in JSON format: {json_file_path}")


def process_text_file(chunk_size, overlap):

    current_dir = os.path.abspath(os.path.dirname(__file__))  # Ensure absolute path

    folder_path = os.path.join(current_dir, "testtxtfiles")

    text_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]


    chunk_data = []  # Initialize chunk_data before the loop

    for filename in text_files:
        file_path = f'{folder_path}/{filename}'

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        chunks = naive_chunking(text, chunk_size, overlap)


        embeddings = get_embeddings(chunks, model_name="sbert")
        chunk_data = [{"chunk_id": i, "text": chunk, "embedding": embedding.tolist()} 
                    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))]
        
        name = filename.removesuffix(".txt")
        save_chunks_to_txt(chunk_data, name, 'chunkedtxt', 'chunked_data')
    return chunk_data


# Run this only if executing this file directly
if __name__ == "__main__":
    chunked_data = process_text_file(chunk_size=600, overlap=50)

    # # Save chunked data for later use in similarity search
    # with open("chunked_embeddings.json", "w") as f:
    #     json.dump(chunked_data, f, indent=2)

    # print(f"Chunking and embedding completed. Data saved to chunked_embeddings.json")

        # Check for duplicate text chunks
    # unique_chunks = set()
    # duplicates = []

    # for chunk in chunked_data:
    #     text = chunk['text']
    #     if text in unique_chunks:
    #         duplicates.append(text)
    #     else:
    #         unique_chunks.add(text)

    # print(f"Found {len(duplicates)} duplicate chunks")
    # for d in duplicates[:5]:  # Print only first 5 to check
    #     print(d)

