import os
import logging

INPUT_FILE = "input.txt"
logging.basicConfig(level=logging.CRITICAL)

map = []
x_map_size = 0
y_map_size = 0

def initialize_map(file_name:str):
    global map
    global x_map_size,y_map_size

    try:
        with open(file_name, 'r' ) as file:
            map = file.readlines()
            y_map_size = len(map)
            x_map_size = len(map[0].strip())

            logging.debug(f"max x: {x_map_size}, max y: {y_map_size}")

    except Exception as e:
        print(f"❌ An error occurred during file processing: {e}")
    

def neighbours_with_char(point_x:int, point_y:int, c:str):
    count:int = 0
    for x in range (point_x-1, point_x+2):
        if x > -1 and x < x_map_size:
            for y in range (point_y-1, point_y+2):
                if y > -1 and y < y_map_size:
                    if point_x==x and point_y==y:
                        continue
                    if map[y][x] == c:
                        logging.debug(f"neighbour found for {point_x},{point_y} at {x},{y}")
                        count+=1
    logging.debug(f"total neighbours: for {point_x},{point_y} is {count}")
    return count

def has_roll(x:int, y:int) -> bool:
    logging.debug(f"x: {x}, y: {y} roll: {map[y][x] == '@'}")
    return (map[y][x] == "@")

def update_map(x:int, y:int, char:str):
    global map
    line_list = list(map[y])
    line_list[x] = char
    map[y] = "".join(line_list)
    logging.info(f"Removed: {x},{y}")

def main():
    file_path = os.path.join("day04/tests", INPUT_FILE)
    initialize_map(file_path)

    summation:int = 0
    prev_summation:int = -1

    while prev_summation != summation:
        prev_summation = summation
        for x in range(0, x_map_size):
            for y in range(0, y_map_size):
                if has_roll(x,y):
                    if neighbours_with_char(x,y,"@") < 4:
                        #Note: real-time update is going to give different order than sample.
                        update_map(x,y,"x")
                        summation+=1
        
    print(f"The number of available rolls is: '{summation}. Good luck getting to the cafeteria!")


if __name__ == "__main__":
    main()
