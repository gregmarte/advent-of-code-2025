import os
import logging

INPUT_FILE = "input.txt"
logging.basicConfig(level=logging.INFO)

def joltage2(n:int):
    first:int = int(str(n)[0])
    second:int = int((str(n))[1])
     
    for c in str(n)[2:]:
        if second > first:
            first = second
            second = int(c)
        if int(c) > second:
            second = int(c)
    
    logging.info(f"Battery value: {first}{second}")
  
    return int(str(first) + str(second))

def joltage12(n:int):
    Digits:int = 12
    solution = [(str)(n)[i] for i in range(0, Digits)]

    for c in str(n)[Digits:]:
        for p in range (0,Digits-1):   
            if solution[p+1] > solution[p]:
                for r in range (p, Digits-1):
                    solution[r] = solution[r+1]
                solution[Digits-1] = c
                break

        if c > solution[Digits-1]:
            solution[Digits-1] = c

    answer = "".join(solution)         
    logging.info(f"Battery value: {answer}")
  
    return int(answer)



def process_file(file_path:str):
    """
    Reads a scanner id file, and outputs the number of times repeats within those ranges
    
    :param file_name: text file, ############
    """
    if not os.path.exists(file_path):
        print(f"🛑 Error: The required file '{file_path}' was **not found** in the current directory.")
        exit(0)

    print(f"📁 Starting to process file: **{file_path}**\n")
    
    try:
        summation:int = 0

        with open(file_path, 'r') as file:
            for line in file:
                summation+=joltage12(int(line))
                                
        print("\n✅ File processing complete.")
        return summation
        
    except Exception as e:
        print(f"❌ An error occurred during file processing: {e}")

if __name__ == "__main__":

    file_path = os.path.join("day03/tests", INPUT_FILE)
  
    print(f"The joltage is: '{process_file(file_path)}. Merry Christmas!")