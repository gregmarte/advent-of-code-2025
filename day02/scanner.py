import os
import re

INPUT_FILE = "input.txt"

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
                            if len(str(x)) % 2 == 1:
                                continue
                            my_segment:int = (len(str(x)) // 2)
                            pattern2 = rf"(\d{{{my_segment}}})(\d{{{my_segment}}})"
                            match2 = re.match(pattern2, str(x))
                            
                            if match2:
                                first_half = int(match2.group(1))
                                second_half = int(match2.group(2))
                                if first_half == second_half:
                                    print(f"Invalid id found: {x}")
                                    summation+=x
                                
        print("\n✅ File processing complete.")
        return summation
        
    except Exception as e:
        print(f"❌ An error occurred during file processing: {e}")


if __name__ == "__main__":

    file_path = os.path.join("day02/tests", INPUT_FILE)
  
    print(f"The combination is: '{process_file(file_path)}. Sum of invalid ids.")
