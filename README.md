# Event Processing
A Python toolkit for processing neuromorphic event imager data and generating frame reconstructions, visualizations, and videos.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Project Structure](#project-structure)


  ## Installation
This was implemented on python 3.13.7
  
Clone the repository:
```bash
git clone https://github.com/mahtabheydari/event-processing.git
cd event-processing

Dependencies:

pip install numpy
pip install pillow
pip install matplotlib
pip install opencv-python
pip install dv
pip install aedat
```
  ## Usage
run_DCE.py example: convert '.aedat4' files into video frames. 
```python

from raw_events.aedat4 import aedat4_unpack, aedat4_unpack_positiveonly
from raw_events.plot_rawevents import plot_events_3D_zoomed
from construct_frames.exposure import time_bins, exposure, build_2D_frames
from construct_frames.processed_visualization import visualize_timebins, visualize_timebins_zoomed,visualize_exposure_frames,visualize_exposure_video, visualize_exposure_frames_log, visualize_exposure_video_log
import os
import numpy as np
#%% Unpack the events

filename = 'blinkinglights_5031_97.aedat4' #replace with filename
x_array, y_array, t_array, polarity_array = aedat4_unpack_positiveonly(filename)
events = np.array([t_array, x_array,y_array, polarity_array]).T 

#%%
frequency = 200 #frames per second, time duration used to process events
period_fraction = 1 #exposure percentage, i.e., 0.5 = 50% exposure
frames = build_2D_frames(events, frequency, period_fraction, exposure_function='on_off', n_start_global=0)

output_video_path = os.path.splitext(filename)[0] + '.mp4'
video_fps = 50 #fps of exported video
visualize_exposure_video_log(frames, output_video_path, video_fps, frequency, period_fraction)
```

### 5. **Examples / Demo**
Resulting video from run_DCE. Event data collected on 3 blinking LEDS at varying frequencies (50 Hz, 31 Hz, 87 Hz)
Frames processed at 200 fps, 100% Exposure. Video saved at 50 fps
<img width="1918" height="962" alt="event frame" src="https://github.com/user-attachments/assets/329906e2-5216-40d1-bb97-7d7ef89e2047" />

```markdown
Video: https://github.com/user-attachments/assets/618b59e2-eeb5-43ae-8742-e4feebbf033b
```
Resulting 3D plot from visualize_events.py on blinking LED data. 

<img width="1200" height="600" alt="Figure_1" src="https://github.com/user-attachments/assets/daf8c71a-eaa6-4d20-9e7a-0354e87030c5" />
<img width="1200" height="600" alt="Figure_2" src="https://github.com/user-attachments/assets/e8684ff3-e9b0-41c4-a033-5dbcf639466d" />

## Project Structure
Main scripts: 
run_DCE.py
	Used to unpack .aedat4 event data and store it as an array.
  Performs digital coded exposure of events.
visualize_events.py 
	Used to unpack .aedat4 event data and store it as an array.
	Plot 3D events. Set the probability (p) to filter out events to speed up computation (all events are not needed for visualization). Center the plot at x_center, y_center, zoomed in from zoom_range. Set n_points 
  set how many points to visualize in plot
	--> In order to have pop up 3D plot that you can rotate/zoom in (see figures above), run visualize_events.py script directly from the command prompt

Helper Function: 
RAW EVENTS
	aedat4.py 
 		aedat4_unpack: this function unpacks all events from .aedat4 file
	  aedat4_unpack_positiveonly: this function unpacks only the positive events from .aedat4 file. This is often sufficient and reduces computation

	plot_rawevents.py
  	plot_events_3D_zoomed: plots 3D events

 CONSTRUCT FRAMES
 		exposure.py: this contains all the functions associated with digital coded exposure. 
	  processed_visualization: contains all functions associated with exposure visualization. can call these if you want to visualize in different ways (images vs video, log scale vs normal scale, etc.)

 

