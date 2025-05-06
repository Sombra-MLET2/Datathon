from src.infra.chroma_database import chroma_client, model_transformer
from src.models.candidate import CandidateSearch


def search_candidates(search_request: CandidateSearch):
    collection = chroma_client.get_collection("candidates_collection")
    embedding = model_transformer.encode(search_request.job_description).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=search_request.top_candidates
    )

    scores = results["distances"][0]
    min_score = min(scores)
    max_score = max(scores)

    candidates = []
    for candidate_meta, score in zip(results["metadatas"][0], scores):
        normalized_score = normalize_to_percentage(score, min_score, max_score)

        candidates.append({
            "codigo_profissional": candidate_meta["codigo_profissional"],
            "similarity_score": normalized_score,
        })

    return candidates


def normalize_to_percentage(score, min_score, max_score):
    if max_score == min_score:
        return 100 if score == max_score else 0

    normalized = ((score - min_score) / (max_score - min_score)) * 100
    return round(100 - normalized, 2)
