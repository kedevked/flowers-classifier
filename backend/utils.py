import os
import json
import random
from collections import Counter
from torch import nn
import torch
from collections import OrderedDict



def create_sequential_layer(network):
	net = []

	for layer, contents in network.items():
		if layer =='input':
			name = contents['name']
			type = contents['type']
			insize= contents['in']
			outsize = contents['out']
			act = contents['act']
			actname = contents['actname']

			if type == 'linear':
				net.append((name, nn.Linear(insize, outsize)))
			else:
				return False
			if act == 'relu':
				net.append((actname,nn.ReLU()))
			if 'drop' in contents.keys():
				dropname = contents['dropname']
				net.append((dropname,nn.Dropout(float(contents['drop']))))


		if layer !='output' and layer!='input':
			name = contents['name']
			type = contents['type']
			insize= contents['in']
			outsize = contents['out']
			

			if type == 'linear':
				net.append((name, nn.Linear(insize, outsize)))
			else:
				return False
			if 'act' in contents.keys():
				act = contents['act']
				acctname = contents['actname']
				if act == 'relu':
					net.append((actname,nn.ReLU()))
				else:
					return False
			if 'drop' in contents.keys():
				dropname = contents['dropname']
				net.append((dropname,nn.Dropout(float(contents['drop']))))


		if layer =='output':
			name = contents['name']
			type = contents['type']
			dim = int(contents['dim'])
			if type == 'logsoft':
				net.append((name, nn.LogSoftmax(dim=dim)))

	return nn.Sequential(OrderedDict(net))




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


def get_random_model_ids():
	"""Returns 3 random model ids if there exist. Otherwise return whats available """
	with open('checkpoints/model_store.json') as f:
		model_store = json.load(f)

	model_ids = list(model_store.keys())

	if len(model_ids) > 2:
		return list(random.sample(model_ids, 3))
	else:
		return model_ids



def results_decider(results):
	"""Returns the result based on majority vote: if all is different selects the first"""

	counts = Counter(results)
	return max(counts, key=counts.get)

def validate_model(model):

	checkpoint = torch.load(model, map_location=lambda storage, loc: storage)
	valid_keys = ['network', 'arch', 'state_dict', 'class_to_idx']

	for key in valid_keys:
		if key not in checkpoint.keys():
			return False, key + " not found, please make sure your model contains this field"
	return True, "Valid model"

if __name__ == '__main__':
	#print(results_decider(['1','3','4','4']))
	#print(get_random_model_ids())

	data = {"input":{"name":"fc1", "type":"linear","in":1024, "out":100, "act":"relu",
			 "drop":0.2, "actname":"relu1", "dropname":"drop1"},
			"1":{"name":"fc2", "type":"linear","in":1024, "out":100, "act":"relu", "drop":0.2, "actname":"relu2", "dropname":"drop2"},
			"1":{"name":"fc3", "type":"linear","in":1024, "out":100},
		"output":{"name":"output", "type":"logsoft","dim":1}

	}

	checkpoint = {"arch":"densenet121", "network": data, "state_dict":[], "class_to_idx":[] }
	torch.save(checkpoint, 'test.pth')
	#print(create_sequential_layer(data))
