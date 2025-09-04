# Event Processing
A Python toolkit for processing neuromorphic event imager data and generating frame reconstructions, visualizations, and videos.
This idea was adapted from Gothard et al. More technical details can be found in their [2022 paper](https://doi.org/10.1088/2634-4386/ac4917)

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

### **Examples / Demo**
Resulting video from run_DCE. Event data collected on 3 blinking LEDS at varying frequencies (50 Hz, 31 Hz, 87 Hz)
Frames processed at 200 fps, 100% Exposure. Video saved at 50 fps
<img width="1918" height="962" alt="event frame" src="https://github.com/user-attachments/assets/329906e2-5216-40d1-bb97-7d7ef89e2047" />

```markdown
Video: https://github.com/user-attachments/assets/618b59e2-eeb5-43ae-8742-e4feebbf033b
```
Resulting 3D plot from visualize_events.py on blinking LED data. 

<img width="1200" height="600" alt="Figure_1" src="https://github.com/user-attachments/assets/daf8c71a-eaa6-4d20-9e7a-0354e87030c5" />
<img width="1200" height="600" alt="Figure_2" src="https://github.com/user-attachments/assets/e8684ff3-e9b0-41c4-a033-5dbcf639466d" />

## 📂 Project Structure

### 🔹 Main Scripts
- **`run_DCE.py`**  
  - Unpacks `.aedat4` event data and stores it as a NumPy array.  
  - Performs **digital coded exposure (DCE)** on the events.  

- **`visualize_events.py`**  
  - Unpacks `.aedat4` event data and stores it as an array.  
  - Plots **3D event clouds** with adjustable parameters:  
    - `p`: probability to filter events (reduce computation, not all events are needed).  
    - `x_center, y_center`: center coordinates of zoomed region.  
    - `zoom_range`: window size around the center.  
    - `n_points`: number of events to visualize.  
  - 👉 To view an **interactive 3D plot** (rotatable and zoomable), run this script directly from the **command prompt**.

---

### 🔹 Helper Functions

#### 📌 Raw Events
- **`aedat4.py`**
  - `aedat4_unpack`: Unpack **all events** from `.aedat4` file.  
  - `aedat4_unpack_positiveonly`: Unpack **only positive events** (often sufficient and reduces computation).  

- **`plot_rawevents.py`**
  - `plot_events_3D_zoomed`: Plot **3D event clouds** with zoom and filtering options.  

#### 📌 Construct Frames
- **`exposure.py`**  
  - Contains functions for **digital coded exposure** (DCE).  

- **`processed_visualization.py`**  
  - Functions for visualizing exposure results in multiple ways:  
    - Images vs. Video.  
    - Log scale vs. Normal scale.  


