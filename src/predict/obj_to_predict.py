from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import scipy.sparse

class obj_to_predict:
	def __init__(self, candidate: str, vacancy: str, comment: str, travel_required: int, pwd: int, english_level: int, spanish_level: int):
		self.candidate = candidate
		self.vacancy = vacancy
		self.comment = comment
		self.travel_required = travel_required
		self.pwd = pwd
		self.english_level = english_level
		self.spanish_level = spanish_level


	def transform_data(self, candidate_vectorizer: TfidfVectorizer, vacancy_vectorizer: TfidfVectorizer, comment_vectorizer: TfidfVectorizer, scaler: StandardScaler):
		vt_candidate = candidate_vectorizer.transform(self.candidate)
		vt_vacancy = vacancy_vectorizer.transform(self.vacancy)
		vt_comment = comment_vectorizer.transform(self.comment)
		data = np.array([self.travel_required, self.pwd, self.english_level, self.spanish_level])
		df = pd.DataFrame(data, columns=['vaga_viagens_requeridas', 'pcd', 'nivel_ingles', 'nivel_espanhol'])
		sc_data = scaler.transform(df)
		return scipy.sparse.hstack([sc_data, vt_candidate, vt_vacancy, vt_comment])