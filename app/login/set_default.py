from configobj import ConfigObj
import os
import subprocess


def set_default(cfg):
    if(not os.path.isfile('~/.seisPlotrc')):
        subprocess.call("touch ~/.seisPlotrc", shell=True)

    data = ConfigObj()
    data.filename = os.path.expanduser('~/.seisPlotrc')

    print(cfg['save'] == "True", type(cfg['save']))
    if(cfg['save']):
        data['name'] = cfg["name"]
        data['author'] = cfg["author"]
        data['description'] = cfg["description"]
        data['date'] = cfg["date"]
        data['directory'] = cfg["directory"]
        data['save'] = cfg["save"]

        data.write()
