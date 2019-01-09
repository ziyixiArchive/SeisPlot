from configobj import ConfigObj
import os


def get_default():
    data = {}
    cfg = ConfigObj(os.path.expanduser('~/.seisPlotrc'))

    try:
        data['name'] = cfg["name"]
        data['author'] = cfg["author"]
        data['description'] = cfg["description"]
        data['date'] = cfg["date"]
        data['directory'] = cfg["directory"]
        data['save'] = cfg["save"]
    finally:
        return data
