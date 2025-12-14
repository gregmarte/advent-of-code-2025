import os
import logging
import numpy as np
from numpy.typing import NDArray
from scipy.spatial import cKDTree

junction_locations: NDArray[np.int_]
circuits:list[list[int]] = []

logging.basicConfig(level=logging.DEBUG)
tree = None

def initialize(file_name:str):
    global tree
    global junction_locations
    file_location = os.path.join("tests", file_name)
    junction_locations = np.loadtxt(file_location, dtype=int, delimiter=",")
    logging.debug(f"Points:\n{junction_locations}")

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

def calculate(wires:int):
    if tree == None:
        raise Exception("Map not loaded.")
    else:
        pairs_with_indices = tree.query_pairs(r=np.inf)

    custom_dtype = np.dtype([
        ('dist', np.float64), 
        ('p1', np.int64), 
        ('p2', np.int64)
    ])

    #Test Version. data_set = np.empty(0, dtype=custom_dtype)
    data_set = np.zeros(499_500, dtype=custom_dtype)

    counter:int = 0
    for i, j in pairs_with_indices:
                   
        # Calculate the Euclidean distance between points i and j
        distance = np.linalg.norm(junction_locations[i] - junction_locations[j])
        
        #Test Version
        # new_row = np.array([(distance, i, j)], dtype=custom_dtype)
        # data_set = np.append(data_set, new_row)
        data_set[counter] = (distance, i, j)
        counter+=1
        logging.debug(f"counter: {counter}, actioning: {i}, {j}")

    sorted_data_set = np.sort(data_set, order='dist')

    #build circuits with this data
    for k in range(0,wires):
        logging.debug(f"Connecting: {sorted_data_set[k]}")
        connect(sorted_data_set[k]["p1"], sorted_data_set[k]["p2"])

    logging.debug(f"Circuits\n{circuits}")
   
    #3 largest
    sorted_descending = sorted(circuits, key=len, reverse=True)
    logging.debug(f"Sorted:\n{sorted_descending}")
    
    print(f"Magic answer: ({len(sorted_descending[0])} * {len(sorted_descending[1])} * {len(sorted_descending[2])})")
    print(f"Magic answer: {len(sorted_descending[0]) * len(sorted_descending[1]) * len(sorted_descending[2])}")
def main():
    initialize("input.txt")
    calculate(1000)
    return


if __name__ == "__main__":
    main()