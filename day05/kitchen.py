import os
import re
import logging
from typing import List, Tuple

INPUT_FILE = "input.txt"
logging.basicConfig(level=logging.INFO)
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

def main_part1():
    fresh_list : List[int] = []
    initialize()
    for item in ingredients:
        if is_fresh(item):
            fresh_list.append(item)
    print(f"Fresh items: {len(fresh_list)}")


def main_part2():
    count: int = 0

    initialize()
    all_fresh: List[Tuple[int, int]] = []
    if len(map) == 0:
        print("Error")
    all_fresh.append(map[0])

    for (new_min, new_max) in map:
        logging.debug(f"Next Case: {new_min},{new_max}")
        logging.debug(f"all_fresh: {all_fresh}")
        for i, (existing_min, existing_max) in enumerate(all_fresh):
            logging.debug(f"Case: {new_min},{new_max}. Handling item: {i}: {existing_min}, {existing_max} with all_fresh.length:{len(all_fresh)}")
            logging.debug(f"all_fresh: {all_fresh}")
            
            # 6 cases (early/late, front/back, inside, over)
            if new_min > existing_max: #early
                logging.debug(f"Early")
                if i == len(all_fresh)-1:
                    logging.debug(f"No more ranges to check, adding")
                    all_fresh.append((new_min,new_max))
                    break
                continue
            elif new_max < existing_min: #late
                logging.debug(f"Late")
                all_fresh.insert(i,(new_min,new_max))
                break
            elif new_min >= existing_min and new_max <= existing_max:  #inside
                logging.debug(f"Inside")
                break
            elif new_min < existing_min and new_max > existing_max:  #outside
                logging.debug(f"Outside")
                #need to get other ranges involved
               
                while True:
                    if len(all_fresh) == i+1 or all_fresh[i+1][0] > new_max:
                        all_fresh[i] = (new_min, new_max)
                        break
                    elif all_fresh[i+1][1] >= new_max:
                        all_fresh[i] = (new_min, all_fresh[i+1][1])
                        all_fresh.pop(i+1)
                        break
                    else:
                        all_fresh.pop(i+1)  
                break

            elif new_min < existing_min and new_max <= existing_max: #front
                logging.debug(f"Front")
                all_fresh[i] = (new_min, existing_max)
                break
            elif new_min >= existing_min and new_max > existing_max: #back
                logging.debug(f"Back")
                #need to get other ranges involved
                while True:
                    if len(all_fresh) == i+1 or all_fresh[i+1][0] > new_max:
                        all_fresh[i] = (existing_min, new_max)
                        break
                    elif all_fresh[i+1][1] >= new_max:
                        all_fresh[i] = (existing_min, all_fresh[i+1][1])
                        all_fresh.pop(i+1)
                        break
                    else:
                        all_fresh.pop(i+1)
                break

            else:
                logging.critical("Case not handled. (early/late, front/back, inside, over) ")

    print(f"Final fresh list: {all_fresh}")

    for (min, max) in all_fresh:
        count += max-min+1
    
    print(f"Fresh items: {count}")
                


if __name__ == "__main__":
    main_part2()