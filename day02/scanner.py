import os
import re
import logging

logging.basicConfig(level=logging.INFO)
INPUT_FILE = "input.txt"

def invalid_logic_case1(x:int):
    if len(str(x)) % 2 == 1:
        return 0
    my_segment:int = (len(str(x)) // 2)
    pattern2 = rf"(\d{{{my_segment}}})(\d{{{my_segment}}})"
    match2 = re.match(pattern2, str(x))
    
    if match2:
        first_half = int(match2.group(1))
        second_half = int(match2.group(2))
        if first_half == second_half:
            print(f"Invalid id found: {x}")
            return x
    return 0

def invalid_logic_case2(x:int):
    max_pattern_length:int = len(str(x)) // 2
    
    for p in range(max_pattern_length,0,-1):
        logging.debug(f"max_pattern: {max_pattern_length}, p: {p}")
        if len(str(x)) % p != 0:
            logging.debug(f"next please. x: {x}, p: {p}")
            continue

        logging.debug(f"a) {x}, b) {str(x)[0]}, c) {str(x)[1]}")

        values = [str(x)[i:i+p] for i in range(0, len(str(x)), p)]
        logging.debug(f"values: {values}, p: {p}")
        sameness:bool = True

        for v in values:
            logging.debug(f"v: {v}, values[0]: {values[0]}")
            if values[0] != v:
                sameness = False
                break

        if sameness:
            logging.info(f"invalid id found: {x}")
            return x

    return 0

def process_file(file_path:str):
    """
    Reads a scanner id file, and outputs the number of times repeats within those ranges
    
    :param file_name: text file, ###-###,###-####
    """
    if not os.path.exists(file_path):
        print(f"🛑 Error: The required file '{file_path}' was **not found** in the current directory.")
        exit(0)

    print(f"📁 Starting to process file: **{file_path}**\n")
    
    try:
        summation:int = 0

        with open(file_path, 'r') as file:
            for line in file:
                items = line.strip().split(',')
                for item in items:
                    pattern = r"(\d+)-(\d+)"

                    match = re.match(pattern, item)
        
                    if match:
                        range_start = int(match.group(1))
                        range_stop = int(match.group(2)) 
                        
                        for x in range(range_start, range_stop+1,1):
                            #summation+=invalid_logic_case1(x)
                            summation+=invalid_logic_case2(x)
                                
        print("\n✅ File processing complete.")
        return summation
        
    except Exception as e:
        print(f"❌ An error occurred during file processing: {e}")


if __name__ == "__main__":

    file_path = os.path.join("day02/tests", INPUT_FILE)
  
    print(f"The combination is: '{process_file(file_path)}. Sum of invalid ids.")
