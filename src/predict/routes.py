import numpy as np
import pandas as pd
from fastapi import APIRouter
from src.predict.predict_model import PredictModel

prediction_router = APIRouter(
	prefix="/prediction",
	tags=["prediction"],
	responses={404: {"description": "Not found"}}
)

@prediction_router.get("/test")
async def test():
	candidate = "area administrativa administrativa    ensino superior incompleto  formacao\nensino medio completo\ninformatica intermediaria (excel, word, internet, outlook)\nadministracao financeira – senac\nexperiencia\n07/02/2021 a atual – teleperformance crm s/a.\nprincipais atividades: ativo em vendas para a philip morris cigarros marlboro.\n09/01/2020 a 10/02/2021 – foxtime recursos humanos\nprincipais atividades: prestacao de servicos para o banco aymore financiamentos de veiculos.\n21/12/2015 a 05/07/2019 – kpmg assurance services ltda.\nprincipais atividades: analise de processos judiciais pessoa fisica e juridica, a fim de evitar riscos para\nempresa com a contratacao de novos clientes. consiste em uma pesquisa a respeito da reputacao e\nintegridade da entidade e proprietarios/administradores. gerenciamento das solicitacoes recebidas pelo\ncliente.\n01/09/2015 a 19/12/2015 – royal academia ltda\nprincipais atividades: recepcao de alunos e funcionarios, funcoes administrativas.\n01/02/2013 a14/01/2015 – malta assessoria de cobrancas ltda\nprincipais atividades: realizar analise nos documentos pessoais e juridicos, contato com cliente verificando se\na indicios de fraude (utilizando os sistemas crivo/receita federal/mdb/aciona registro das analise dos\nclientes/sistemas tim).\n03/10/2011 a 18/05/2012- vetdantas produtos para animais ltda- me\nbancario, emissao e liberacao de pedidos, contas a pagar e receber.\nqualificacoes\nprofissional com excelente comunicacao e experiencia em atendimento, pleno dominio da rotina administrativa,\nboa digitacao, bom raciocinio logico, dedicada, adaptavel a mudancas e de facil relacionamento\n"
	vaga = "analista ensino superior cursando  ti - projetos- perfil: conhecimentos intermediarios excel (formulas, tabelas, pivotable e graficos)\ntrabalho pode ser remoto, mas ir presencialmente e um diferencial\nendereco do projeto: av. pres. juscelino kubitschek, 2235 - vila nova conceicao, sao paulo - sp, 04543-011\nhorario das 8 as 17hs budgeted rate - indicate currency and type (hourly/daily)* 80/h"
	vaga_viagens_requeridas = 0
	pcd = 0
	nivel_ingles = 0
	nivel_espanhol = 1
	comentario = ""
	test_prediction = PredictModel("RandomForest")
	result = test_prediction.predict(candidate, vaga, comentario,vaga_viagens_requeridas, pcd, nivel_ingles, nivel_espanhol)
	return {'result': result}


@prediction_router.get("/test-df")
async def test_df():
	candidate = "area administrativa administrativa    ensino superior incompleto  formacao\nensino medio completo\ninformatica intermediaria (excel, word, internet, outlook)\nadministracao financeira – senac\nexperiencia\n07/02/2021 a atual – teleperformance crm s/a.\nprincipais atividades: ativo em vendas para a philip morris cigarros marlboro.\n09/01/2020 a 10/02/2021 – foxtime recursos humanos\nprincipais atividades: prestacao de servicos para o banco aymore financiamentos de veiculos.\n21/12/2015 a 05/07/2019 – kpmg assurance services ltda.\nprincipais atividades: analise de processos judiciais pessoa fisica e juridica, a fim de evitar riscos para\nempresa com a contratacao de novos clientes. consiste em uma pesquisa a respeito da reputacao e\nintegridade da entidade e proprietarios/administradores. gerenciamento das solicitacoes recebidas pelo\ncliente.\n01/09/2015 a 19/12/2015 – royal academia ltda\nprincipais atividades: recepcao de alunos e funcionarios, funcoes administrativas.\n01/02/2013 a14/01/2015 – malta assessoria de cobrancas ltda\nprincipais atividades: realizar analise nos documentos pessoais e juridicos, contato com cliente verificando se\na indicios de fraude (utilizando os sistemas crivo/receita federal/mdb/aciona registro das analise dos\nclientes/sistemas tim).\n03/10/2011 a 18/05/2012- vetdantas produtos para animais ltda- me\nbancario, emissao e liberacao de pedidos, contas a pagar e receber.\nqualificacoes\nprofissional com excelente comunicacao e experiencia em atendimento, pleno dominio da rotina administrativa,\nboa digitacao, bom raciocinio logico, dedicada, adaptavel a mudancas e de facil relacionamento\n"
	vaga = "analista ensino superior cursando  ti - projetos- perfil: conhecimentos intermediarios excel (formulas, tabelas, pivotable e graficos)\ntrabalho pode ser remoto, mas ir presencialmente e um diferencial\nendereco do projeto: av. pres. juscelino kubitschek, 2235 - vila nova conceicao, sao paulo - sp, 04543-011\nhorario das 8 as 17hs budgeted rate - indicate currency and type (hourly/daily)* 80/h"
	vaga_viagens_requeridas = 0
	pcd = 0
	nivel_ingles = 0
	nivel_espanhol = 1
	comentario = ""
	data = np.array([[candidate, vaga, vaga_viagens_requeridas, pcd, nivel_ingles, nivel_espanhol, comentario]])
	df = pd.DataFrame(data, columns=['candidato', 'vaga', 'vaga_viagens_requeridas', 'pcd', 'nivel_ingles', 'nivel_espanhol', 'comentario'])
	test_prediction = PredictModel("XGBoost")
	result = test_prediction.predict_df(df)
	return {'result': result}