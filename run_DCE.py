from raw_events.aedat4 import aedat4_unpack, aedat4_unpack_positiveonly
from raw_events.plot_rawevents import plot_events_3D_zoomed
from construct_frames.exposure import time_bins, exposure, build_2D_frames
from construct_frames.processed_visualization import visualize_timebins, visualize_timebins_zoomed,visualize_exposure_frames,visualize_exposure_video, visualize_exposure_frames_log, visualize_exposure_video_log
import os
import numpy as np
#%% Unpack the events

filename = 'filename.aedat4' #replace with filename
x_array, y_array, t_array, polarity_array = aedat4_unpack_positiveonly(filename)
events = np.array([t_array, x_array,y_array, polarity_array]).T 

#%%
frequency = 100 #frames per second, time duration used to process events
period_fraction = 0.2 #exposure percentage, i.e., 0.5 = 50% exposure
frames = build_2D_frames(events, frequency, period_fraction, exposure_function='on_off', n_start_global=0)

output_video_path = os.path.splitext(filename)[0] + '.mp4'
visualize_exposure_video_log(frames, output_video_path, 50, frequency, period_fraction)
