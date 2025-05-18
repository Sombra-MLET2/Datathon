from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ApplicantBaseDTO(BaseModel):
    nome: str
    email: str
    telefone: Optional[str] = None
    telefone_recado: Optional[str] = None
    objetivo_profissional: Optional[str] = None
    
    class Config:
        from_attributes = True


class ApplicantCreateDTO(ApplicantBaseDTO):
    codigo_profissional: str
    data_nascimento: Optional[str] = None
    nivel_academico: Optional[str] = None
    nivel_ingles: Optional[str] = None
    nivel_espanhol: Optional[str] = None
    remuneracao: Optional[float] = None
    nivel_profissional: Optional[str] = None
    area_atuacao: Optional[str] = None
    conhecimentos_tecnicos: Optional[str] = None


class ApplicantResponseDTO(BaseModel):
    id: int
    codigo_profissional: str
    
    # Infos Básicas
    nome: str
    telefone: Optional[str] = None
    telefone_recado: Optional[str] = None
    objetivo_profissional: Optional[str] = None
    data_criacao: Optional[datetime] = None
    inserido_por: Optional[str] = None
    email: str
    local: Optional[str] = None
    sabendo_de_nos_por: Optional[str] = None
    data_atualizacao: Optional[datetime] = None
    
    # Informações Pessoais
    data_aceite: Optional[datetime] = None
    cpf: Optional[str] = None
    fonte_indicacao: Optional[str] = None
    email_secundario: Optional[str] = None
    data_nascimento: Optional[datetime] = None
    telefone_celular: Optional[str] = None
    sexo: Optional[str] = None
    estado_civil: Optional[str] = None
    pcd: Optional[str] = None
    endereco: Optional[str] = None
    skype: Optional[str] = None
    url_linkedin: Optional[str] = None
    facebook: Optional[str] = None
    
    # Informações Profissionais
    titulo_profissional: Optional[str] = None
    area_atuacao: Optional[str] = None
    conhecimentos_tecnicos: Optional[str] = None
    certificacoes: Optional[str] = None
    outras_certificacoes: Optional[str] = None
    remuneracao: Optional[float] = None
    nivel_profissional: Optional[str] = None
    qualificacoes: Optional[str] = None
    experiencias: Optional[str] = None
    
    # Formação e Idiomas
    nivel_academico: Optional[str] = None
    nivel_ingles: Optional[str] = None
    nivel_espanhol: Optional[str] = None
    outro_idioma: Optional[str] = None
    outro_curso: Optional[str] = None
    
    # Cargo Atual
    id_ibrati: Optional[str] = None
    email_corporativo: Optional[str] = None
    cargo_atual: Optional[str] = None
    projeto_atual: Optional[str] = None
    cliente: Optional[str] = None
    unidade: Optional[str] = None
    data_admissao: Optional[datetime] = None
    data_ultima_promocao: Optional[datetime] = None
    nome_superior_imediato: Optional[str] = None
    email_superior_imediato: Optional[str] = None
    
    # Curriculum
    cv_pt: Optional[str] = None
    cv_en: Optional[str] = None
    
    class Config:
        from_attributes = True


class ApplicantListResponseDTO(BaseModel):
    items: List[ApplicantResponseDTO]
    total: int
    page: int
    page_size: int
    total_pages: int
