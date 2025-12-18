import os, re, logging

logging.basicConfig(level=logging.INFO)
data_file = "input.txt"

data: list[tuple[str,list[list[int]],list[int]]] = []
goal:str = "."

def initialize():
    global data_file
    file_location = os.path.join("day10", "tests", data_file)

    with open(file_location, 'r') as file:
        for line in file:
            lights:str = ""
            buttons: list[list[int]] = []
            jolts:list[int] = []

            pattern = r'\[(.+?)\](.+?)\{(.+?)\}\s*'
            match = re.match(pattern, line)
            if match:
                lights:str = match.group(1)
                content_blocks = re.findall(r'\((.*?)\)',  match.group(2))
                
                for block_string in content_blocks:
                    number_strings = block_string.split(",")
                    integer_list = [int(num_str) for num_str in number_strings]
                    buttons.append(integer_list)
                
                for jolt in match.group(3).split(","):
                    jolts.append(int(jolt))

            logging.debug(f"Lights:{lights}, Buttons: {buttons}, Jolts:{jolts}")
            item = (lights, buttons, jolts)
            data.append(item)
    return

def isSolved(value: list[str]) -> bool:
    return all(char == "." for char in value)

def flip(s:str) -> str:
    if s == "#":
        return "."
    elif s == ".":
        return "#"
    else:
        raise Exception("Unexpected input: {s}")

def rotate(item:str, button:list[int])->str:
    existing_value:list[str] = list(item)
    new_value:list[str]=list(existing_value)
   
    for b in button:
        new_value[b] = flip(existing_value[b])
    logging.debug(f"button is: {button}, rotation is: {"".join(new_value)}")
    return "".join(new_value)

def solve():
    turns = 0
    solution:int = 0
    for (lights,buttons,_) in data:
        lights_start:str = "." * len(lights)
        seen:set[str] = set()
        turn:set[str] = set()
        turn.add(lights_start)
        seen.add(lights_start)

        while turns < 10:
            if lights in turn:
                logging.info(f"********* Found in {turns} turns.******")
                solution+=turns
                turns = 0
                turn.add(lights_start)
                break
            turns += 1

            #rotate each item in turn, and give me a new list for the next turn.
            #that new list is evaluted for anything seen before, and is thrown out.
            #that new list is evaluated for the goal
            #next turn.
            next_turn:set[str] = set()

            for item in turn:
                for button in buttons:
                    next_turn.add(rotate(item, button))
                
            next_turn = next_turn - seen
            seen = seen | next_turn
            turn = next_turn
    print(f"Solution: {solution}")
    return

def main():
    initialize()
    solve()
    return

if __name__ == "__main__":
    main()