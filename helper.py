import numpy as np

def compute_distance(landmark1, landmark2):
    """Compute normalized 3D distance between two pose landmarks."""
    raw_distance = np.sqrt((landmark1.x - landmark2.x) ** 2 + (landmark1.y - landmark2.y) ** 2 + (landmark1.z - landmark2.z) ** 2)
    return round(raw_distance, 4)
