import joblib
from src.predict.obj_to_predict import obj_to_predict

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
				return joblib.load("model/RandomForest/model.gz")
			elif model_name == "XGBoost":
				return joblib.load("model/XGBoost/model.gz")
			else:
				return None
		except:
			raise FileNotFoundError(f"Model {model_name} not found")


	@staticmethod
	def __load_label_encoders():
		try:
			return joblib.load("model/label_encoders.gz")
		except:
			raise FileNotFoundError(f"Label encoders file not found")


	@staticmethod
	def __load_standard_scaler():
		try:
			return joblib.load("model/standard_scaler.gz")
		except:
			raise FileNotFoundError(f"Standard scaler file not found")


	@staticmethod
	def __load_vectorizers():
		try:
			return joblib.load("model/vectorizers.gz")
		except:
			raise FileNotFoundError(f"Vectorizers file not found")


	def predict(self, obj: obj_to_predict):
		data_to_predict = obj.transform_data(self.vectorizers.candidato, self.vectorizers.vaga, self.vectorizers.comentario, self.standard_scaler)
		result = self.model.predict(data_to_predict)
		return self.label_encoders.situacaoinverse_transform(result)