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
import json
import torch
from flask_mail import Mail



app = Flask(__name__)
CORS(app, support_credentials=True)
os.makedirs('checkpoints', exist_ok=True)
app.config.update(
    MAIL_SERVER='smtp.googlemail.com',
    MAIL_PORT=465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = '',
    MAIL_PASSWORD = ''
)

mail = Mail(app)


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


@app.route('/upload-model', methods=['POST', 'GET'])
@cross_origin()
def upload_model():
    """Stores a checkpoint or saved model and returns a unique ID"""

    if request.method =='POST' and 'file' in request.files :
        f = request.files['file']
        print(type(f))
        #valid , response = utils.validate_model(f)

        if "model" in request.form.keys():  
            network = json.loads(request.form['model'])
            new_checkpoint=utils.insert_params(network, f)

        else:
            return jsonify({"message": "model param not present in request. Fill and resubmit"})
    
        sec_file = secure_filename(f.filename)        

        # generate random id: TOD0: write a function that checks for conflict
        model_id = ''.join(str(e) for e in list(randint(0, 9, 20)))

        
        #f.save(os.path.join('checkpoints', sec_file))
        filename = os.path.join('checkpoints', sec_file) #+ "_" + model_id
        filename = filename.split('.')[0] + "_" + model_id + ".pth"
        torch.save(new_checkpoint, filename)
        # insert into model store
        utils.insert_id(model_id,filename.split('/')[-1])

        # send email if present

        # if "email" in request.form.keys():
        #     recipient = request.form["email"]

        #     subject = "MODEL ID CONFIRMATION"
        #     sender = ''
        #     body = 'Your model has been successfully uploaded and saved. Your MODEL ID is: ' + model_id 
        #     body+='Please use this ID if you want to make predictions based on this model'

        #     res=utils.send_email(mail, body, subject, sender, recipient)
        #     pritn(res)

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


@app.route('/send_mail', methods=['POST', 'GET'])
@cross_origin()
def send_mail():

    valid_params = ['subject', 'message', 'sender', 'recipient']

    for i in valid_params:
        if i not in request.form.keys():
            return Response(i + "not present in the request fields. Refill and submit", status=400)

    subject = request.form['subject']
    message = request.form['message']
    sender = request. form['sender']
    recipient = request.form['recipient']

    msg = Message(message,
                  subject=subject,
                  sender=sender,
                  recipients=[recipient])

    mail.send(msg)

    return Response("Msg sent successfully")


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)

