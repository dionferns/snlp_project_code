import json

def load_most_similar(json_file="most_similar(cosine).json"):
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load()









if __name__ == "__main__":
    # Load the most similar results
    most_similar_chunks = load_most_similar()

    # Example: Print the top results
    for i, chunk in enumerate(most_similar_chunks):
        print(f"Loaded Top {i+1} Similar Chunk:\n{chunk['text']}\n")