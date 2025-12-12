import os
import logging
import numpy as np
from typing import List
from numpy.typing import NDArray

INPUT_FILE = "input.txt"
logging.basicConfig(level=logging.DEBUG)

data_array: NDArray[np.int64]
operators_list: List[str] = []
operators:str

def lines_excluding_last(file_path:str):
     with open(file_path, 'r' ) as file:
            global operators
            previous_line = file.readline()

            if previous_line:
                for current_line in file:
                    yield previous_line
                    previous_line = current_line
                operators = current_line # pyright: ignore[reportPossiblyUnboundVariable]

def initialize():
    global data_array
    global operators_list
    file_path = os.path.join("day06/tests", INPUT_FILE)

    try:
        data_array = np.loadtxt(lines_excluding_last(file_path),dtype=int)
        #data_array = data_array.T
        operators_list = operators.split()
        logging.debug(f"Data Array")
        logging.debug(f"{data_array}")
        logging.debug(f"Operators")
        logging.debug(f"{operators_list}")

    except Exception as e:
        print(f"❌ An error occurred during file processing: {e}")




def main1():
    summation:int = 0
    initialize()
    temp_prod: NDArray[np.int64] = data_array.prod(axis=0) 
    temp_sum: NDArray[np.int64] = data_array.sum(axis=0)

    for i, o in enumerate(operators_list):
        if o == "+":
            logging.debug(f"column gives: {temp_sum[i]}")
            summation+=temp_sum[i]
        elif o == "*":
            logging.debug(f"column gives: {temp_prod[i]}")
            summation+=temp_prod[i]
        else:
            raise Exception("Unknown operator. Only know: *,+")
        
    print(f"Math homework complete: {summation}")
    return

if __name__ == "__main__":
    main1()