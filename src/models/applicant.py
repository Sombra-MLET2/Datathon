from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Float

from src.infra.database import Base


class Applicant(Base):
    __tablename__ = "applicants"

    id = Column(Integer, primary_key=True, index=True)
    codigo_profissional = Column(String, unique=True, index=True)
    
    # Infos Básicas
    nome = Column(String)
    telefone = Column(String)
    telefone_recado = Column(String)
    objetivo_profissional = Column(String)
    data_criacao = Column(DateTime)
    inserido_por = Column(String)
    email = Column(String)
    local = Column(String)
    sabendo_de_nos_por = Column(String)
    data_atualizacao = Column(DateTime)
    
    # Informações Pessoais
    data_aceite = Column(DateTime, nullable=True)
    cpf = Column(String)
    fonte_indicacao = Column(String)
    email_secundario = Column(String)
    data_nascimento = Column(DateTime, nullable=True)
    telefone_celular = Column(String)
    sexo = Column(String)
    estado_civil = Column(String)
    pcd = Column(String)
    endereco = Column(String)
    skype = Column(String)
    url_linkedin = Column(String)
    facebook = Column(String)
    
    # Informações Profissionais
    titulo_profissional = Column(String)
    area_atuacao = Column(String)
    conhecimentos_tecnicos = Column(Text)
    certificacoes = Column(Text)
    outras_certificacoes = Column(Text)
    remuneracao = Column(Float, nullable=True)
    nivel_profissional = Column(String)
    qualificacoes = Column(Text)
    experiencias = Column(Text)
    
    # Formação e Idiomas
    nivel_academico = Column(String)
    nivel_ingles = Column(String)
    nivel_espanhol = Column(String)
    outro_idioma = Column(String)
    outro_curso = Column(String)
    
    # Cargo Atual
    id_ibrati = Column(String)
    email_corporativo = Column(String)
    cargo_atual = Column(String)
    projeto_atual = Column(String)
    cliente = Column(String)
    unidade = Column(String)
    data_admissao = Column(DateTime, nullable=True)
    data_ultima_promocao = Column(DateTime, nullable=True)
    nome_superior_imediato = Column(String)
    email_superior_imediato = Column(String)
    
    # Curriculum
    cv_pt = Column(Text)
    cv_en = Column(Text)
    
    def __init__(self, applicant_data):

        self.codigo_profissional = applicant_data.get("infos_basicas", {}).get("codigo_profissional", "")
        
        # Infos Básicas
        infos_basicas = applicant_data.get("infos_basicas", {})
        self.nome = infos_basicas.get("nome", "")
        self.telefone = infos_basicas.get("telefone", "")
        self.telefone_recado = infos_basicas.get("telefone_recado", "")
        self.objetivo_profissional = infos_basicas.get("objetivo_profissional", "")
        self.inserido_por = infos_basicas.get("inserido_por", "")
        self.email = infos_basicas.get("email", "")
        self.local = infos_basicas.get("local", "")
        self.sabendo_de_nos_por = infos_basicas.get("sabendo_de_nos_por", "")
        
        try:
            self.data_criacao = datetime.strptime(infos_basicas.get("data_criacao", ""), "%d-%m-%Y %H:%M:%S")
        except (ValueError, TypeError):
            self.data_criacao = None
            
        try:
            self.data_atualizacao = datetime.strptime(infos_basicas.get("data_atualizacao", ""), "%d-%m-%Y %H:%M:%S")
        except (ValueError, TypeError):
            self.data_atualizacao = None
        
        # Informações Pessoais
        info_pessoais = applicant_data.get("informacoes_pessoais", {})
        self.cpf = info_pessoais.get("cpf", "")
        self.fonte_indicacao = info_pessoais.get("fonte_indicacao", "")
        self.email_secundario = info_pessoais.get("email_secundario", "")
        self.telefone_celular = info_pessoais.get("telefone_celular", "")
        self.sexo = info_pessoais.get("sexo", "")
        self.estado_civil = info_pessoais.get("estado_civil", "")
        self.pcd = info_pessoais.get("pcd", "")
        self.endereco = info_pessoais.get("endereco", "")
        self.skype = info_pessoais.get("skype", "")
        self.url_linkedin = info_pessoais.get("url_linkedin", "")
        self.facebook = info_pessoais.get("facebook", "")
        
        try:
            self.data_aceite = datetime.strptime(info_pessoais.get("data_aceite", ""), "%d/%m/%Y %H:%M")
        except (ValueError, TypeError):
            self.data_aceite = None
            
        try:
            self.data_nascimento = datetime.strptime(info_pessoais.get("data_nascimento", ""), "%d-%m-%Y")
        except (ValueError, TypeError):
            self.data_nascimento = None
        
        info_prof = applicant_data.get("informacoes_profissionais", {})
        self.titulo_profissional = info_prof.get("titulo_profissional", "")
        self.area_atuacao = info_prof.get("area_atuacao", "")
        self.conhecimentos_tecnicos = info_prof.get("conhecimentos_tecnicos", "")
        self.certificacoes = info_prof.get("certificacoes", "")
        self.outras_certificacoes = info_prof.get("outras_certificacoes", "")
        self.nivel_profissional = info_prof.get("nivel_profissional", "")
        self.qualificacoes = info_prof.get("qualificacoes", "")
        self.experiencias = info_prof.get("experiencias", "")
        
        try:
            self.remuneracao = float(info_prof.get("remuneracao", 0))
        except (ValueError, TypeError):
            self.remuneracao = None
        
        # Formação e Idiomas
        formacao = applicant_data.get("formacao_e_idiomas", {})
        self.nivel_academico = formacao.get("nivel_academico", "")
        self.nivel_ingles = formacao.get("nivel_ingles", "")
        self.nivel_espanhol = formacao.get("nivel_espanhol", "")
        self.outro_idioma = formacao.get("outro_idioma", "")
        self.outro_curso = formacao.get("outro_curso", "")
        
        # Cargo Atual
        cargo = applicant_data.get("cargo_atual", {})
        self.id_ibrati = cargo.get("id_ibrati", "")
        self.email_corporativo = cargo.get("email_corporativo", "")
        self.cargo_atual = cargo.get("cargo_atual", "")
        self.projeto_atual = cargo.get("projeto_atual", "")
        self.cliente = cargo.get("cliente", "")
        self.unidade = cargo.get("unidade", "")
        self.nome_superior_imediato = cargo.get("nome_superior_imediato", "")
        self.email_superior_imediato = cargo.get("email_superior_imediato", "")
        
        try:
            self.data_admissao = datetime.strptime(cargo.get("data_admissao", ""), "%d-%m-%Y")
        except (ValueError, TypeError):
            self.data_admissao = None
            
        try:
            self.data_ultima_promocao = datetime.strptime(cargo.get("data_ultima_promocao", ""), "%d-%m-%Y")
        except (ValueError, TypeError):
            self.data_ultima_promocao = None

        self.cv_pt = applicant_data.get("cv_pt", "")
        self.cv_en = applicant_data.get("cv_en", "")
