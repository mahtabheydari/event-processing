import numpy as np
import PIL.Image # https://pypi.org/project/Pillow/
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import cv2
from matplotlib.colors import LogNorm

def visualize_timebins(groups, nframes, RPM): 
    for n in range (0,nframes):   #change based on which frames you want to generate
        example = groups[n]
        example = example[:,1:4]
        
        grid = np.zeros((480, 640))
        for i in range(example.shape[0]):
            x, y = example[i,0:2]
            grid[y, x] += example[i,2] 
        
        maxabs = max(np.abs(np.max(grid)), np.abs(np.min(grid)))
        
        # Avoid log(0) by setting a minimum value
        grid[grid == 0] = 1e-3
        
        plt.imshow(grid, cmap='Greys', norm=LogNorm())
        plt.colorbar() 
        plt.title('%s Hz'%(RPM))
        plt.axis('off')  # This removes the axis ticks and labels

        plt.show()
    

def visualize_timebins_zoomed(groups,nframes,xcenter,ycenter,zoomrange):
    for n in range(0, nframes):   # Change based on which frames you want to generate
        example = groups[n]
        example = example[:, 1:4]
        
        grid = np.zeros((480, 640))
        for i in range(example.shape[0]):
            x, y = example[i, 0:2]
            grid[y, x] += example[i, 2] 
        
        # Calculate max absolute value for color scaling
        maxabs = max(np.abs(np.max(grid)) , np.abs(np.min(grid)))
        
        # Zooming logic
        x_min = max(xcenter - zoomrange, 0)
        x_max = min(xcenter + zoomrange, grid.shape[1])
        y_min = max(ycenter - zoomrange, 0)
        y_max = min(ycenter + zoomrange, grid.shape[0])
        
        # Slice the grid to zoom in
        zoomed_grid = grid[y_min:y_max, x_min:x_max]

        # Plot the zoomed-in portion
        plt.imshow(zoomed_grid, cmap='RdBu', vmin=-maxabs, vmax=maxabs)
        plt.colorbar()
        plt.title("Summed Events, Frame = %s"%(n))
        plt.show()
        
def visualize_exposure_frames(groups_with_exposure, n_frames,period_fraction, RPM):
    for n in range (0,n_frames):   
        example = groups_with_exposure[n]
        example = example[:,1:4]
        
        grid = np.zeros((480, 640))
        for i in range(example.shape[0]):
            x, y = example[i,0:2]
            grid[y, x] += example[i,2] 
        plt.imshow(grid, cmap = 'Greys')
        plt.colorbar() 
        plt.title("Boxcar Exposure Function %s, %s RPM" %(period_fraction, RPM))
        plt.show()
        
def create_exposure_frames(groups_with_exposure, n_frames):
    frames = []
    for n in range (0,n_frames):   
        example = groups_with_exposure[n]
        example = example[:,1:4]
        
        grid = np.zeros((480, 640))
        for i in range(example.shape[0]):
            x, y = example[i,0:2]
            grid[y, x] += example[i,2] 
        frames.append(grid)
    return frames

        

def create_frames(data_list, height=480, width=640):
    frames = []
    for example in data_list:
        grid = np.zeros((height, width), dtype=np.float32)
        for i in range(example.shape[0]):
            x, y = example[i, 1:3].astype(int)  # Use columns 1 and 2
            value = example[i, 3]
            if 0 <= x < width and 0 <= y < height:
                grid[y, x] += value
        frames.append(grid)
    return frames


def visualize_exposure_video(groups_with_exposure, n_frames, period_fraction, output_video_path='output_video.mp4'):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4
    out = cv2.VideoWriter(output_video_path, fourcc, 30.0, (640, 480))  # 30 fps and 640x480 resolution
    
    for n in range(n_frames):
        example = groups_with_exposure[n]
        example = example[:, 1:4]
        
        grid = np.zeros((480, 640))

        for i in range(example.shape[0]):
            x, y = example[i, 0:2]
            grid[y, x] += example[i, 2]  

        grid_normalized = cv2.normalize(grid, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        grid_bgr = cv2.cvtColor(grid_normalized, cv2.COLOR_GRAY2BGR)

        out.write(grid_bgr)

    out.release()
    print(f"Video saved at {output_video_path}")

def visualize_exposure_frames_zoomed(groups_with_exposure, n_frames, period_fraction, xcenter, ycenter, window_size):
    # Assuming the zoomed region is always 100x100
    zoomed_frames = np.zeros((n_frames, 2 * window_size, 2 * window_size))

    for n in range(n_frames): 
        print (n)
        example = groups_with_exposure[n][:, 1:4]  # Extract x, y, polarity

        grid = np.zeros((480, 640))
        for i in range(example.shape[0]):
            x, y = example[i, 0:2].astype(int)
            if 0 <= x < 640 and 0 <= y < 480:
                grid[y, x] += example[i, 2]

        # Zooming logic
        x_min = max(xcenter - window_size, 0)
        x_max = min(xcenter + window_size, grid.shape[1])
        y_min = max(ycenter - window_size, 0)
        y_max = min(ycenter + window_size, grid.shape[0])

        zoomed_grid = grid[y_min:y_max, x_min:x_max]

        # Store the frame (make sure it’s exactly 100x100)
        if zoomed_grid.shape == (2 * window_size, 2 * window_size):
            zoomed_frames[n] = zoomed_grid
        else:
            # Pad if necessary (edge cases)
            padded = np.zeros((2 * window_size, 2 * window_size))
            padded[:zoomed_grid.shape[0], :zoomed_grid.shape[1]] = zoomed_grid
            zoomed_frames[n] = padded

        # Optional: Save the image
        plt.imshow(zoomed_grid, cmap='Greys')
        plt.colorbar()
        plt.title(f"Summed Events, Frame = {n}")
        #plt.savefig(f'exposure_{period_fraction*100:.0f}_zoomed_frame{n}.png')
        plt.close()

    return zoomed_frames
        
        
def visualize_exposure_frames_log(groups_with_exposure, n_frames, period_fraction, RPM):
    for n in range(n_frames):   
        example = groups_with_exposure[n]
        example = example[:, 1:4]
        
        grid = np.zeros((480, 640))
        for i in range(example.shape[0]):
            x, y = example[i, 0:2].astype(int)
            grid[y, x] += example[i, 2] 
    
        # Avoid log(0) by setting a minimum value
        grid[grid == 0] = 1e-3
        
        plt.imshow(grid, cmap='Greys', norm=LogNorm())
        plt.colorbar() 
        plt.title(f"Boxcar Exposure Function {period_fraction}, {RPM} RPM")
        plt.show()


def visualize_exposure_video_log(frames, output_video_path, fps, frequency, period_fraction):
    """
    Create a video from  2D frames with log normalization.

    Parameters
    ----------
    
    frames : np.ndarray
        Array of shape (n_frames, 480, 640), each 2D frame.
    output_video_path : str
        Path to save the output video.
    fps : float
        Frames per second of the output video.
    frequency : in fps. the time window for exposure. included for labeling the title
    period_fraction : exposure fraction. included for labeling the title 
    
    """
    n_frames, height, width = frames.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    epsilon = 1e-3  # small value to avoid log(0)

    for n in range(n_frames):
        grid = frames[n]

        # Log normalization
        log_grid = np.log(grid + epsilon)

        norm_log_grid = cv2.normalize(log_grid, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        grid_bgr = cv2.cvtColor(norm_log_grid, cv2.COLOR_GRAY2BGR)
        
        title = 'Frequency = %s fps, Exposure = %s'%(frequency, period_fraction)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        font_color = (255, 255, 255)  # white text
        thickness = 1
        line_type = cv2.LINE_AA
        cv2.putText(grid_bgr, title, (10, 30), font, font_scale, font_color, thickness, line_type)

        out.write(grid_bgr)

    out.release()
    print(f"Video saved at {output_video_path}")