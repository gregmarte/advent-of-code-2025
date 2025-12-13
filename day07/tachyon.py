import os
import logging

INPUT_FILE = "input.txt"
logging.basicConfig(level=logging.INFO)

elem_empty:str = "."
elem_light:str = "|"
elem_splitter:str = "^"
elem_source:str = "S"

def main():
    count: int = 0
    previous: list[str] = []
    next: list[str] = []
    

    file_name = os.path.join("day07/tests", INPUT_FILE)
    
    try:
        with open(file_name, 'r' ) as file:
            for line in file:

                if len(previous) == 0:
                    next = list(line.replace(elem_source,elem_light).strip())
                else:
                    next = list(line.strip())
                    for i, e in enumerate(next):
                        if previous[i] == elem_light: 
                            if e == elem_splitter:
                                count+=1
                                if i>0:
                                    if next[i-1] == elem_empty:
                                        next[i-1] = elem_light
                                    elif next[i-1] == elem_light:
                                       logging.debug(f"Lines joined. No action")
                                    elif next[i-1] == elem_splitter:
                                        logging.critical("Unhandled case") 
                                    else:
                                        logging.critical("Unexpected data.")
                                if i < len(previous)-1:
                                    if next[i+1] == elem_empty:
                                        next[i+1] = elem_light
                                    elif next[i+1] == elem_light:
                                       logging.debug(f"Lines joined. No action")
                                    elif next[i+1] == elem_splitter:
                                        logging.critical("Unhandled case") 
                                    else:
                                        logging.critical("Unexpected data.")
                            elif e == elem_empty:
                                next[i] = elem_light
                            elif e == elem_light:
                                logging.debug(f"Lines joined. No action")

                previous = next
                logging.info(f"{next}")

    except Exception as e:
        print(f"❌ An error occurred during file processing: {e}")

    print(f"Count, spliters: {count}")

if __name__ == "__main__":
    main()