import joblib
import pandas as pd
import scipy
import unicodedata

from src.infra.configs import logger, ML_MODEL_NAME
from src.models.job_vacancy import JobVacancy
from src.models.applicant import Applicant


vectorizers = joblib.load("./Model/RandomForest/vectorizers.gz")
scaler = joblib.load("./Model/RandomForest/standard_scaler.gz")
label_encoders = joblib.load("./Model/RandomForest/label_encoders.gz")

ml_model = None
if ML_MODEL_NAME == "RandomForest":
    ml_model = joblib.load("./Model/RandomForest/model.gz")
elif ML_MODEL_NAME == "XGBoost":
    ml_model = joblib.load("./Model/XGBoost/model.gz")
else:
    raise ValueError("Modelo de ML não reconhecido!")

nivel_map = {
    'nenhum': 0,
    'basico': 1,
    'intermediario': 2,
    'avancado': 3,
    'fluente': 4
}

situacao_map = {
    "candidatura em andamento": [
        "inscrito",
        "prospect",
        "em avaliacao pelo rh",
        "entrevista tecnica",
        "entrevista com cliente",
        "encaminhado ao requisitante",
        "encaminhar proposta",
        "documentacao pj",
        "documentacao clt",
        "documentacao cooperado"
    ],
    "contratacao confirmada": [
        "aprovado",
        "proposta aceita",
        "contratado pela decision",
        "contratado como hunting"
    ],
    "recusado": [
        "nao aprovado pelo rh",
        "nao aprovado pelo requisitante",
        "nao aprovado pelo cliente"
    ],
    "desistencia": [
        "desistiu",
        "desistiu da contratacao",
        "recusado",
        "sem interesse nesta vaga"
    ]
}


def infer_offer_from_candidate(vacancy: JobVacancy, applicant: Applicant):
    logger.info("Starting inference process")
    
    if ml_model is None:
        logger.error("ML model not loaded")
        raise Exception("ML model not loaded")

    try:
        logger.info("Mapping DTO to DataFrame")
        df = map_dto_to_df(vacancy, applicant)
        logger.info("DataFrame mapped")

        logger.info("Pre-processing DataFrame")
        df = pre_process(df)
        logger.info("DataFrame pre-processed")

        logger.info("Applying feature transformation")
        X_model_input = apply_feature_transformation(df)
        logger.info("Feature transformation applied")

        logger.info("Getting probability of acceptance")
        acceptance_prob = get_acceptance_prob(X_model_input)
        logger.info("Probability obtained")

    except Exception as e:
        logger.error(f"Error during inference: {e}")
        raise Exception("Error during inference")
    
    logger.info("Inference completed successfully")

    return {"acceptance_probability": acceptance_prob}


def map_dto_to_df(vacancy: JobVacancy, applicant: Applicant) -> pd.DataFrame:
    applicant_data = {
        'area_atuacao': applicant.area_atuacao,
        'certificacoes': applicant.certificacoes,
        'conhecimentos_tecnicos': applicant.conhecimentos_tecnicos,
        'cv_pt': applicant.cv_pt,
        'nivel_academico': applicant.nivel_academico,
        'nivel_espanhol': applicant.nivel_espanhol,
        'nivel_ingles': applicant.nivel_ingles,
        'outras_certificacoes': applicant.outras_certificacoes,
        'outro_idioma': applicant.outro_idioma,
        'pcd': applicant.pcd,
        'titulo_profissional': applicant.titulo_profissional
    }

    vacancy_data = {
        'areas_atuacao': vacancy.areas_atuacao,
        'demais_observacoes': vacancy.demais_observacoes,
        'nivel_academico_vaga': vacancy.nivel_academico,
        'nivel_espanhol_vaga': vacancy.nivel_espanhol,
        'nivel_ingles_vaga': vacancy.nivel_ingles,
        'nivel_profissional': vacancy.nivel_profissional,
        'outro_idioma_vaga': vacancy.outro_idioma,
        'principais_atividades': vacancy.principais_atividades,
        'vaga_especifica_para_pcd': vacancy.vaga_especifica_para_pcd,
        'viagens_requeridas': vacancy.viagens_requeridas
    }

    applicant_and_vacancy_data = {**applicant_data, **vacancy_data}
    df = pd.DataFrame([applicant_and_vacancy_data])

    return df


def pre_process(df: pd.DataFrame) -> pd.DataFrame:
    df = df.apply(lambda col: col.map(string_normalizer) if col.dtype == 'object' else col)
    df.replace('-', None, inplace=True)

    df['pcd'] = df['pcd'].apply(lambda x: 1 if x == 'sim' else 0)
    df['vaga_especifica_para_pcd'] = df['vaga_especifica_para_pcd'].apply(lambda x: 1 if x == 'sim' else 0)
    df['pcd_match'] = ((df['pcd'] == 1) & (df['vaga_especifica_para_pcd'] == 1)).astype(int)

    df['viagens_requeridas'] = df['viagens_requeridas'].apply(lambda x: 1 if x == 'sim' else 0)

    df['nivel_ingles'] = df['nivel_ingles'].map(nivel_map).fillna(0)
    df['nivel_ingles_vaga'] = df['nivel_ingles_vaga'].map(nivel_map).fillna(0)
    df['ingles'] = (df['nivel_ingles'] >= df['nivel_ingles_vaga']).astype(int)

    df['nivel_espanhol'] = df['nivel_ingles'].map(nivel_map).fillna(0)
    df['nivel_espanhol_vaga'] = df['nivel_ingles_vaga'].map(nivel_map).fillna(0)
    df['espanhol'] = (df['nivel_espanhol'] >= df['nivel_espanhol_vaga']).astype(int)

    df.fillna("", inplace=True)

    candidato_cols = ['titulo_profissional', 'area_atuacao', 'conhecimentos_tecnicos',
                      'certificacoes', 'outras_certificacoes', 'nivel_academico', 'outro_idioma', 'cv_pt']
    df['candidato'] = df[candidato_cols].agg(' '.join, axis=1)

    vaga_cols = ['nivel_profissional', 'nivel_academico_vaga', 'outro_idioma_vaga',
                 'areas_atuacao', 'principais_atividades', 'demais_observacoes']
    df['vaga'] = df[vaga_cols].agg(' '.join, axis=1)

    _df = df[['candidato', 'vaga', 'viagens_requeridas', 'pcd_match', 'ingles', 'espanhol']]

    _df.rename(columns={
        'situacao_candidado': 'situacao',
        'comentario': 'comentario',
        'viagens_requeridas': 'vaga_viagens_requeridas',
        'pcd_match': 'pcd',
        'ingles': 'nivel_ingles',
        'espanhol': 'nivel_espanhol'
    }, inplace=True)

    return _df


def apply_feature_transformation(df: pd.DataFrame) -> scipy.sparse.csr_matrix:
    vt_candidato = vectorizers["candidato"].transform(df['candidato'])
    vt_vaga = vectorizers["vaga"].transform(df['vaga'])
    #vt_comentario = vectorizers["comentario"].transform(df['comentario'])

    num_data = df[['vaga_viagens_requeridas', 'pcd', 'nivel_ingles', 'nivel_espanhol']]
    num_scaled = scaler.transform(num_data)

    X_model_input = scipy.sparse.hstack([num_scaled, vt_candidato, vt_vaga]) # vt_comentario

    return X_model_input


def get_acceptance_prob(X: scipy.sparse.spmatrix) -> float:
    proba = ml_model.predict_proba(X)[0]

    situacao_classes = label_encoders["situacao"].classes_
    acceptance_idx = list(situacao_classes).index("contratacao confirmada")

    acceptance_prob = float(proba[acceptance_idx])
    
    return acceptance_prob
    

def string_normalizer(text):
    if text is None or text == "":
        return None
    else:
        return ''.join(c for c in unicodedata.normalize('NFD', text) if not unicodedata.combining(c)).lower()


def status_map(text):
    for grupo, status_list in situacao_map.items():
        if text in status_list:
            return grupo
    return None
