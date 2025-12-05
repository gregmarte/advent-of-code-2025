import os
import re

INPUT_FILE = "input.txt"

def process_file(file_path:str):
    """
    Reads a movement file, and outputs the number of times that 0 is touched/entered.
    
    :param file_name: Movement text file, L32\nR450\nR23
    """
    if not os.path.exists(file_path):
        print(f"🛑 Error: The required file '{file_path}' was **not found** in the current directory.")
        exit(0)

    print(f"📁 Starting to process file: **{file_path}**\n")
    
    try:
        number_of_zeros:int = 0
        lock_points_to:int = 50

        with open(file_path, 'r') as file:
            
            for line in file:
                pattern = r"(\D)(\d+)"

                match = re.match(pattern, line)
    
                if match:
                    char_result = match.group(1)
                    int_result = int(match.group(2)) 
                    
                    direction:int = -1 if (char_result == 'L') else 1
                    touch_start:bool = True if lock_points_to == 0 else False
                    lock_points_to = (lock_points_to + (direction * int_result)) 

                    if lock_points_to == 0:
                        number_of_zeros+=1
                
                    while lock_points_to < 0:
                        number_of_zeros+=1
                        lock_points_to+=100
                        if touch_start:
                            number_of_zeros-=1
                            touch_start = False
                        if lock_points_to == 0:
                            number_of_zeros+=1
                    while lock_points_to > 99:
                        number_of_zeros+=1
                        lock_points_to-=100


                    print(f"R: {line.strip()}. C: {number_of_zeros}. N: {lock_points_to}.")

                else:
                    print(f"\nParsing '{line}'...")
                    print("No match found for the expected format.")
                    break
                                
        print("\n✅ File processing complete.")
        return number_of_zeros
        
    except Exception as e:
        print(f"❌ An error occurred during file processing: {e}")


def process_file_first_case(file_path:str):
    if not os.path.exists(file_path):
        print(f"🛑 Error: The required file '{file_path}' was **not found** in the current directory.")
        exit(0)

    print(f"📁 Starting to process file: **{file_path}**\n")
    
    try:
        number_of_zeros:int = 0
        lock_points_to:int = 50

        with open(file_path, 'r') as file:
            
            for line in file:
                pattern = r"(\D)(\d+)"

                match = re.match(pattern, line)
    
                if match:
                    char_result = match.group(1)
                    int_result = int(match.group(2)) 
                    
                    direction:int = -1 if (char_result == 'L') else 1
                    step_size = int_result % 100

                    lock_points_to = (lock_points_to + (direction * step_size)) % 100

                    print(f"Lock points to: {lock_points_to}")
                    if lock_points_to == 0:
                        number_of_zeros+=1
                    if lock_points_to < 0:
                        lock_points_to+=100

                else:
                    print(f"\nParsing '{line}'...")
                    print("No match found for the expected format.")
                    break
                                
        print("\n✅ File processing complete.")
        return number_of_zeros
        
    except Exception as e:
        print(f"❌ An error occurred during file processing: {e}")

if __name__ == "__main__":

    file_path = os.path.join("day01", INPUT_FILE)
  
    print(f"The combination is: '{process_file(file_path)}. Merry Christmas!")
