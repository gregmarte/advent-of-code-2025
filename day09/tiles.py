import os
import logging
import re

logging.basicConfig(level=logging.DEBUG)

tiles: list[tuple[int,int]] = []        #x,y coordinates
areas: list[tuple[int, int, int]] = []  #area, point1, point2

def initialize(file_name:str):
    global tiles
   
    file_location = os.path.join("day09", "tests", file_name)
    
    with open(file_location, 'r') as file:
        for line in file:
            pattern = r"(\d+),(\d+)"
            match = re.match(pattern, line)

            if match:
                tiles.append((int(match.group(1)), int(match.group(2))))

    logging.debug(f"Points:\n{tiles}")

def calculate():
    global areas
    for i in range(0, len(tiles)):
        for j in range(i+1,len(tiles)):
            x1,y1 = tiles[i]
            x2,y2 = tiles[j]

            area = (abs(x1-x2)+1)*(abs(y1-y2)+1)
            areas.append((area, i, j))

    areas.sort(key=lambda x: x[0], reverse=True)
            

def main():
    initialize("input.txt")
    calculate()

    print(f"Largest area is: {areas[0][0]}, Using points: {tiles[areas[0][1]]} and {tiles[areas[0][2]]}")
    return

if __name__ == "__main__":
    main()