import numpy as np

def compute_distance(landmark1, landmark2):
    """Compute screen-space distance between two pose landmarks."""
    return np.sqrt((landmark1.x - landmark2.x) ** 2 + (landmark1.y - landmark2.y) ** 2)
