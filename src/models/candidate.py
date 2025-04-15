from typing import Optional, Dict

from pydantic import BaseModel


class CandidateSearch(BaseModel):
    top_candidates: int = 5
    job_description: str


class InfosBasicas(BaseModel):
    telefone_recado: Optional[str] = None
    telefone: Optional[str] = None
    objetivo_profissional: Optional[str] = None
    data_criacao: Optional[str] = None
    inserido_por: Optional[str] = None
    email: str
    local: Optional[str] = None
    sabendo_de_nos_por: Optional[str] = None
    data_atualizacao: Optional[str] = None
    codigo_profissional: str
    nome: str


class InformacoesPessoais(BaseModel):
    data_aceite: Optional[str] = None
    nome: str
    cpf: Optional[str] = None
    fonte_indicacao: Optional[str] = None
    email: str
    email_secundario: Optional[str] = None
    data_nascimento: Optional[str] = None
    telefone_celular: Optional[str] = None
    telefone_recado: Optional[str] = None
    sexo: Optional[str] = None
    estado_civil: Optional[str] = None
    pcd: Optional[str] = None
    endereco: Optional[str] = None
    skype: Optional[str] = None
    url_linkedin: Optional[str] = None
    facebook: Optional[str] = None


class InformacoesProfissionais(BaseModel):
    titulo_profissional: Optional[str] = None
    area_atuacao: Optional[str] = None
    conhecimentos_tecnicos: Optional[str] = None
    certificacoes: Optional[str] = None
    outras_certificacoes: Optional[str] = None
    remuneracao: Optional[str] = None
    nivel_profissional: Optional[str] = None


class FormacaoEIdiomas(BaseModel):
    nivel_academico: Optional[str] = None
    nivel_ingles: Optional[str] = None
    nivel_espanhol: Optional[str] = None
    outro_idioma: Optional[str] = None


class Candidate(BaseModel):
    infos_basicas: InfosBasicas
    informacoes_pessoais: InformacoesPessoais
    informacoes_profissionais: Optional[InformacoesProfissionais] = None
    formacao_e_idiomas: Optional[FormacaoEIdiomas] = None
    cargo_atual: Optional[Dict] = None
    cv_pt: Optional[str] = None
    cv_en: Optional[str] = None
