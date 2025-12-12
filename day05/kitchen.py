import os
import re
import logging
from typing import List, Tuple

INPUT_FILE = "input.txt"
logging.basicConfig(level=logging.CRITICAL)
map: List[Tuple[int, int]] = []
ingredients: List[int] = []

def initialize():
    global map,ingredients
    file_path = os.path.join("day05/tests", INPUT_FILE)

    try:
        with open(file_path, 'r' ) as file:
            section:int = 1

            for line in file:
                if not line.strip():
                    section+=1
                    continue

                if section == 1:
                    pattern = r"(\d+)-(\d+)"
                    match = re.match(pattern, line.strip())
                    if match:
                        min=int(match.group(1))
                        max=int(match.group(2))
                        map.append((min,max))
                    else:
                        raise Exception("Error in parsing the file. Section1")
                
                elif section == 2:
                    pattern = r"(\d+)"
                    match2 = re.match(pattern, line.strip())
                    if match2:
                        num=int(match2.group(1))
                        ingredients.append(num)
                    else:
                        raise Exception("Error in parsing the file. Section2")

                else: 
                    raise Exception("Error in parsing the file")

    except Exception as e:
        print(f"❌ An error occurred during file processing: {e}")


def is_fresh(item:int) -> bool:
    for (min,max) in map:
        if item >= min and item <= max:
            logging.info(f"Fresh item found: {item}")
            return True
    return False

def main():
    fresh_list : List[int] = []
    initialize()
    for item in ingredients:
        if is_fresh(item):
            fresh_list.append(item)
    print(f"Fresh items: {len(fresh_list)}")


if __name__ == "__main__":
    main()