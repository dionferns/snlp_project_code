# from sentence_transformers import CrossEncoder
# from similarity_search import find_most_similar_chunks
# import json
# import os


# cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# def load_most_similar(directory="testtxtfiles_unranked/"):

#     current_dir = os.path.abspath(os.path.dirname(__file__))  # Ensure absolute path
# # mkae sure the chunk id values are the same you got from the part
#     folder_path = os.path.join(current_dir, directory)

#     for filename in os.listdir(folder_path):
#         if filename.startswith(".json"):
#             file_path = os.path.join(folder_path, filename)

#         with open(file_path, "r", encoding="utf-8") as f:
#             data = json.load(f)
#             for test in data["tests"]:
#                 finish this part 

#     with open(folder_path, "r", encoding="utf-8") as f:
#         return json.load(f)

# def CrossEncoder_reranker(query, top_chunks):
#     query_chunk_pairs = [ (query, chunk["text"]) for chunk in top_chunks]

#     scores = cross_encoder.predict(query_chunk_pairs)


#     for i, chunk in enumerate(top_chunks):
#         chunk["cross_encoder_score"] = scores[i].item()

    
#     ranked_chunks = sorted(top_chunks, key=(lambda x: x["cross_encoder_score"]), reverse=True)

#     return ranked_chunks


# def save_reranked_chunks(ranked_chunks, output_file="reranked_chunks.json"):
#     """Save the re-ranked chunks to a JSON file."""
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(ranked_chunks, f, indent=2)

#     print(f"Re-ranked chunks saved to {output_file}")

# if __name__ == "__main__":
#     # Load the most similar results
#     sim_search_cosine_chunks = load_most_similar()

#     query = "Hello what is you name?"
#     ranked_chunks = CrossEncoder_reranker(query,sim_search_cosine_chunks)


#     save_reranked_chunks(ranked_chunks)


#     for j, chunks in enumerate(ranked_chunks):
#         print(f"Re-Ranked {j+1}: Score {chunks['cross_encoder_score']:.4f}\n{chunks['text']}\n")
        
#         # Example: Print the top results
#     for i, chunk in enumerate(sim_search_cosine_chunks):
#         print(f"Loaded Top {i+1} Similar Chunk:\n{chunk['text']}\n")

# from sentence_transformers import CrossEncoder
# import json
# import os

# # Load cross encoder model
# cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# def load_most_similar(directory="testtxtfiles_unranked/"):
#     """Load and re-rank retrieved chunks from JSON files in the folder."""
    
#     current_dir = os.path.abspath(os.path.dirname(__file__))  # Ensure absolute path
#     folder_path = os.path.join(current_dir, directory)

#     for filename in os.listdir(folder_path):
#         if filename.endswith(".json"):  # ✅ Ensure we're reading JSON files
#             file_path = os.path.join(folder_path, filename)

#             with open(file_path, "r", encoding="utf-8") as f:
#                 data = json.load(f)

#             for test in data["tests"]:
#                 query_text = test["query"]

#                 # Extract retrieved chunks along with their chunk_id
#                 retrieved_chunks = [
#                     {"chunk_id": list(chunk.keys())[0], "text": list(chunk.values())[0]}
#                     for chunk in test["retrieved_chunks"]
#                 ]

#                 # Prepare query-chunk pairs for cross-encoder
#                 query_chunk_pairs = [(query_text, chunk["text"]) for chunk in retrieved_chunks]

#                 # Compute cross-encoder scores
#                 scores = cross_encoder.predict(query_chunk_pairs)

#                 # Attach scores and re-rank
#                 for i, chunk in enumerate(retrieved_chunks):
#                     chunk["cross_encoder_score"] = scores[i]

#                 ranked_chunks = sorted(retrieved_chunks, key=lambda x: x["cross_encoder_score"], reverse=True)

#                 # ✅ Store the re-ranked chunks back in the JSON
#                 test["retrieved_chunks_ranked"] = ranked_chunks

#             # ✅ Save the updated JSON file with ranked chunks
#             with open(file_path, "w", encoding="utf-8") as f:
#                 json.dump(data, f, indent=2, ensure_ascii=False)

#     print(f"Processed and re-ranked all JSON files in '{directory}' successfully.")



import shutil
import os
import json
from sentence_transformers import CrossEncoder

# Load cross encoder model
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def duplicate_folder(original_folder="testtxtfiles_unranked", duplicate_folder="testtxtfiles_ranked"):
    """Create a duplicate of the original folder before re-ranking."""
    current_dir = os.path.abspath(os.path.dirname(__file__))  # Ensure absolute path
    original_path = os.path.join(current_dir, original_folder)
    duplicate_path = os.path.join(current_dir, duplicate_folder)

    if os.path.exists(duplicate_path):
        shutil.rmtree(duplicate_path)  # Remove if already exists
    shutil.copytree(original_path, duplicate_path)  # Copy contents
    print(f" Folder '{original_folder}' duplicated to '{duplicate_folder}'.")

def load_most_similar(directory="testtxtfiles_unranked/"):
    """Load and re-rank retrieved chunks from JSON files in the folder."""
    
    current_dir = os.path.abspath(os.path.dirname(__file__))  # Ensure absolute path
    folder_path = os.path.join(current_dir, directory)

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):  #  Ensure we're reading JSON files
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for test in data["tests"]:
                query_text = test["query"]

                # Extract retrieved chunks along with their chunk_id
                retrieved_chunks = [
                    {"chunk_id": list(chunk.keys())[0], "text": list(chunk.values())[0]}
                    for chunk in test["retrieved_chunks"]
                ]

                # Prepare query-chunk pairs for cross-encoder
                query_chunk_pairs = [(query_text, chunk["text"]) for chunk in retrieved_chunks]

                # Compute cross-encoder scores
                scores = cross_encoder.predict(query_chunk_pairs)

                # Attach scores and re-rank
                for i, chunk in enumerate(retrieved_chunks):
                    chunk["cross_encoder_score"] = float(scores[i])

                ranked_chunks = sorted(retrieved_chunks, key=lambda x: x["cross_encoder_score"], reverse=True)

                #  Store both original and re-ranked chunks
                test["retrieved_chunks_unranked"] = retrieved_chunks
                test["retrieved_chunks_ranked"] = ranked_chunks

            #  Save the updated JSON file with ranked chunks
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    print(f" Processed and re-ranked all JSON files in '{directory}' successfully.")

# Run duplication and re-ranking
if __name__ == "__main__":
    duplicate_folder()  # Step 1: Duplicate 'testtxtfiles' to 'testtxtfiles_unranked'
    load_most_similar()  # Step 2: Load and re-rank retrieved chunks
