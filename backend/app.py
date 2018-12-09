from flask import Flask
from flask import request
from flask import Response
from predict import predict, predict_with_model, predict3
from flask_cors import CORS, cross_origin
from flask import jsonify
from werkzeug import secure_filename
import os
from numpy.random import randint
import utils



app = Flask(__name__)
CORS(app, support_credentials=True)
os.makedirs('checkpoints', exist_ok=True)


@app.route('/predict', methods=['POST', 'GET'])
@cross_origin()
def predict_flower():
    '''
        returns a flower prediction
    '''
    if request.method == 'POST':
        if 'file' not in request.files:
            return Response('No file uploaded', status=500)
        else :
            return jsonify({"name": predict(request.files['file'])})
    else:
        return Response('Bad request', status=500)


@app.route('/predict_new', methods=['POST', 'GET'])
@cross_origin()
def predict_flower_new():
    '''
        returns a flower prediction
    '''
    if request.method == 'POST':
        if 'file' not in request.files:
            return Response('No file uploaded', status=500)
        else :
            return jsonify({"name": predict3(request.files['file'])})
    else:
        return Response('Bad request', status=500)


@app.route('/upload_model', methods=['POST', 'GET'])
@cross_origin()
def upload_model():
    """Stores a checkpoint or saved model and returns a unique ID"""

    if request.method =='POST' and 'model' in request.files :
        f = request.files['model']

        valid , response = utils.validate_model(f)

        if valid:  
            pass
        else:
            return jsonify({"message": response})
    
        sec_file = secure_filename(f.filename)
        

        # generate random id: TOD0: write a function that checks for conflict
        model_id = ''.join(str(e) for e in list(randint(0, 9, 20)))

        # insert into model store
        utils.insert_id(model_id,sec_file)
        f.save(os.path.join('checkpoints', sec_file))
        return jsonify({"status": "saved" , "id":model_id})
    else:
        return Response('Bad request', status=500)


@app.route('/model_predict', methods=['POST', 'GET'])
@cross_origin()
def model_predict():
    """Predicts a flower species based on selected model id"""

    if request.method == 'POST':
        #validate the model_id
        if 'model_id' not in request.form:
            return Response('Required field model_id not present in request. Refill and retry', status=500)

        model_id = request.form.get('model_id')

        #validate the model file
        if 'file' not in request.files:
            return Response('No file uploaded', status=500)
        else :
            pred = predict_with_model(request.files['file'], model_id)
            return jsonify({"name": pred})
    else:
        return Response('Bad request', status=500)

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)

