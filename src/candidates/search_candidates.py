from src.infra.chroma_database import chroma_client, model_transformer
from src.models.candidate import CandidateSearch


def search_candidates(search_request: CandidateSearch):
    collection = chroma_client.get_collection("candidates_collection")
    embedding = model_transformer.encode(search_request.job_description).tolist()

    results = collection.query(query_embeddings=[embedding], n_results=search_request.top_candidates)

    hits = []
    for doc, meta, id_ in zip(results["documents"][0], results["metadatas"][0], results["ids"][0]):
        hits.append({
            "id": id_,
            "score": None,
            "document": doc,
            "candidate": meta
        })

    return hits