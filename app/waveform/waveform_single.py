import json
from configobj import ConfigObj
import os
import obspy
from datetime import timedelta


def get_waveform_single(eventid, stationid):
    cfg = ConfigObj(os.path.expanduser('~/.seisPlotrc'))
    baseurl = os.path.expanduser(cfg["directory"])
    if(baseurl[-1] != "/"):
        baseurl = baseurl+"/"
    result = {}

    url_z = baseurl+eventid+"/*"+stationid+"*Z"
    url_r = baseurl+eventid+"/*"+stationid+"*R"
    url_t = baseurl+eventid+"/*"+stationid+"*T"

    zall = obspy.read(url_z)
    rall = obspy.read(url_r)
    tall = obspy.read(url_t)
    if(len(zall) != 0):
        z = zall[0]
        result["stats"] = {"delta": z.stats.delta,
                           "npts": z.stats.npts, "o": float(z.stats.sac.o)}
        result["z"] = z.data.tolist()
    elif(len(zall) == 0):
        result["z"] = None

    if(len(rall) != 0):
        r = rall[0]
        result["stats"] = {"delta": r.stats.delta,
                           "npts": r.stats.npts, "o": float(r.stats.sac.o)}
        result["r"] = r.data.tolist()
    elif(len(rall) == 0):
        result["r"] = None

    if(len(tall) != 0):
        t = tall[0]
        result["stats"] = {"delta": t.stats.delta,
                           "npts": t.stats.npts, "o": float(t.stats.sac.o)}
        result["t"] = t.data.tolist()
    elif(len(tall) == 0):
        result["t"] = None

    return json.dumps(result)


def post_waveform_single(eventid, stationid, data):
    cfg = ConfigObj(os.path.expanduser('~/.seisPlotrc'))
    baseurl = os.path.expanduser(cfg["directory"])
    if(baseurl[-1] != "/"):
        baseurl = baseurl+"/"
    result = {}

    url_z = baseurl+eventid+"/*"+stationid+"*Z"
    url_r = baseurl+eventid+"/*"+stationid+"*R"
    url_t = baseurl+eventid+"/*"+stationid+"*T"

    zall = obspy.read(url_z)
    rall = obspy.read(url_r)
    tall = obspy.read(url_t)
    if(len(zall) != 0):
        z = zall[0]
        result["stats"] = {"delta": z.stats.delta,
                           "npts": z.stats.npts, "o": float(z.stats.sac.o)}
        result["z"], result["stats"] = handle_post_single_waveform(
            z, data, result["stats"])

    elif(len(zall) == 0):
        result["z"] = None

    if(len(rall) != 0):
        r = rall[0]
        result["stats"] = {"delta": r.stats.delta,
                           "npts": r.stats.npts, "o": float(r.stats.sac.o)}
        result["r"], result["stats"] = handle_post_single_waveform(
            r, data, result["stats"])
    elif(len(rall) == 0):
        result["r"] = None

    if(len(tall) != 0):
        t = tall[0]
        result["stats"] = {"delta": t.stats.delta,
                           "npts": t.stats.npts, "o": float(t.stats.sac.o)}
        result["t"], result["stats"] = handle_post_single_waveform(
            t, data, result["stats"])
    elif(len(tall) == 0):
        result["t"] = None

    return json.dumps(result)


def handle_post_single_waveform(wave, data, stats):
    shock_time = wave.stats.starttime + \
        timedelta(seconds=float(wave.stats.sac.o))
    end_time = wave.stats.endtime
    start_time = data["start_time"]
    filter = data["filter"]
    wave = filt_data(wave, filter)
    if(start_time == "reference_time"):
        finalwave = wave
        stats = {"delta": finalwave.stats.delta,
                 "npts": finalwave.stats.npts,
                 "o": float(finalwave.stats.sac.o)}
        return finalwave.data.tolist(), stats
    elif(start_time == "shock_time"):
        finalwave = wave.slice(shock_time, end_time)
        stats = {"delta": finalwave.stats.delta,
                 "npts": finalwave.stats.npts,
                 "o": float(finalwave.stats.sac.o)}
        return finalwave.data.tolist(), stats
    elif(isinstance(start_time, float)):
        the_new_start_time = shock_time + \
            timedelta(seconds=float(start_time)) - \
            timedelta(seconds=200.0)
        finalwave = wave.slice(the_new_start_time, end_time)
        stats = {"delta": finalwave.stats.delta,
                 "npts": finalwave.stats.npts,
                 "o": float(finalwave.stats.sac.o)}
        return finalwave.data.tolist(), stats


def filt_data(wave, filter):
    if((filter[0] != 0) and (filter[1] != 0)):
        return wave.filter("bandpass", freqmin=1./filter[1], freqmax=1./filter[0])
    elif((filter[0] == 0) and (filter[1] != 0)):
        return wave.filter("lowpass", freq=1./filter[1])
    elif((filter[0] == 0) and (filter[1] == 0)):
        return wave
