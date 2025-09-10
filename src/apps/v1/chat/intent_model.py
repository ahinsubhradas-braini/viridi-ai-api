# Import python core libary dependices
import numpy as np

# Imports from project or 3rd party libary dependices
from sentence_transformers import SentenceTransformer

def cosine_similarity(vec1, vec2):
    """
    vec1: shape (1, 384)
    vec2: shape (N, 384) -> multiple phrases
    Returns: (1, N) similarity scores
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    # Normalize both
    vec1_norm = vec1 / np.linalg.norm(vec1, axis=1, keepdims=True)
    vec2_norm = vec2 / np.linalg.norm(vec2, axis=1, keepdims=True)
    
    return np.dot(vec1_norm, vec2_norm.T)


def predict_intent(user_query: str, threshold: float = 0.5):
    model_name = "all-MiniLM-L6-v2"
    model = SentenceTransformer(model_name)

    intent_phrases = {
        "greetings": ["hi", "hello", "hey", "good morning", "good evening"],
        "in_domain": [
            "invoice",
            "product",
            "vat",
            "unspsc",
            "accounting",
            "purchase order",
            "post orders",
            "pricing",
            "cost",
            "suppliers",
            "vendors",
            "billing",
        ],
        "out_of_domain": [
            "weather",
            "sports",
            "news",
            "music",
            "movies",
            "travel",
            "sports",
            "politics",
            "economy",
            "health",
            "technology",
        ],
    }
    intent_embeddings = {
        intent: model.encode(phrases, convert_to_numpy=True)
        for intent, phrases in intent_phrases.items()
    }
    query_vec = model.encode([user_query], convert_to_numpy=True)
    best_intent = "out_of_domain"
    best_score = 0.0

    for intent, vectors in intent_embeddings.items():
        scores = cosine_similarity(query_vec, vectors)  # Shape (1, n_phrases)
        print(f"Intent: {intent}, Scores: {scores}")
        max_score = float(np.max(scores))
        print(f"Intent: {intent}, Max Score: {max_score}")
        
        if max_score > best_score:
            best_score = max_score
            best_intent = intent

    if best_score < threshold:
        best_intent = "out_of_domain"

    return {"intent": best_intent, "score": float(best_score)}
