from raw_events.aedat4 import aedat4_unpack, aedat4_unpack_positiveonly
from raw_events.plot_rawevents import plot_events_3D_zoomed
import numpy as np
import os
#%%

filename = 'filename.aedat4' #replace with file name
x_array, y_array, t_array, polarity_array = aedat4_unpack_positiveonly(filename)
events = np.array([t_array, x_array,y_array, polarity_array]).T 

#%% Plot 3D Events zoomed ##
p = 0.0005  # Probability of success
x_center = 320
y_center = 320
zoom_range = 200
n_points = 1000000
plot_events_3D_zoomed(events, n_points, x_center, y_center, zoom_range, p)