import os
import logging
import re

from typing import Set

logging.basicConfig(level=logging.INFO)

#There are 1000 red tiles.
#Let map[(x,y)] be my points
#where x_map(x)= is the furthest x point used. 
x_map:list[int] = []
y_map:list[int] = []

red_tiles: list[tuple[int,int]] = []    #x_map,y_map coordinates
areas: list[tuple[int, tuple[int,int], tuple[int,int]]] = []  #area, point1, point2

map_size:int
map: dict[tuple[int, int], bool] 

TEST_FILENAME = 'input.txt'

def initialize(file_name:str):
    global red_tiles, map, map_size, x_map, y_map
    set_x: Set[int] = set()
    set_y: Set[int] = set()
   
    file_location = os.path.join("day09", "tests", file_name)
    
    counter:int = 0
    with open(file_location, 'r') as file:
        for line in file:
            pattern = r"(\d+),(\d+)"
            match = re.match(pattern, line)

            if match:
                red_tiles.append((int(match.group(1)), int(match.group(2))))
                counter+=1
    
    map_size = counter+2 #+2 for a boundary/border, to support filling from outside area.
    
    set_x.add(-1)
    set_y.add(-1)
    for (my_x,my_y) in red_tiles:
        set_x.add(my_x)
        set_x.add(my_x+1)
        set_y.add(my_y)
        set_y.add(my_y+1)
    set_x.add(map_size)
    set_y.add(map_size)

    x_map = sorted(set_x)
    y_map = sorted(set_y)

    map = {
        (x, y): True
        for x in range(map_size)
        for y in range(map_size)
    }

    logging.debug(f"Points:\n{red_tiles}")
    logging.debug(f"\nx_map: {x_map}\ny_map:{y_map}")
    
    
def print_map():
    #testing 
    if map_size < 25:
        for x in range(0, len(x_map)):
            for y in range(0, len(y_map)):
                print(f"{int(map[x,y])}", end="")
            print("")

def build_map(paths_as:bool):
    iter=0

    for tile1,tile2 in zip(red_tiles, red_tiles[1:] + red_tiles[:1]):

        iter+=1
        x1,y1 = tile1
        x2,y2 = tile2

        x1_t = x_map.index(x1)
        y1_t = y_map.index(y1)
        x2_t = x_map.index(x2)
        y2_t = y_map.index(y2)
        logging.debug(f"Transforms: {x1_t},{y1_t}, {x2_t}, {y2_t}")

        
        row_min = min(x1_t, x2_t)
        row_max = max(x1_t, x2_t)
        col_min = min(y1_t,y2_t)
        col_max = max(y1_t,y2_t)
        logging.debug(f"Map: {row_min},{row_max}, {col_min}, {col_max}")

        for x in range(row_min, row_max + 1):
            for y in range(col_min, col_max + 1):
                logging.debug(f"Adding: {x},{y}, for {tile1} to {tile2}")
                map[(x,y)] = paths_as

        logging.debug(f"i:{iter}, adding {tile1} to {tile2}")

        print_map()

def fill_map():
   
    to_check = [(0,0)] #begin 'water fill' pattern at border. Note: find a better way.
    iterations = 0

    while len(to_check) > 0 and iterations < map_size * map_size * 4:
        iterations+=1
        (x,y) = to_check.pop()
        if iterations%100 == 0:
            logging.debug(f"x: {x}, y:{y}, i:{iterations}")
        if map[x,y] == True:
            map[x,y] = False
            if (x > 0):
                to_check.append((x-1,y))
            if (x < map_size - 1):
                to_check.append((x+1,y))
            if (y > 0):
                to_check.append((x, y-1))
            if (y < map_size - 1):
                to_check.append((x,y+1))

    print_map()

    return

def calculate():
    global areas
    for i in range(0, len(red_tiles)):
        for j in range(i+1,len(red_tiles)):
            x1,y1 = red_tiles[i]
            x2,y2 = red_tiles[j]

            area = (abs(x1-x2)+1)*(abs(y1-y2)+1)
            areas.append((area, red_tiles[i], red_tiles[j]))

    areas.sort(key=lambda x: x[0], reverse=False) #smallest is at front, .pop() to get largest.

    #now find the largest one where everything inside is true.
    iter=0

    while len(areas) > 0 or iter > 1000:
        iter+=1
        area,i,j = areas.pop() 

        row_min = min(i[0], j[0]) 
        row_max = max(i[0], j[0]) 
        col_min = min(i[1], j[1]) 
        col_max = max(i[1], j[1]) 

        #transform
        row_min_t = x_map.index(row_min)
        row_max_t = x_map.index(row_max)
        col_min_t = y_map.index(col_min)
        col_max_t = y_map.index(col_max)

        all_are_true = all(
            map[(x, y)]
            for x in range(row_min_t, row_max_t)  
            for y in range(col_min_t, col_max_t) 
        )

        if all_are_true:
            logging.info(f"Area found. area: {area}, p1: {i}, p2: {j}")
            return int(area)

    raise Exception("item not found in Areas")
    

def main():
    initialize(TEST_FILENAME)
    build_map(paths_as=False)
    fill_map()
    build_map(paths_as=True)
    calculate()
    
    return

if __name__ == "__main__":
    main()