import numpy as np

def time_bins(frame_time, events):
    events_timesorted = events[events[:, 0].argsort()]
    
    # Initialize a list to store event groups
    groups = []
    
    # Determine the bin index for each event
    current_group = []
    current_bin_start = 0
    
    for event in events_timesorted:
        event_time = event[0]
        bin_index = int(event_time // frame_time)  # Determine the bin index based on event time
        
        if bin_index == current_bin_start:
            current_group.append(event)
        else:
            if current_group:
                groups.append(np.array(current_group))
            current_group = [event]
            current_bin_start = bin_index
    
    # Append the last group
    if current_group:
        groups.append(np.array(current_group))
    
    return groups


def exposure(groups, function, period_fraction):
    groups_withexposure = []

    for current_group in groups:
        current_group = np.array(current_group)
        current_group_timenormalized = current_group[:,0] - np.min(current_group[:,0])
        current_group[:,0] = current_group_timenormalized
        total_time = current_group_timenormalized[-1]  
        
        period_length = period_fraction * total_time
        
        time = current_group_timenormalized
        
        
        if function == 'on_off':
            weighted_polarity = np.array([1 if t < period_length  else 0 for t in time])
        
        elif function == 'triangle':
            weighted_polarity = np.array([2 * (t % period_length) / period_length if (t % period_length) < period_length / 2 else 2 * (1 - (t % period_length) / period_length) for t in time])
        
        elif function == 'sinusoidal':
            weighted_polarity = np.sin(2 * np.pi * time / period_length)
        
        else:
            raise ValueError(f"Unknown function type: {function}")
        
        currentgroup_withexposure = np.copy(current_group)
        currentgroup_withexposure[:, 3] = weighted_polarity*current_group[:,3]
        
        groups_withexposure.append(currentgroup_withexposure)
    return groups_withexposure




def gabor_exposure(groups, frequency, period_fraction):
    groups_withexposure = []

    for current_group in groups:
        current_group = np.array(current_group)
        current_group_timenormalized = current_group[:, 0] - np.min(current_group[:, 0])
        current_group[:, 0] = current_group_timenormalized
        total_time = current_group_timenormalized[-1]

        period_length = period_fraction * total_time
        time = current_group_timenormalized

        # Time wrapped to the period
        t_mod = time % period_length

        # Center the window at period_length / 2 for symmetry
        t_centered = t_mod - (period_length / 2)

        # Define Gaussian width σ based on period length
        sigma = period_length / 6  # You can adjust the divisor to control width

        # Gabor function
        gaussian = np.exp(- (t_centered ** 2) / (2 * sigma ** 2))
        sinusoid = np.cos(2 * np.pi * frequency * t_centered / period_length)
        gabor = gaussian * sinusoid

        # Normalize to 0–1
        gabor_normalized = (gabor - np.min(gabor)) / (np.max(gabor) - np.min(gabor))

        # Apply weighting to 4th column
        currentgroup_withexposure = np.copy(current_group)
        currentgroup_withexposure[:, 3] = gabor_normalized * current_group[:, 3]

        groups_withexposure.append(currentgroup_withexposure)

    return groups_withexposure

def build_2D_frames(events_array, frequency, period_fraction, 
                    exposure_function, n_start_global=0):
    """
    Convert event-based data into stacked 2D frames with customizable exposure function.

    Parameters
    ----------
    events_array : np.ndarray
        Array of shape (n_events, 4) with [t, x, y, polarity].
    frequency : float
        Frames per second.
    period_fraction : int
        Fraction of the period for exposure calculation.
    exposure_function : str
        Type of exposure function ('on_off', 'triangle', 'sinusoidal').
    n_start_global : int
        Starting index for processing groups.

    Returns
    -------
    frames : np.ndarray
        Array of shape (n_frames, 480, 640), each 2D frame stacked.
    """
    
    frame_time = (1 / frequency) * 1e6
    groups = time_bins(frame_time, events_array)
    
    # Compute exposure frames using the chosen function
    groups_withexposure = exposure(
        groups[n_start_global:], 
        function=exposure_function, 
        period_fraction=period_fraction
    )
    
    # Build 2D frames
    frames = []
    for frame in groups_withexposure:
        example = frame[:, 1:4]  # columns x, y, polarity
        grid = np.zeros((480, 640))
        for i in range(example.shape[0]):
            x, y = example[i, 0:2].astype(int)
            grid[y, x] += example[i, 2]  # add polarity
        frames.append(grid)
    
    return np.array(frames)  # shape: (n_frames, 480, 640)