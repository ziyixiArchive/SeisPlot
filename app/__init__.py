import os
from flask import Flask
from flask_restful import Api, Resource, request
from .api import Login, Login_get_default, Catalog, Catalog_event, Waveform_single, Waveform_multiple
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Login, '/api/login')
api.add_resource(Login_get_default, '/api/login_get_default')
api.add_resource(Catalog, '/api/catalog')
api.add_resource(Catalog_event, '/api/catalog/<id>')
api.add_resource(Waveform_single, '/api/<eventid>/<stationid>')
api.add_resource(Waveform_multiple, '/api/waveform_multiple/<id>')
