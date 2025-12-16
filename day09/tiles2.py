import os
import logging
import re
import numpy as np
import h5py

logging.basicConfig(level=logging.DEBUG)

red_tiles: list[tuple[int,int]] = []        #x,y coordinates
areas: list[tuple[int, int, int]] = []  #area, point1, point2

map_size:int = 100000
non_prod:bool = False
MY_MAP = "large_map"
TEST_FILENAME = 'input.txt'

def initialize(file_name:str, map_name:str):
    global red_tiles
    global min_x, min_y, max_x, max_y
   
    file_location = os.path.join("day09", "tests", file_name)
    
    with open(file_location, 'r') as file:
        for line in file:
            pattern = r"(\d+),(\d+)"
            match = re.match(pattern, line)

            if match:
                red_tiles.append((int(match.group(1)), int(match.group(2))))

    with h5py.File(map_name+'.hdf5', 'w') as f:
    
        f.create_dataset(
            map_name,
            shape=(map_size, map_size), 
            dtype=np.bool_,
            fillvalue=True  
        )

    logging.debug(f"Points:\n{red_tiles}")
    
    #Type checking
    # with h5py.File(largemap+'.hdf5', 'r+') as f:
    #     # Retrieve the dataset object
    #     map_dataset = f[map_name]
        
    #     slice_region = np.s_[50, 60:71]
        
    #     map_dataset[slice_region] = True   # pyright: ignore, see README.md
    #     #logging.debug(f"true?: map_dataset {map_dataset[(50,65)]}, false?: {map_dataset[5,5]}") 

    

def build_map(map_name:str, paths_as:bool):

    with h5py.File(map_name+'.hdf5', 'r+') as f:
        map_dataset = f[map_name]

        iter=0

        for tile1,tile2 in zip(red_tiles[:-1] , red_tiles[1:]):
            iter+=1
            row_min = min(tile1[0], tile2[0])
            row_max = max(tile1[0], tile2[0])
            col_min = min(tile1[1], tile2[1])
            col_max = max(tile1[1], tile2[1])

            row_slice = slice(row_min, row_max + 1)
            col_slice = slice(col_min, col_max + 1)

            slice_region = np.s_[row_slice, col_slice]
            map_dataset[slice_region] = paths_as
            logging.debug(f"i:{iter}, adding {tile1} and {tile2}")

        #testing 
        if non_prod and map_size == 10:
            full_map_array = f[map_name][()] # pyright: ignore[reportUnknownVariableType], see README.md
            logging.debug(full_map_array.astype(int)) # pyright: ignore[reportUnknownArgumentType, reportAttributeAccessIssue, reportUnknownMemberType]

    return
def fill_map(map_name:str):
    with h5py.File(map_name+'.hdf5', 'r+') as f:
        map_dataset = f[map_name]

        to_check = [(0,0)]
        iterations = 0

        while len(to_check) > 0 and iterations < map_size * map_size * 4:
            iterations+=1
            (x,y) = to_check.pop()
            logging.debug(f"x: {x}, y:{y}, i:{iterations}")
            if map_dataset[x,y] == True:
                map_dataset[x,y] = False
                if (x > 0):
                    to_check.append((x-1,y))
                if (x < map_size - 1):
                    to_check.append((x+1,y))
                if (y > 0):
                    to_check.append((x, y-1))
                if (y < map_size - 1):
                    to_check.append((x,y+1))
    
        #testing 
        if non_prod and map_size == 10:
            full_map_array = f[map_name][()] # pyright: ignore[reportUnknownVariableType], see README.md
            logging.debug(full_map_array.astype(int)) # pyright: ignore[reportUnknownArgumentType, reportAttributeAccessIssue, reportUnknownMemberType]

    return

def calculate(map_name:str):
    global areas
    for i in range(0, len(red_tiles)):
        for j in range(i+1,len(red_tiles)):
            x1,y1 = red_tiles[i]
            x2,y2 = red_tiles[j]

            area = (abs(x1-x2)+1)*(abs(y1-y2)+1)
            areas.append((area, i, j))

    areas.sort(key=lambda x: x[0], reverse=False) #smallest is at front, .pop() to get largest.

    #now find the largest one where everything inside is true.
    with h5py.File(map_name+'.hdf5', 'r+') as f:
        map_dataset = f[map_name]
        iter=0

        while len(areas) > 0 or iter > 1000:
            iter+=1
            dist,i,j = areas.pop() # type: ignore

            row_min = min(red_tiles[i][0], red_tiles[j][0]) # type: ignore
            row_max = max(red_tiles[i][0], red_tiles[j][0]) # type: ignore
            col_min = min(red_tiles[i][1], red_tiles[j][1]) # type: ignore
            col_max = max(red_tiles[i][1], red_tiles[j][1]) # type: ignore

            row_slice = slice(row_min, row_max + 1)
            col_slice = slice(col_min, col_max + 1)

            slice_region = np.s_[row_slice, col_slice]
            if np.all(map_dataset[slice_region]): # type: ignore
                logging.info(f"Area found. area: {dist}, p1: {red_tiles[i]}, p2: {red_tiles[j]}")
                return int(dist)

    raise Exception("item not found in Areas")
    

def main():
    global non_prod, map_size

    non_prod = False #False
    map_size = 100000   #100000    

    initialize(TEST_FILENAME, MY_MAP)
    build_map(MY_MAP,paths_as=False)
    fill_map(MY_MAP)
    build_map(MY_MAP,paths_as=True)
    calculate(MY_MAP)
    
    return

if __name__ == "__main__":
    main()