import sys
import CONSTANTS as const
"""Independent Functions"""
def decompose(molecules_dict):
    atoms_dict = {}
    for molecule, quantity in molecules_dict.items():
        molecule += '.'
        atom = ""
        for symbol in molecule:
            if (len(atom) and symbol.isupper()) or symbol == '.':
                if atom[-1].isdigit():
                    if not (atom[:-1] in const.ATOMIC_MASSES.keys()):
                        print(f"Error: Incorrect atom name: {atom[:-1]}")
                        sys.exit()
                    if atom[:-1] in atoms_dict:
                        atoms_dict[atom[:-1]] += quantity*int(atom[-1])
                    else:
                        atoms_dict[atom[:-1]] = quantity*int(atom[-1])
                else:
                    if not (atom in const.ATOMIC_MASSES.keys()):
                        print(f"Error: Incorrect atom name: {atom[:-1]}")
                        sys.exit()
                    if atom in atoms_dict:
                        atoms_dict[atom] += quantity
                    else:
                        atoms_dict[atom] = quantity
                atom = ""
            atom += symbol
    
    return atoms_dict
        
def str2tuple(tuple_string):
    tuple_string = tuple_string.replace('(', '')
    tuple_string = tuple_string.replace(')', '')
    tuple_string = tuple_string.replace(' ', '')
    try:
        result = tuple(map(int, tuple_string.split(',')))
        return result
    except:
        raise Exception("Non-int elements in a tuple")

def str2tuple_any(tuple_string):
    tuple_string = tuple_string.replace('(', '')
    tuple_string = tuple_string.replace(')', '')
    tuple_string = tuple_string.replace(' ', '')
    return tuple(tuple_string.split(','))

def parse_setup_file(filename):
    result_dict = {}
    try:
        with open(filename, 'r') as setup_file:
            file_lines = setup_file.readlines()
    except:
        with open(filename, 'w') as setup_file:
            setup_file.write("""#This file can be used for a simpler argument assignment during the initial datafile generation process.
#Each argument - value pair should start on a new line and be of format: "arg_name=value"

""")
        print(f"Error: Setup file {filename} does not exist")
        print(f"A sample file {filename} has been created")
        sys.exit()
    
        
    file_lines = list(filter(lambda x: (x[0] != '#' and x[0] != '\n'), file_lines))
    for line in file_lines:
        arg, value = line.replace(' ', '').replace("\n", '').split('=')[0:2]
        result_dict[arg.lower()] = value
        
    return result_dict
    
def even_space_circle(r, unit_side):
    coords = []
    radial_steps = int(r/unit_side)
    
    for i in range(radial_steps):
        for j in range(radial_steps):
            x = i + unit_side/2
            y = j + unit_side/2
            if (x)**2 + (y)**2 <= r**2:
                #First quadrant
                coords.append((x, y))
                
                #Second quadrant
                x = -i - unit_side/2
                y = j + unit_side/2
                coords.append((x, y))
                    
                #Second quadrant
                x = -i - unit_side/2
                y = -j - unit_side/2
                coords.append((x, y))
                
                #Fourth quadrant
                x = i + unit_side/2
                y = -j - unit_side/2
                coords.append((x, y))
                
    return coords
                
def dict2arr(dictionary):
    try:
        indecies = list(map(int, dictionary.keys()))
        array = []*len(indecies)
        for ind in indecies:
            array[ind] = dictionary[str(ind)]
        return array
    except:
        return list(dictionary.values())

















