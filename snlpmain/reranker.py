from sentence_transformers import CrossEncoder
from similarity_search import find_most_similar_chunks
import json

cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def load_most_similar(json_file="most_similar(cosine).json"):
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)

def CrossEncoder_reranker(query, top_chunks):
    query_chunk_pairs = [ (query, chunk["text"]) for chunk in top_chunks]

    scores = cross_encoder.predict(query_chunk_pairs)


    for i, chunk in enumerate(top_chunks):
        chunk["cross_encoder_score"] = scores[i].item()

    
    ranked_chunks = sorted(top_chunks, key=(lambda x: x["cross_encoder_score"]), reverse=True)

    return ranked_chunks

def save_reranked_chunks(ranked_chunks, output_file="reranked_chunks.json"):
    """Save the re-ranked chunks to a JSON file."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(ranked_chunks, f, indent=2)

    print(f"Re-ranked chunks saved to {output_file}")

if __name__ == "__main__":
    # Load the most similar results
    sim_search_cosine_chunks = load_most_similar()

    query = "Hello what is you name?"
    ranked_chunks = CrossEncoder_reranker(query,sim_search_cosine_chunks)


    save_reranked_chunks(ranked_chunks)


    for j, chunks in enumerate(ranked_chunks):
        print(f"Re-Ranked {j+1}: Score {chunks['cross_encoder_score']:.4f}\n{chunks['text']}\n")
        
        # Example: Print the top results
    for i, chunk in enumerate(sim_search_cosine_chunks):
        print(f"Loaded Top {i+1} Similar Chunk:\n{chunk['text']}\n")

