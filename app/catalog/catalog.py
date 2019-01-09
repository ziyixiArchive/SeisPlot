from configobj import ConfigObj
import os
import obspy
import json
import glob
import numpy as np


def get_catalog():
    if(directory_has_problem()):
        return
    catalog = read_catalog()
    return catalog


def directory_has_problem():
    cfg = ConfigObj(os.path.expanduser('~/.seisPlotrc'))
    if(not os.path.exists(os.path.expanduser(cfg["directory"]))):
        print(cfg["directory"])
        return True


def read_catalog():
    cfg = ConfigObj(os.path.expanduser('~/.seisPlotrc'))
    baseurl = os.path.expanduser(cfg["directory"])
    if(baseurl[-1] != "/"):
        baseurl = baseurl+"/"
    result = []

    event_ids = os.listdir(baseurl)
    if(".DS_Store" in event_ids):
        event_ids.remove(".DS_Store")
    thecount = 1
    for event_id in event_ids:
        event_url = baseurl+event_id
        event_obspy = obspy.read(event_url+"/*Z")
        item = event_obspy[0]
        stats = item.stats
        item_result = {
            "index": thecount,
            "event_time": ".".join(str(stats.starttime).split(".")[:-1]),
            "event_id": event_id,
            "event_latitude": str(stats.sac["evla"]),
            "event_longitude": str(stats.sac["evlo"]),
            "event_depth": str(stats.sac["evdp"]),
            "event_magnitude": str(stats.sac["mag"])
        }
        result.append(item_result)
        thecount += 1

    return json.dumps(result)


def get_catalog_event(id):
    cfg = ConfigObj(os.path.expanduser('~/.seisPlotrc'))
    baseurl = os.path.expanduser(cfg["directory"])
    if(baseurl[-1] != "/"):
        baseurl = baseurl+"/"
    result = []
    event_url = baseurl+id
    event_z = glob.glob(event_url+"/*Z")
    event_r = glob.glob(event_url+"/*R")
    event_t = glob.glob(event_url+"/*T")
    thelength = np.array([len(event_z), len(event_r), len(event_t)])
    maxpos = thelength.argmax()

    if(maxpos == 0):
        event_obspy = obspy.read(event_url+"/*Z")
    elif(maxpos == 1):
        event_obspy = obspy.read(event_url+"/*R")
    elif(maxpos == 2):
        event_obspy = obspy.read(event_url+"/*T")

    for item in event_obspy:
        stats = item.stats
        item_result = {
            "station_name": str(stats.station),
            "station_latitude": str(stats.sac["stla"]),
            "station_longitude": str(stats.sac["stlo"]),
            "station_gcarc": str(stats.sac["gcarc"]),
        }
        result.append(item_result)

    return json.dumps(result)
