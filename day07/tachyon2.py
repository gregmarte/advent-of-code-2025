import os
import logging

INPUT_FILE = "input.txt"
logging.basicConfig(level=logging.CRITICAL)

elem_empty:str = "."
elem_taychon:str = "1"
elem_splitter:str = "^"
elem_source:str = "S"

def main():
    count: int = 0              #num of times that reality exists/splits
    previous: list[str] = []    #The line above, i.e. tachyon rays in.
    next: list[str] = []        #The line being built. Starts with physical, and then modified with previous.
    
    file_name = os.path.join("day07/tests", INPUT_FILE)
    
    try:
        with open(file_name, 'r' ) as file:
            for line in file:

                if len(previous) == 0:
                    next = list(line.replace(elem_source,elem_taychon).strip())
                    count+=1 #one reality
                else:
                    next = list(line.strip())
                    for i, e in enumerate(next):
                        logging.debug(f"previous i says: {previous[i]}, I am int? {(previous[i]).isdigit()}")
                        
                        if previous[i].isdigit():    #if tachyon above.
                            taychon_intensity = previous[i] #read the intensity

                            #interacts with splitter
                            if e == elem_splitter:          
                                count+=int(taychon_intensity)
                                if i>0:
                                    if next[i-1] == elem_empty:
                                        next[i-1] = taychon_intensity
                                    elif next[i-1].isdigit():
                                        logging.debug(f"Lines joined. Increase intensity")
                                        next[i-1] = str(int(taychon_intensity)+int(next[i-1]))
                                    elif next[i-1] == elem_splitter:
                                        logging.critical("Unhandled case") 
                                    else:
                                        logging.critical("Unexpected data.")
                                else:
                                    count-=int(taychon_intensity)
                                if i < len(previous)-1:
                                    if next[i+1] == elem_empty:
                                        next[i+1] = taychon_intensity
                                    elif next[i+1].isdigit():
                                        logging.debug(f"Lines joined. Increase intensity")
                                        next[i+1] = str(int(taychon_intensity)+int(next[i+1]))
                                    elif next[i+1] == elem_splitter:
                                        logging.critical("Unhandled case") 
                                    else:
                                        logging.critical("Unexpected data.")
                                else:
                                    count-= int(taychon_intensity)
                            #OR, interacts with empty space, i.e. propogates
                            elif e == elem_empty:
                                next[i] = taychon_intensity

                            #OR, finds another taychon from a nearby splitter, i.e. amplifies
                            elif e.isdigit():
                                logging.debug(f"Lines joined. Increase intensity")
                                next[i] = str(int(taychon_intensity)+int(next[i]))

                previous = next
                logging.info(f"{next}")

    except Exception as e:
        print(f"❌ An error occurred during file processing: {e}")

    print(f"Count, realities: {count}")

if __name__ == "__main__":
    main()