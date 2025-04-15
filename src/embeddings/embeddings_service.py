import json
from textwrap import dedent
from typing import cast

from tqdm import tqdm

from src.infra.chroma_database import chroma_client, model_transformer
from src.infra.configs import logger
from src.models.candidate import CandidateSearch, Candidate, InformacoesProfissionais

BATCH_SIZE = 10


def index_all_applicants(json_path="./data/json/applicants.json"):
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    collection = reset_candidates_collection()

    # Convert the dict to a list of (id, app) pairs
    applicants = [(str(candidate_id), app_data) for candidate_id, app_data in data.items()]
    total = len(applicants)

    logger.info("Starting to index applicants into ChromaDB...")
    logger.info(f"Total applicants to index: {total}")

    if total == 0:
        logger.info("No applicants to index.")
        return

    cont = 0

    for i in tqdm(range(0, total, BATCH_SIZE), desc="Indexing batches"):
        logger.info(f"Indexing batch {i} / {total}")

        batch = applicants[i:i + BATCH_SIZE]

        ids = [candidate_id for candidate_id, _ in batch]
        documents = [_build_embedding_input(app) for _, app in batch]
        metadatas = [
            {
                "codigo_profissional": candidate_id,
                "nome": app.get("infos_basicas", {}).get("nome", ""),
                "email": app.get("infos_basicas", {}).get("email", ""),
                "telefone": app.get("infos_basicas", {}).get("telefone", ""),
                "area_atuacao": app.get("informacoes_profissionais", {}).get("area_atuacao", ""),
            }
            for candidate_id, app in batch
        ]

        try:
            collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            cont += len(batch)
            logger.info(f"✅ Indexed {cont} / {total} applicants")
        except Exception as e:
            logger.error(f"❌ Error indexing batch starting at {i}: {e}")

    logger.info(f"🎉 Done! Indexed {cont} applicants.")



def index_single_applicant(candidate: Candidate):
    try:
        logger.info(
            f"✏️ Indexing candidate {candidate.infos_basicas.codigo_profissional} : '{candidate.infos_basicas.nome}'")

        codigo_profissional = candidate.infos_basicas.codigo_profissional

        ids = [codigo_profissional]
        documents = [_build_embedding_input(candidate)]
        metadatas = [
            {
                "codigo_profissional": codigo_profissional,
                "nome": candidate.infos_basicas.nome,
                "email": candidate.infos_basicas.email,
                "telefone": candidate.infos_basicas.telefone,
                "area_atuacao": candidate.informacoes_profissionais.area_atuacao,
            }
        ]

        collection = chroma_client.get_collection("candidates_collection")
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

        logger.info(
            f"☑️Candidate {candidate.infos_basicas.codigo_profissional} : '{candidate.infos_basicas.nome}' was indexed")

    except Exception as e:
        logger.error(f"❌ Error indexing candidate: {e}")
        raise Exception(f"❌ Error indexing candidate {candidate.infos_basicas.codigo_profissional} : '{candidate.infos_basicas.nome}'")



def reset_candidates_collection():
    try:
        chroma_client.delete_collection("candidates_collection")
    except:
        logger.warning("Collection not found. Will create a new one.")

    return chroma_client.create_collection("candidates_collection")


def _build_embedding_input(candidate):
    if type(candidate) is not dict:
        candidate = cast(Candidate, candidate)
        prof: InformacoesProfissionais = candidate.informacoes_profissionais

        return dedent(f"""
        Portuguese CV: {candidate.cv_pt}
        English CV: {candidate.cv_en}
        Professional Title: {prof.titulo_profissional}
        Certificates: {prof.certificacoes}
        Professional Level: {prof.nivel_profissional}
        """)

    prof = candidate.get("informacoes_profissionais", {})
    return dedent(f"""
    Portuguese CV: {candidate.get("cv_pt", "")}
    English CV: {candidate.get("cv_en", "")}
    Professional Title: {prof.get("titulo_profissional", "")}
    Certificates: {prof.get("certificacoes", "")}
    Professional Level: {prof.get("nivel_profissional", "")}
    """)
