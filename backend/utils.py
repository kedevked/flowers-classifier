import os
import json


def insert_id(model_id, filename):

	"""This function inserts a model id the model store"""

	#load model store json
	model_store = {}
	with open('checkpoints/model_store.json') as f:
		model_store = json.load(f)

	model_store[model_id] = filename

	with open('checkpoints/model_store.json', 'w') as f:
		json.dump(model_store, f)


	return True



def get_model_path(model_id):
	"""This function returns the path of a model based on the model ID"""
	with open('checkpoints/model_store.json') as f:
		model_store = json.load(f)

		if model_id in model_store.keys():
			return model_store[model_id]

		else:
			return False

