import numpy as np

def compute_distance(landmark1, landmark2):
    return np.sqrt((landmark1.x-landmark2.x)**2 + (landmark1.y-landmark2.y)**2 + (landmark1.z - landmark2.z)**2)

# New helper function signatures

def normalize_landmarks(landmarks):
    """Normalize the landmarks to a standard scale."""
    pass

def calculate_angle(landmark1, landmark2, landmark3):
    """Calculate the angle formed by three landmarks."""
    pass

def filter_landmarks(landmarks, threshold):
    """Filter out landmarks that do not meet a certain threshold."""
    pass

def transform_landmarks(landmarks, transformation_matrix):
    """Apply a transformation matrix to the landmarks."""
    pass

def compute_centroid(landmarks):
    """Compute the centroid of a set of landmarks."""
    pass
