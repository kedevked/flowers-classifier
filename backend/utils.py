import os
import json
import random
from collections import Counter
from torch import nn
import torch
from collections import OrderedDict
from flask_mail import Message


def load_checkpoint_model(checkpoint):
      
    arch = checkpoint['arch']
    arch = arch.lower()
    print(arch)
    if arch == "densenet121":
        model = models.densenet121(pretrained=True)
    elif arch =="resnet18":
        model= models.resnet18(pretrained=True)
    elif arch == "alexnet":
        model = models.alexnet(pretrained=True)
    elif arch =="squeezenet":
        model = models.squeezenet1_0(pretrained=True)
    elif arch =="vgg16":
        model = models.vgg16(pretrained=True)
    elif arch =="densenet161":
        model = models.densenet161(pretrained=True)
    elif arch =="inception":
        model = models.inception_v3(pretrained=True)  

    else:
        return False
    model.classifier = utils.create_classifer(checkpoint['network'])
    model.load_state_dict(checkpoint['state_dict'])
    model.class_to_idx = checkpoint['class_to_idx']
    return model

 

def create_sequential_layer(network):

	"""Parser for creating sequential layers for the model(Depreciated)"""
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


def create_classifer(network):
	"""Parser for creating sequential layers for the model"""

	net = []
	#print(network)
	for layer in network:
		type = layer['type']
		contents = layer
		if type == "linear":
			name = contents['name']
			insize= contents['in']
			outsize = contents['out']
			net.append((name, nn.Linear(insize, outsize)))

		elif type =="relu":
			name = contents['name']
			net.append((name,nn.ReLU()))

		elif type == "dropout":
			name = contents['name']
			drop = contents['drop']
			net.append((name,nn.Dropout(float(drop))))

		elif type == "logsoft":
			name = contents['name']
			dim = int(contents['drop'])
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


def insert_params(network, model):
	checkpoint = torch.load(model, map_location=lambda storage, loc: storage)

	checkpoint['network'] = network['layers']
	checkpoint['arch'] = network['arch']

	return checkpoint



def send_email(mail, message, subject, sender, recipient):
    msg = mail.send_message(body=message,
              subject=subject,
              sender=sender,
              recipients=[recipient])

    #	mail.send(msg)

    return "Msg sent successfully"



def model_testing(model):
	try:
		loaded_model = load_checkpoint_model(model)
		print(loaded_model)
		if loaded_model:
			return True
		else:
			return False
	except Exception as e:
		return False
	




if __name__ == '__main__':
	#print(results_decider(['1','3','4','4']))
	#print(get_random_model_ids())

	# data = {"input":{"name":"fc1", "type":"linear","in":1024, "out":100, "act":"relu",
	# 		 "drop":0.2, "actname":"relu1", "dropname":"drop1"},
	# 		"1":{"name":"fc2", "type":"linear","in":1024, "out":100, "act":"relu", "drop":0.2, "actname":"relu2", "dropname":"drop2"},
	# 		"1":{"name":"fc3", "type":"linear","in":1024, "out":100},
	# 	"output":{"name":"output", "type":"logsoft","dim":1}

	# }

	data = [{"name":"fc1", "type":"linear", "in":1024, "out": 300},
			{"name":"relu1", "type":"relu"}, {"name":"drop1", "type":"dropout", "drop":0.2 },
			{"name":"fc2", "type":"linear", "in":300, "out": 102}, 
			{"name":'output', "type": "logsoft", "dim":1}]
	checkpoint = {"arch":"densenet121", "network": data, "state_dict":[], "class_to_idx":[] }
	#torch.save(checkpoint, 'test.pth')
	#print(create_sequential_layer(data))
	#print(create_classifer(data))

	#insert arch

	checkpoint = torch.load('checkpoints/checkpoint_1_81241662617885720627.pth', map_location=lambda storage, loc: storage)

	checkpoint['arch'] = 'densenet121'

	