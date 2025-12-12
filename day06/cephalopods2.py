import os
import logging
import math
from typing import List

INPUT_FILE = "input.txt"
logging.basicConfig(level=logging.DEBUG)

data_array: List[List[int]] = []
operators_list: List[str] = []
operators:str

def lines_excluding_last(file_path:str):
     with open(file_path, 'r' ) as file:
            global operators
            previous_line = file.readline()

            if previous_line:
                for current_line in file:
                    yield list(previous_line.replace(' ', "x").replace('\n', "x"))
                    previous_line = current_line
                operators = current_line # pyright: ignore[reportPossiblyUnboundVariable]


def initialize():
   
    global operators_list
    global data_array
    data_temp: List[List[str]] = []
    file_path = os.path.join("day06/tests", INPUT_FILE)

    try:
        data_stream = lines_excluding_last(file_path)
        for row in data_stream:
            data_temp.append(row)
        
        transposed_matrix = list(zip(*data_temp))
        data_temp = [list(row) for row in transposed_matrix]

        value_to_remove = 'x'
        data_temp = [
            [item for item in inner_list if item != value_to_remove]
            for inner_list in data_temp
            ]

        concat_data_temp = [
            [int("".join(map(str, inner_list)))] 
            if inner_list else 
            []                                    
            for inner_list in data_temp
        ]

        current_group: List[int] = []

        for item_list in concat_data_temp:
            if item_list:
                current_group.extend(item_list)
            else:
                if current_group:
                    data_array.append(current_group)
                current_group = []

        if current_group:
            data_array.append(current_group)

        operators_list = operators.split()
        logging.debug(f"Data Array")
        logging.debug(f"{data_array}")
        logging.debug(f"Operators")
        logging.debug(f"{operators_list}")

    except Exception as e:
        print(f"❌ An error occurred during file processing: {e}")

def main():
    summation:int = 0
    initialize()

    for i, o in enumerate(operators_list):
        if o == "+":
            temp:int = sum(data_array[i]) 
            logging.debug(f"column gives: {temp}")
            summation+=temp
        elif o == "*":
            temp = math.prod(data_array[i])
            logging.debug(f"column gives: {temp}")
            summation+=temp
        else:
            raise Exception("Unknown operator. Only know: *,+")
        
    print(f"Math homework complete: {summation}")
    return



if __name__ == "__main__":
    main()