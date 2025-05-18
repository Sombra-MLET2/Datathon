from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class JobVacancyBaseDTO(BaseModel):
    titulo_vaga: str
    cliente: Optional[str] = None
    tipo_contratacao: Optional[str] = None
    
    class Config:
        from_attributes = True


class JobVacancyCreateDTO(JobVacancyBaseDTO):
    vaga_id: str
    data_requicisao: Optional[str] = None
    empresa_divisao: Optional[str] = None
    nivel_profissional: Optional[str] = None
    nivel_academico: Optional[str] = None
    nivel_ingles: Optional[str] = None
    nivel_espanhol: Optional[str] = None
    pais: Optional[str] = None
    estado: Optional[str] = None
    cidade: Optional[str] = None


class JobVacancyResponseDTO(BaseModel):
    id: int
    vaga_id: str
    
    # Informações Básicas
    data_requicisao: Optional[datetime] = None
    limite_esperado_para_contratacao: Optional[datetime] = None
    titulo_vaga: str
    vaga_sap: Optional[str] = None
    cliente: Optional[str] = None
    solicitante_cliente: Optional[str] = None
    empresa_divisao: Optional[str] = None
    requisitante: Optional[str] = None
    analista_responsavel: Optional[str] = None
    tipo_contratacao: Optional[str] = None
    prazo_contratacao: Optional[str] = None
    objetivo_vaga: Optional[str] = None
    prioridade_vaga: Optional[str] = None
    origem_vaga: Optional[str] = None
    superior_imediato: Optional[str] = None
    superior_nome: Optional[str] = None
    superior_telefone: Optional[str] = None
    
    # Perfil da Vaga
    pais: Optional[str] = None
    estado: Optional[str] = None
    cidade: Optional[str] = None
    bairro: Optional[str] = None
    regiao: Optional[str] = None
    local_trabalho: Optional[str] = None
    vaga_especifica_para_pcd: Optional[str] = None
    faixa_etaria: Optional[str] = None
    horario_trabalho: Optional[str] = None
    nivel_profissional: Optional[str] = None
    nivel_academico: Optional[str] = None
    nivel_ingles: Optional[str] = None
    nivel_espanhol: Optional[str] = None
    outro_idioma: Optional[str] = None
    areas_atuacao: Optional[str] = None
    principais_atividades: Optional[str] = None
    competencia_tecnicas_e_comportamentais: Optional[str] = None
    demais_observacoes: Optional[str] = None
    viagens_requeridas: Optional[str] = None
    equipamentos_necessarios: Optional[str] = None
    
    # Benefícios
    valor_venda: Optional[str] = None
    valor_compra_1: Optional[str] = None
    valor_compra_2: Optional[str] = None
    
    class Config:
        from_attributes = True


class JobVacancyListResponseDTO(BaseModel):
    items: List[JobVacancyResponseDTO]
    total: int
    page: int
    page_size: int
    total_pages: int
