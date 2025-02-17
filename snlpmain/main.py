import os 
import json
from sentence_transformers import SentenceTransformer
import numpy as np
import re

# Load model
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

def naive_chunking(text, chunk_size, overlap):
    "Function to chunk the text"
    start = 0
    chunks = []
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# def smart_chunking(text, chunk_size, overlap):
#     words = re.split(r'(\s+)', text)  # Splitting text into words while keeping spaces
#     chunks = []
#     current_chunk = ""
    
#     for word in words:
#         if len(current_chunk) + len(word) <= chunk_size:
#             current_chunk += word
#         else:
#             chunks.append(current_chunk.strip())
#             current_chunk = word  # Start a new chunk with the current word

#     if current_chunk:  # Append any remaining text
#         chunks.append(current_chunk.strip())

    return chunks

def embed_chunks(chunks):
    embeddings = model.encode(chunks, convert_to_numpy=True)
    return embeddings



def save_chunks_to_txt(chunks, file_name, output_folder_txt,output_folder_json ):
    """
    Save chunked text to a specific folder.

    :param chunks: List of chunked text.
    :param file_name: Name of the output file (without extension).
    :param output_folder: Directory where files will be saved.
    """

    # Ensure the output folder exists
    os.makedirs(output_folder_txt, exist_ok=True)  # Creates folder if it doesn’t exist
    os.makedirs(output_folder_json, exist_ok=True)  # Creates folder if it doesn’t exist

    # Define full file paths
    text_file_path = os.path.join(output_folder_txt, f"{file_name}.txt")
    json_file_path = os.path.join(output_folder_json, f"{file_name}.json")

    # Save text file
    with open(text_file_path, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"Chunk {i+1}:\n")
            f.write(chunk + "\n\n")
    print(f"Chunks saved in txt format: {text_file_path}")

    # Save JSON file
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print(f"Chunks saved in JSON format: {json_file_path}")


def process_text_file(chunk_size, overlap):
    # function to load all the files from a folder which are txt files.
    # folder_path =  '/Users/raymonfernandes/Desktop/Dion_work/snlp_project_code/snlpmain/testtxtfiles'

    current_dir = os.path.abspath(os.path.dirname(__file__))  # Ensure absolute path

    folder_path = os.path.join(current_dir, "testtxtfiles")

    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]



    chunk_data = []  # Initialize chunk_data before the loop

    for filename in txt_files:
        file_path = f'folder_path/{filename}'

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        chunks = naive_chunking(text, chunk_size, overlap)
        # chunks = smart_chunking(text, chunk_size, overlap)

        
        embeddings = embed_chunks(chunks)

        chunk_data = [{"chunk_id": i, "text": chunk, "embedding": embedding.tolist()} 
                    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))]
        name = filename.removesuffix(".txt")
        save_chunks_to_txt(chunks, name, 'chunkedtxt', 'chunkedjson')
    return chunk_data


chunked_data = process_text_file(chunk_size=600, overlap=50)


