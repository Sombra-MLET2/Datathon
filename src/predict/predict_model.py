import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import scipy.sparse
from typing import List

class PredictModel:
	def __init__(self, model_name: str) -> None:
		self.model_name = model_name
		self.model = self.__load_model(model_name)
		self.label_encoders = self.__load_label_encoders()
		self.standard_scaler = self.__load_standard_scaler()
		self.vectorizers = self.__load_vectorizers()


	@staticmethod
	def __load_model(model_name: str):
		try:
			if model_name == "RandomForest":
				return joblib.load("./model/train/RandomForest/model.gz")
			elif model_name == "XGBoost":
				return joblib.load("./model/train/XGBoost/model.gz")
			else:
				return None
		except:
			raise FileNotFoundError(f"Model {model_name} not found")


	@staticmethod
	def __load_label_encoders():
		try:
			return joblib.load("./model/train/label_encoders.gz")
		except:
			raise FileNotFoundError(f"Label encoders file not found")


	@staticmethod
	def __load_standard_scaler():
		try:
			return joblib.load("./model/train/standard_scaler.gz")
		except:
			raise FileNotFoundError(f"Standard scaler file not found")


	@staticmethod
	def __load_vectorizers():
		try:
			return joblib.load("./model/train/vectorizers.gz")
		except:
			raise FileNotFoundError(f"Vectorizers file not found")


	def predict(self, candidate: str, vacancy: str, comment: str, travel_required: int, pwd: int, english_level: int, spanish_level: int) -> str:
		data_to_predict = self.__transform_data(candidate, vacancy, comment, travel_required, pwd, english_level, spanish_level)
		result = self.model.predict(data_to_predict)
		return self.label_encoders["situacao"].inverse_transform(result)[0]


	def predict_df(self, df: pd.DataFrame) -> List[str]:
		df_to_predict = self.__transform_data_df(df)
		result = self.model.predict(df_to_predict)
		return self.label_encoders["situacao"].inverse_transform(result).tolist()


	def __transform_data(self, candidate: str, vacancy: str, comment: str, travel_required: int, pwd: int, english_level: int, spanish_level: int):
		vt_candidate = self.vectorizers['candidato'].transform([candidate])
		vt_vacancy = self.vectorizers['vaga'].transform([vacancy])
		vt_comment = self.vectorizers['comentario'].transform([comment])
		data = np.array([[travel_required, pwd, english_level, spanish_level]])
		df = pd.DataFrame(data, columns=['vaga_viagens_requeridas', 'pcd', 'nivel_ingles', 'nivel_espanhol'])
		sc_data = self.standard_scaler.transform(df)
		return scipy.sparse.hstack([sc_data, vt_candidate, vt_vacancy, vt_comment])


	def __transform_data_df(self, df: pd.DataFrame):
		vt_candidate = self.vectorizers['candidato'].transform(df['candidato'])
		vt_vacancy = self.vectorizers['vaga'].transform(df['vaga'])
		vt_comment = self.vectorizers['comentario'].transform(df['comentario'])
		aux_df = df[['vaga_viagens_requeridas', 'pcd', 'nivel_ingles', 'nivel_espanhol']]
		sc_data = self.standard_scaler.transform(aux_df)
		return scipy.sparse.hstack([sc_data, vt_candidate, vt_vacancy, vt_comment])