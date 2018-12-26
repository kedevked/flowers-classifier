import argparse
import os
import json
import numpy as np
import torch
from torch import nn
from torch import optim
import matplotlib.pyplot as plt
from torchvision import datasets, transforms, models
from PIL import Image
import os
from torch.autograd import Variable
from collections import OrderedDict
import utils

parser = argparse.ArgumentParser()

parser.add_argument('image', nargs='?', help='image path')

parser.add_argument('dir', nargs='?', help='checkpoint file')

parser.add_argument('--topk', action='store',
                    default=5,
                    dest='topk',
                    help='topk classes',
                    type=int
                   )

parser.add_argument('--category_names', action='store',
                    dest='categories',
                    help='json file with all categories',
                   )

parser.add_argument('--gpu', 
                    action='store_const', 
                    default=False, 
                    const=True,
                    help='use gpu')

arguments = parser.parse_args()

device = 'gpu' if arguments.gpu and torch.cuda.is_available() else 'cpu'

def load_checkpoint(filepath):
    
    model = models.densenet121(pretrained=True)
    
    classifier = nn.Sequential(OrderedDict([
                      ('fc1', nn.Linear(1024, 300)),
                      ('relu1', nn.ReLU()),
                      ('fc2', nn.Linear(300, 102)),
                      ('output', nn.LogSoftmax(dim=1))]))
    model.classifier = classifier
    checkpoint = torch.load(filepath, map_location=lambda storage, loc: storage)
    model.load_state_dict(checkpoint['state_dict'])
    model.class_to_idx = checkpoint['class_to_idx']
    return model


def load_checkpoint_test(filepath):
    
    model = models.densenet121(pretrained=True)
    
    classifier = nn.Sequential(OrderedDict([
                      ('fc1', nn.Linear(1024, 500)),
                      ('relu1', nn.ReLU()),
                      ('fc2', nn.Linear(500, 102)),
                      ('output', nn.LogSoftmax(dim=1))]))
    model.classifier = classifier
    checkpoint = torch.load(filepath, map_location=lambda storage, loc: storage)
    model.load_state_dict(checkpoint['state_dict'])
    model.class_to_idx = checkpoint['class_to_idx']
    return model


def load_checkpoint_general(filepath):
      
    checkpoint = torch.load(filepath, map_location=lambda storage, loc: storage)
    arch = checkpoint['arch']
    arch = arch.lower()
    #print(arch)
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



loaded_model = load_checkpoint_test('checkpoints/checkpoint_1_34078121870140268755.pth')
with open('cat_to_name.json', 'r') as f:
    cat_to_name = json.load(f)

def get_flowers_name(classes):
    flowers_name = [cat_to_name[index] for index in classes]
    return flowers_name


def process_image(image):
    ''' Scales, crops, and normalizes a PIL image for a PyTorch model,
        returns an Numpy array
    '''
    
    # TODO: Process a PIL image for use in a PyTorch model
    
    size = 256, 256
    image.thumbnail(size, Image.ANTIALIAS)
    
    width, height = image.size   # Get dimensions
    print('w', width, 'h', height)
    new_width, new_height = 224, 224
    
    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

    image = image.crop((left, top, right, bottom))
    
    # im.crop(8, 8, 248, 248)
    np_image = np.array(image)/255
    np_norm =  ( np_image - np.array([0.485, 0.456, 0.406]) ) / np.array([0.229, 0.224, 0.225])
    return np_norm.transpose((-1, 0, 1))

def predict(image_path) :
    print('predict')
    _, classes = predict_top_classes(image_path)
    print('classes', classes)
    print('element', classes[0])
    flowers = get_flowers_name(classes)
    return flowers[0]

def predict3(image_path):
    #load model 
    results = []
    for model_id in utils.get_random_model_ids():
        print(model_id)
        filepath = utils.get_model_path(model_id)
        loaded_model = load_checkpoint_general('checkpoints/'+filepath)

        _, classes = predict_top_classes(image_path,loaded_model)
        
        results.append(classes[0])
    print(results)
    return get_flowers_name(list(utils.results_decider(results)))[0]



def predict_with_model(image_path, model_id):

    #load model 
    filepath = utils.get_model_path(model_id)
    loaded_model = load_checkpoint('checkpoints/'+filepath)

    _, classes = predict_top_classes(image_path,loaded_model)
    print('classes', classes)
    print('element', classes[0])
    flowers = get_flowers_name(classes)
    return flowers[0]

    
def predict_top_classes(image_path, model=loaded_model, topk=1):
    ''' Predict the class (or classes) of an image using a trained deep learning model.
    '''
    # TODO: Implement the code to predict the class from an image file
    image = Image.open(image_path)
    img = process_image(image)
    
    # move model and input to gpu if available
    model.to(device)

    model.eval()

    # Calculate the class probabilities (softmax) for img
    with torch.no_grad():
        output = model.forward(Variable(torch.FloatTensor([img]).to(device)))

    ps, indices = torch.exp(output).topk(5)
    index_to_class = {v: k for k, v in model.class_to_idx.items()}
    return ps.numpy().flatten().tolist(), [index_to_class[index] for index in indices.numpy().flatten().tolist()]
