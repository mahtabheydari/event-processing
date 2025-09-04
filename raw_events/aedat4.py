import dv_processing as dv
import aedat
from aedat import Decoder
import numpy as np
import PIL.Image # https://pypi.org/project/Pillow/
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os


def aedat4_unpack(filename):
    x_values = []
    y_values = []
    t_values = []
    polarity_values = []
    decoder = aedat.Decoder(filename)
    total_packets = 0
    for packet in decoder:
        total_packets += 1
        
    n = 0
    decoder = aedat.Decoder(filename)

    for packet in decoder:
        print('Packet %s/%s'%(n,total_packets))
        if "events" in packet:
            # For each event, extract x, y, t, and polarity
            for event in packet["events"]:
                b = (packet["events"])

                events_string = ','.join(str(x) for x in event)
                delimiters = r"[,()|]"
                events_list = re.split(delimiters, events_string)
                events_array = np.array(list(filter(None, events_list)))
    
                t_values.append(int(events_array[0]))
                x_values.append(int(events_array[1]))
                y_values.append(int(events_array[2]))
                
                polarity = 1 if events_array[3] == 'True' else -1
                polarity_values.append(polarity)
                
            n +=1
            if n == 31:
                break
                
            
    x_array = np.array(x_values)
    y_array = np.array(y_values)
    t_array = np.array(t_values)
    t_array = t_array[:] - np.min(t_array)
    polarity_array = np.array(polarity_values)
    return x_array, y_array, t_array, polarity_array


def aedat4_unpack_positiveonly(filename):
    x_values = []
    y_values = []
    t_values = []
    polarity_values = []
    decoder = aedat.Decoder(filename)
    total_packets = 0
    for packet in decoder:
        total_packets += 1
    print(total_packets)
        
    n = 0
    decoder = aedat.Decoder(filename)

    for packet in decoder:
        print('Packet %s/%s'%(n,total_packets))
        if "events" in packet:
            # For each event, extract x, y, t, and polarity
            for event in packet["events"]:
                b = (packet["events"])
                events_string = ','.join(str(x) for x in event)
                delimiters = r"[,()|]"
                events_list = re.split(delimiters, events_string)
                events_array = np.array(list(filter(None, events_list)))
                if events_array[3] == 'True':
                    t_values.append(int(events_array[0]))
                    x_values.append(int(events_array[1]))
                    y_values.append(int(events_array[2]))
                    polarity = 1 
                    polarity_values.append(polarity)
            n +=1
             
    x_array = np.array(x_values)
    y_array = np.array(y_values)
    t_array = np.array(t_values)
    t_array = t_array[:] - np.min(t_array)
    polarity_array = np.array(polarity_values)
    return x_array, y_array, t_array, polarity_array












