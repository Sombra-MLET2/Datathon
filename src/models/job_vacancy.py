from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from src.infra.database import Base


class JobVacancy(Base):
    __tablename__ = "job_vacancies"

    id = Column(Integer, primary_key=True, index=True)
    vaga_id = Column(String, unique=True, index=True)
    
    # Informações Básicas
    data_requicisao = Column(DateTime, nullable=True)
    limite_esperado_para_contratacao = Column(DateTime, nullable=True)
    titulo_vaga = Column(String)
    vaga_sap = Column(String)
    cliente = Column(String)
    solicitante_cliente = Column(String)
    empresa_divisao = Column(String)
    requisitante = Column(String)
    analista_responsavel = Column(String)
    tipo_contratacao = Column(String)
    prazo_contratacao = Column(String)
    objetivo_vaga = Column(Text)
    prioridade_vaga = Column(String)
    origem_vaga = Column(String)
    superior_imediato = Column(String)
    superior_nome = Column(String)
    superior_telefone = Column(String)
    
    # Perfil da Vaga
    pais = Column(String)
    estado = Column(String)
    cidade = Column(String)
    bairro = Column(String)
    regiao = Column(String)
    local_trabalho = Column(String)
    vaga_especifica_para_pcd = Column(String)
    faixa_etaria = Column(String)
    horario_trabalho = Column(String)
    nivel_profissional = Column(String)
    nivel_academico = Column(String)
    nivel_ingles = Column(String)
    nivel_espanhol = Column(String)
    outro_idioma = Column(String)
    areas_atuacao = Column(String)
    principais_atividades = Column(Text)
    competencia_tecnicas_e_comportamentais = Column(Text)
    demais_observacoes = Column(Text)
    viagens_requeridas = Column(String)
    equipamentos_necessarios = Column(String)
    
    # Benefícios
    valor_venda = Column(String)
    valor_compra_1 = Column(String)
    valor_compra_2 = Column(String)
    
    def __init__(self, vacancy_data, vaga_id):
        """
        Initialize a JobVacancy from a dictionary containing vacancy data
        """
        self.vaga_id = vaga_id
        
        # Informações Básicas
        info_basicas = vacancy_data.get("informacoes_basicas", {})
        self.titulo_vaga = info_basicas.get("titulo_vaga", "")
        self.vaga_sap = info_basicas.get("vaga_sap", "")
        self.cliente = info_basicas.get("cliente", "")
        self.solicitante_cliente = info_basicas.get("solicitante_cliente", "")
        self.empresa_divisao = info_basicas.get("empresa_divisao", "")
        self.requisitante = info_basicas.get("requisitante", "")
        self.analista_responsavel = info_basicas.get("analista_responsavel", "")
        self.tipo_contratacao = info_basicas.get("tipo_contratacao", "")
        self.prazo_contratacao = info_basicas.get("prazo_contratacao", "")
        self.objetivo_vaga = info_basicas.get("objetivo_vaga", "")
        self.prioridade_vaga = info_basicas.get("prioridade_vaga", "")
        self.origem_vaga = info_basicas.get("origem_vaga", "")
        self.superior_imediato = info_basicas.get("superior_imediato", "")
        self.superior_nome = info_basicas.get("nome", "")
        self.superior_telefone = info_basicas.get("telefone", "")
        
        # Parse dates
        try:
            self.data_requicisao = datetime.strptime(info_basicas.get("data_requicisao", ""), "%d-%m-%Y")
        except (ValueError, TypeError):
            self.data_requicisao = None
            
        try:
            limite_data = info_basicas.get("limite_esperado_para_contratacao", "")
            if limite_data and limite_data != "00-00-0000":
                self.limite_esperado_para_contratacao = datetime.strptime(limite_data, "%d-%m-%Y")
            else:
                self.limite_esperado_para_contratacao = None
        except (ValueError, TypeError):
            self.limite_esperado_para_contratacao = None
        
        # Perfil da Vaga
        perfil = vacancy_data.get("perfil_vaga", {})
        self.pais = perfil.get("pais", "")
        self.estado = perfil.get("estado", "")
        self.cidade = perfil.get("cidade", "")
        self.bairro = perfil.get("bairro", "")
        self.regiao = perfil.get("regiao", "")
        self.local_trabalho = perfil.get("local_trabalho", "")
        self.vaga_especifica_para_pcd = perfil.get("vaga_especifica_para_pcd", "")
        self.faixa_etaria = perfil.get("faixa_etaria", "")
        self.horario_trabalho = perfil.get("horario_trabalho", "")
        self.nivel_profissional = perfil.get("nivel profissional", "")  # Note the space in the key
        self.nivel_academico = perfil.get("nivel_academico", "")
        self.nivel_ingles = perfil.get("nivel_ingles", "")
        self.nivel_espanhol = perfil.get("nivel_espanhol", "")
        self.outro_idioma = perfil.get("outro_idioma", "")
        self.areas_atuacao = perfil.get("areas_atuacao", "")
        self.principais_atividades = perfil.get("principais_atividades", "")
        self.competencia_tecnicas_e_comportamentais = perfil.get("competencia_tecnicas_e_comportamentais", "")
        self.demais_observacoes = perfil.get("demais_observacoes", "")
        self.viagens_requeridas = perfil.get("viagens_requeridas", "")
        self.equipamentos_necessarios = perfil.get("equipamentos_necessarios", "")
        
        # Benefícios
        beneficios = vacancy_data.get("beneficios", {})
        self.valor_venda = beneficios.get("valor_venda", "")
        self.valor_compra_1 = beneficios.get("valor_compra_1", "")
        self.valor_compra_2 = beneficios.get("valor_compra_2", "")
