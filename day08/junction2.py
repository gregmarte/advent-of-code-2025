import os
import logging
import numpy as np
from numpy.typing import NDArray
from scipy.spatial import cKDTree

junction_locations: NDArray[np.int_]
circuits:list[list[int]] = []
num_items:int = 0

logging.basicConfig(level=logging.DEBUG)
tree = None

def initialize(file_name:str):
    global tree
    global junction_locations
    global num_items
    file_location = os.path.join("tests", file_name)
    junction_locations = np.loadtxt(file_location, dtype=int, delimiter=",")
    num_items = len(junction_locations)

    logging.debug(f"Points:\n{junction_locations}")
    logging.debug(f"Number of items: {num_items}")

    tree = cKDTree(junction_locations)

def connect(i:int, j:int):
    global circuits
    circuitI:int = -1 #undefined
    circuitJ:int = -1 #undefined
    lastWasI:bool = True
    logging.debug(f"Calling connect on: {i},{j}")

    for index, circuit in enumerate(circuits):
        if i in circuit:
            circuitI = index
            lastWasI = True
        if j in circuit:
            circuitJ = index
            lastWasI = False

    if circuitI == -1 and circuitJ == -1:
        #no match found, add new circuit
        circuits.append([i,j])
        logging.debug(f"added new circuit. [{i},{j}]")
    elif circuitI != -1 and circuitJ != -1:
        if circuitI != circuitJ:
            if lastWasI:
                circuits.append(circuits.pop(circuitI) + circuits.pop(circuitJ))
            else:
                circuits.append(circuits.pop(circuitJ) + circuits.pop(circuitI))
            logging.debug(f"merged circuits for. [{i},{j}]")
        else:
            logging.debug(f"already in the same circuit. Wasted wire.")
    elif circuitI != -1:
        circuits[circuitI].append(j)
        logging.debug(f"added i,j to circuit: {circuitI}")
    elif circuitJ != -1:
        circuits[circuitJ].append(i)
        logging.debug(f"added i,j to circuit: {circuitJ}")
    else:
        logging.critical("Case not handled. fn:connect")
    return

def calculate():
    if tree == None:
        raise Exception("Map not loaded.")
    else:
        pairs_with_indices = tree.query_pairs(r=np.inf)

    custom_dtype = np.dtype([
        ('dist', np.float64), 
        ('p1', np.int64), 
        ('p2', np.int64)
    ])

    n_pairs = (num_items * (num_items - 1)) // 2
    data_set = np.zeros(n_pairs, dtype=custom_dtype)

    counter:int = 0
    for i, j in pairs_with_indices:
                   
        # Calculate the Euclidean distance between points i and j
        distance = np.linalg.norm(junction_locations[i] - junction_locations[j])
        
        data_set[counter] = (distance, i, j)
        counter+=1
        logging.debug(f"counter: {counter}, actioning: {i}, {j}")

    sorted_data_set = np.sort(data_set, order='dist')

    #build until all one
    k:int = 0
    while True:
        logging.debug(f"Connecting: {sorted_data_set[k]}")
        connect(sorted_data_set[k]["p1"], sorted_data_set[k]["p2"])
        if len(circuits[0]) >= num_items:
            logging.debug("all is one circuit")
            print(f"Last items were: {junction_locations[sorted_data_set[k]['p1']]} and {junction_locations[sorted_data_set[k]['p2']]}")
            print(f"Magic answer is: {junction_locations[sorted_data_set[k]['p1']][0] * junction_locations[sorted_data_set[k]['p2']][0] }")
            break
        if k > num_items * num_items:
            raise Exception("Solution not found")
        k+=1

def main():
    initialize("input.txt")
    calculate()
    return

if __name__ == "__main__":
    main()