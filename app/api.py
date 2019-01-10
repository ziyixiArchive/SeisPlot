from flask_restful import Resource, request
from .login import set_default, get_default
from .catalog import get_catalog, get_catalog_event
from .waveform import get_waveform_single, post_waveform_single, post_waveform_multiple


class Login(Resource):
    def post(self):
        data = request.get_json(force=True)
        set_default(data)
        return "success"


class Login_get_default(Resource):
    def get(self):
        return get_default()


class Catalog(Resource):
    def get(self):
        return get_catalog()


class Catalog_event(Resource):
    def get(self, id):
        return get_catalog_event(id)


class Waveform_single(Resource):
    def get(self, eventid, stationid):
        return get_waveform_single(eventid, stationid)

    def post(self, eventid, stationid):
        data = request.get_json(force=True)
        return post_waveform_single(eventid, stationid, data)


class Waveform_multiple(Resource):
    def post(self, id):
        setting = request.get_json(force=True)
        return post_waveform_multiple(id, setting)
