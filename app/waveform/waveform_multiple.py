import glob
import json
import os
from datetime import timedelta

import obspy
from configobj import ConfigObj
from obspy.taup import TauPyModel


def post_waveform_multiple(id, setting):
    cfg = ConfigObj(os.path.expanduser('~/.seisPlotrc'))
    baseurl = os.path.expanduser(cfg["directory"])
    if(baseurl[-1] != "/"):
        baseurl = baseurl+"/"

    event_search_base_url = baseurl+id+"/"
    z_url = event_search_base_url+"*Z"
    r_url = event_search_base_url+"*R"
    t_url = event_search_base_url+"*T"

    z = obspy.read(z_url)
    r = obspy.read(r_url)
    t = obspy.read(t_url)

    filter_range = setting["filter"]
    filt_data(z, filter_range)
    filt_data(r, filter_range)
    filt_data(t, filter_range)

    result = {
        "stats": {
            "z": [],
            "r": [],
            "t": []
        },
        "waves": {
            "z": [],
            "r": [],
            "t": []
        }
    }
    new_start_times, end_times = get_new_times(z, r, t, setting)

    for i, wave in enumerate(z):
        newwave = wave.slice(new_start_times["z"][i], end_times["z"][i])
        result["waves"]["z"].append(newwave.data.tolist())
        result["stats"]["z"].append({
            "delta": newwave.stats.delta,
            "npts": newwave.stats.npts,
            "o": float(newwave.stats.sac.o)
        })
    for i, wave in enumerate(r):
        newwave = wave.slice(new_start_times["r"][i], end_times["r"][i])
        result["waves"]["r"].append(newwave.data.tolist())
        result["stats"]["r"].append({
            "delta": newwave.stats.delta,
            "npts": newwave.stats.npts,
            "o": float(newwave.stats.sac.o)
        })
    for i, wave in enumerate(t):
        newwave = wave.slice(new_start_times["t"][i], end_times["t"][i])
        result["waves"]["t"].append(newwave.data.tolist())
        result["stats"]["t"].append({
            "delta": newwave.stats.delta,
            "npts": newwave.stats.npts,
            "o": float(newwave.stats.sac.o)
        })

    return json.dumps(result)


def filt_data(waves, filter_range):
    if((filter_range[0] == 0) and (filter_range[1] == 0)):
        return waves
    elif((filter_range[0] == 0) and (filter_range[1] != 0)):
        return waves.filter("lowpass", freq=1./filter_range[1])
    else:
        return waves.filter("bandpass", freqmin=1./filter_range[1], freqmax=1./filter_range[0])


def get_new_times(z, r, t, setting):
    shock_times = {
        "z": [],
        "r": [],
        "t": []
    }

    end_times = {
        "z": [],
        "r": [],
        "t": []
    }

    for wave in z:
        shock_times["z"].append(wave.stats.starttime +
                                timedelta(seconds=float(wave.stats.sac.o)))
        end_times["z"].append(wave.stats.endtime)
    for wave in r:
        shock_times["r"].append(wave.stats.starttime +
                                timedelta(seconds=float(wave.stats.sac.o)))
        end_times["r"].append(wave.stats.endtime)
    for wave in t:
        shock_times["t"].append(wave.stats.starttime +
                                timedelta(seconds=float(wave.stats.sac.o)))
        end_times["t"].append(wave.stats.endtime)

    start_time = setting["start_time"]
    new_start_times = {
        "z": [],
        "r": [],
        "t": []
    }

    if(start_time == "reference_time"):
        for i, wave in enumerate(z):
            new_start_times["z"].append(wave.stats.starttime)
        for i, wave in enumerate(r):
            new_start_times["r"].append(wave.stats.starttime)
        for i, wave in enumerate(t):
            new_start_times["t"].append(wave.stats.starttime)
    elif(start_time == "shock_time"):
        for i, wave in enumerate(z):
            new_start_times["z"].append(shock_times["z"][i])
        for i, wave in enumerate(r):
            new_start_times["r"].append(shock_times["r"][i])
        for i, wave in enumerate(t):
            new_start_times["t"].append(shock_times["t"][i])
    elif(start_time == "p_arrival_time"):
        for i, wave in enumerate(z):
            new_start_times["z"].append(cal_p_arrival(wave, setting))
        for i, wave in enumerate(r):
            new_start_times["r"].append(cal_p_arrival(wave, setting))
        for i, wave in enumerate(t):
            new_start_times["t"].append(cal_p_arrival(wave, setting))
    elif(start_time == "s_arrival_time"):
        for i, wave in enumerate(z):
            new_start_times["z"].append(cal_s_arrival(wave, setting))
        for i, wave in enumerate(r):
            new_start_times["r"].append(cal_s_arrival(wave, setting))
        for i, wave in enumerate(t):
            new_start_times["t"].append(cal_s_arrival(wave, setting))

    return new_start_times, end_times


def cal_p_arrival(wave, setting):
    model = TauPyModel(model=setting["model"])
    depth = float(wave.stats.sac.evdp)
    gcarc = float(wave.stats.sac.gcarc)
    p_obj = model.get_travel_times(
        source_depth_in_km=depth, distance_in_degree=gcarc, phase_list=["p"])
    if(p_obj == []):
        P_obj = model.get_travel_times(
            source_depth_in_km=depth, distance_in_degree=gcarc, phase_list=["P"])
        # return P_obj[0].time
        return wave.stats.starttime+timedelta(seconds=(float(wave.stats.sac.o)+P_obj[0].time))
    else:
        # return p_obj[0].time
        return wave.stats.starttime+timedelta(seconds=(float(wave.stats.sac.o)+p_obj[0].time))


def cal_s_arrival(wave, setting):
    model = TauPyModel(model=setting["model"])
    depth = float(wave.stats.sac.evdp)
    gcarc = float(wave.stats.sac.gcarc)
    s_obj = model.get_travel_times(
        source_depth_in_km=depth, distance_in_degree=gcarc, phase_list=["s"])
    if(s_obj == []):
        S_obj = model.get_travel_times(
            source_depth_in_km=depth, distance_in_degree=gcarc, phase_list=["S"])
        # return S_obj[0].time
        return wave.stats.starttime+timedelta(seconds=(float(wave.stats.sac.o)+S_obj[0].time))
    else:
        # return s_obj[0].time
        return wave.stats.starttime+timedelta(seconds=(float(wave.stats.sac.o)+s_obj[0].time))
