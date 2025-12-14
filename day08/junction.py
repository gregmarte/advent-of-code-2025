import os
import logging
import numpy as np
from numpy.typing import NDArray
from scipy.spatial import cKDTree

junction_locations: NDArray[np.int_]

INPUT_FILE = "test01.txt"
logging.basicConfig(level=logging.DEBUG)

file_location = os.path.join("day08/tests", INPUT_FILE)

def initialize():
    junction_locations = np.loadtxt(file_location, dtype=int, delimiter=",")
    logging.debug(f"Points:\n{junction_locations}")

    tree = cKDTree(junction_locations)

    pairs_with_indices = tree.query_pairs(r=np.inf)

    min_distance = np.inf
    closest_pair_indices = None

    for i, j in pairs_with_indices:
        # Calculate the Euclidean distance between points i and j
        distance = np.linalg.norm(junction_locations[i] - junction_locations[j])
        
        if distance < min_distance:
            min_distance = distance
            closest_pair_indices = (i, j)

    if closest_pair_indices == None:
        logging.critical("No pair found")
    else:
        i,j = closest_pair_indices

        print(f"Closest distance found: {min_distance:.4f}")
        print(f"Indices of the closest pair: {closest_pair_indices}")
        print(f"Point {i}: {junction_locations[i]}")
        print(f"Point {j}: {junction_locations[j]}")
        

def main():
    initialize()
    return


if __name__ == "__main__":
    main()