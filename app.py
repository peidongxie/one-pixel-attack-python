from random import randint

from flask import Flask, request

from attack import attack
from load import *

app = Flask(__name__)


@app.after_request
def cors(response):
    try:
        origin = request.headers['Origin']
        if origin.endswith('peaceandlove.top'):
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            response.headers['Access-Control-Allow-Method'] = 'GET,POST,OPTIONS'
            response.headers['Access-Control-Allow-Origin'] = origin
        return response
    except KeyError:
        return response


@app.route('/')
def main():
    return 'This is the Flask backend of the One Pixel Attack project.'


@app.route('/attack', methods=['POST'])
def attack_controller():
    json = request.get_json(force=True)
    try:
        if json['image'] == '':
            index = randint(0, 9999)
            path = image_creator(index)
            image = image_loader(path)
            label = label_loader(index)
        else:
            path = 'static/' + json['image']
            image = image_loader(path)
            label = json['label']
        model = model_loader('static/' + json['model'])
        count = json['count']
        normalized = json['normalized']
    except KeyError:
        return {'success': False}
    if image is None:
        return {'success': False}
    width, height, label, prediction, perturbation, affected_prediction = attack(image, model, label, count, normalized)
    return {
        'image': base64_loader(path),
        'width': width,
        'height': height,
        'label': label,
        'before': (prediction * 1000).astype(int).tolist(),
        'change': perturbation,
        'after': (affected_prediction * 1000).astype(int).tolist(),
        'success': True,
    }


@app.route('/file', methods=['POST'])
def file_controller():
    try:
        file = request.files['file']
    except KeyError:
        return {'name': ''}
    filename = file.filename
    if filename.endswith('.npy') or filename.endswith('.png'):
        return {'name': image_creator(file)[7:]}
    elif filename.endswith('.h5'):
        return {'name': model_creator(file)[7:]}
    else:
        return {'name': ''}


@app.route('/image/<name>', methods=['GET'])
def image_controller(name):
    base64 = base64_loader('static/' + name)
    if base64 is None:
        return {'base64': ''}
    else:
        return {'base64': base64}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50001, ssl_context=('api.peaceandlove.top.pem', 'api.peaceandlove.top.key'))
