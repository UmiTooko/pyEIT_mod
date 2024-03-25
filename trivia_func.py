import numpy as np


def amplify_normal_distribution(x, mean, std_dev, start, finish):
    distance_from_mean = np.abs(x - mean)
    amplification_factor = np.clip(1 + distance_from_mean * distance_from_mean / std_dev, start, finish)  # Clip to ensure values stay within desired range
    amplified_value = x * amplification_factor
    return amplified_value