import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_events_3D_zoomed(events, n_points, x_center, y_center, zoom_range, p, time_scale=5):
    """
    Plot a zoomed 3D scatter of event-based data, stretched along the time axis.

    Parameters
    ----------
    events : np.ndarray
        Array of shape (n,4) with columns [t, x, y, polarity].
    n_points : int
        Number of events to sample for plotting.
    x_center : float
        X-coordinate center for zooming.
    y_center : float
        Y-coordinate center for zooming.
    zoom_range : float
        Range around the center to include events in x and y directions.
    p : float
        Probability of keeping each event (Bernoulli subsampling).
    time_scale : float
        Scaling factor for the time axis (larger = longer time axis).
    """
    
    # Bernoulli subsampling
    size = len(events)
    bernoulli_samples = np.random.binomial(n=1, p=p, size=size)
    events = events[bernoulli_samples == 1]

    # Filter events within zoom range
    x_min = x_center - zoom_range/2
    x_max = x_center + zoom_range/2
    y_min = y_center - zoom_range/2
    y_max = y_center + zoom_range/2

    mask = (events[:,1] >= x_min) & (events[:,1] <= x_max) & \
           (events[:,2] >= y_min) & (events[:,2] <= y_max)
    zoomed_events = events[mask]

    if len(zoomed_events) == 0:
        print("No events in the zoomed region.")
        return

    # Randomly sample n_points
    if len(zoomed_events) > n_points:
        idx = np.random.choice(len(zoomed_events), n_points, replace=False)
        zoomed_events = zoomed_events[idx]

    t = zoomed_events[:,0]
    x = zoomed_events[:,1]
    y = zoomed_events[:,2]
    pol = zoomed_events[:,3]

    # Map polarity to color
    colors = np.where(pol > 0, 'red', 'blue')

    # Create 3D scatter plot
    fig = plt.figure(figsize=(12,6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, t, y, c=colors, s=1, alpha=0.7)

    ax.set_xlabel('X')
    ax.set_ylabel('Time')
    ax.set_zlabel('Y')
    ax.set_title(f'3D Event Plot Zoomed Around ({x_center}, {y_center})')
    ax.grid(False)

    # Set box aspect ratio: [X, Time, Y]
    ax.set_box_aspect([1, 5, 1])  # make Time axis 5x longer

    plt.show()
