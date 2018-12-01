from flask import Flask
from flask import request
from flask import Response
from predict import predict
from flask_cors import CORS, cross_origin
from flask import jsonify

app = Flask(__name__)
CORS(app, support_credentials=True)

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

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)