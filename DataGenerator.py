from typing import List, Dict, Tuple
import CONSTANTS as const
import numpy as np
import Logger, helper_functions
import sys

"""Data Generator Class"""
class DataGenerator:
    
    def __init__(self, atoms: Dict[str, int], density: float, filename: str = "data.initial", generate_datafile:bool = False, bonds:int = 0, angles:int = 0, dihedrals:int = 0, impropers:int = 0, region_coordinates: Tuple[int, int, int] = (0, 0, 0, 1), distance_from_walls:float = 0.5, m:int = 10, force_field:bool = False):
        #Atoms dictionary consists of pairs with atoms' types and quantities. Example: {"O":3,  "B":1, "Si":4}
        
        self.atoms = atoms
        self.m = m
        self.density = density
        self.filename = filename
        self.bonds = bonds
        self.angles = angles
        self.dihedrals = dihedrals
        self.impropers = impropers
        self.region_coordinates = region_coordinates
        self.distance_from_walls = distance_from_walls
#        self.submit_batch = submit_batch
        self.force_field = force_field
        self.scaled = False
        
        
        
        
        
        if generate_datafile:
            self.generate_datafile()
            sys.exit()
        
    
    def atom_num_scale(self):
        for key, value in self.atoms.items():
            self.atoms[key] = value*self.m
        self.scaled = True
        
    #This function allows a user to append data to an existing file
    def file_append(self, data: str, filename: str = -1):
        filename = self.filename if filename == -1 else filename
        
        existing_data = open(filename, 'r').read()
        open(filename, 'w').write(existing_data + data)
        
        
    
    
    def calculate_region_params(self):
        if not self.scaled:
            self.atom_num_scale()
        #Total number of atoms present in the simulation
        self.atom_number = sum(self.atoms.values())
        #Number of different atom types
        self.type_quantity = len(self.atoms)
        #Total mass of all atoms is calculated by summing the products of atom quantity and atomic mass of each atom type
        self.total_mass = sum([atom_quantity * const.ATOMIC_MASSES[atom_type] for atom_type, atom_quantity in self.atoms.items()])
        #Calcting volume by dividing total mass by density [mu/Å3]
        self.shape_volume:float = self.total_mass/(self.density*0.60221409)
        #Calculate the length of an atomic cube side by deviding total volume by number of atoms to get volume occupied per atom and then taking a cube root of it
        #Leaving the spacing of 0.4 Angstroms
        self.atom_unit_size = (self.shape_volume/self.atom_number)**(1/3) - 0.4
        #Side of the simulation box
        self.cube_side = self.shape_volume**(1/3)
        
        
    #This function calculates all values needed for a header of the lammps initial datafile
    def header_setup(self, first_line: str = "Generated From Cif"):
        if not self.scaled:
            self.atom_num_scale()
        
        region_definition = f"""
{self.region_coordinates[0]} {self.cube_side} xlo xhi
{self.region_coordinates[1]} {self.cube_side} ylo yhi
{self.region_coordinates[2]} {self.cube_side} zlo zhi
"""
        
        #Writing up the header of the lammps datafile according to the rules listed here: https://docs.lammps.org/read_data.html
        header = f"""#{first_line}

{self.atom_number} atoms
{self.bonds} bonds
{self.angles} angles
{self.dihedrals} dihedrals
{self.impropers} impropers
{self.type_quantity} atom types
{region_definition}
"""
        open(self.filename, 'w').write(header)
    
    #This function calculates evenly spaced positions in a cube, assigns each position an atom of a specific type, and writes that information into the lammps initial data file
    def create_atom_positions(self):
        if not self.scaled:
            self.atom_num_scale()
        

        atom_string = """Atoms

"""
        #Calculate the number of atoms on a side
        atoms_on_side = int((self.cube_side - self.distance_from_walls*2)/self.atom_unit_size)
        #numpy.linspace(start, end, step, include endpoints) - Returns a list of evenly spaced numbers
        available_side_positions = np.linspace(self.distance_from_walls + self.atom_unit_size/2, self.cube_side - self.distance_from_walls, atoms_on_side, endpoint = False)
        
        #Writing out atom coordinates into a data.initial file
        atom_types_counter = list(self.atoms.values())
        all_3d_pos = []
        for x in available_side_positions:
            for y in available_side_positions:
                for z in available_side_positions:
                    all_3d_pos.append((x, y, z))
        np.random.shuffle(all_3d_pos)
        
        if len(all_3d_pos) <= sum(atom_types_counter):
            print("Error: Simulation box is too small. Cannot place atoms according to inputted density.")
            sys.exit()
        
        atom_type = 0
        i = 0
        print(''.join([value.center(15) for value in "Id Type Charge x y z".split(' ')]), '\n')
        while sum(atom_types_counter):
            if not atom_types_counter[atom_type]:
                atom_type += 1
            to_add = f"{i + 1} {atom_type + 1} 0 {round(all_3d_pos[i][0] + self.region_coordinates[0], 3)} {round(all_3d_pos[i][1] + self.region_coordinates[1], 3)} {round(all_3d_pos[i][2] + self.region_coordinates[2], 3)}\n"
            atom_types_counter[atom_type] -= 1
            atom_string += to_add
            print(''.join([value.center(15) for value in to_add.split(' ')]))
            i += 1
        self.file_append(atom_string)
        

    #This function sets up a .FF file for convenient use of table potentials    
    def setup_force_field(self):
        atom_names = list(self.atoms.keys())
        force_field_file = open("Potentials.FF", 'w')
        to_write = "#Automatically generated potentials definition file\n"
        for i, atom in enumerate(atom_names):
            to_write += f"mass\t\t{i + 1} {const.ATOMIC_MASSES[atom]} #{atom}\n"
        to_write += '\n'
        for i, atom in enumerate(atom_names):
            to_write += f"group\t\t{atom} type {i + 1} {i + 1}\n"
        to_write += '\n'
        
        to_write += "pair_style\ttable linear 10000 #The number of instances should be changed according to the table used\n\n"
        to_write += "variable\tTABLE string \"put table name here\"\n\n#Change group names (Si-Si) according to the table used\n"
        
 
        for i in range(len(atom_names)):
            for j in range(i, len(atom_names)):
                to_write += f"pair_coeff\t{i + 1} {j +1} ${{TABLE}} {atom_names[i]}-{atom_names[j]}\n"
            to_write += '\n'
                
        force_field_file.write(to_write)
        force_field_file.close()
        
        
        
    #This function automatically assembles both part of the file generation allowing one to not call them separately
    def generate_datafile(self):
        self.calculate_region_params()
        if not self.scaled:
            self.atom_num_scale()
        self.header_setup()
        self.create_atom_positions()
        lg = Logger.Logger()
        lg.write_line([self.atoms, self.density, self.filename, self.bonds, self.angles, self.dihedrals, self.impropers, self.region_coordinates, self.distance_from_walls, self.m])

#        if self.submit_batch:
#            os.system("vim `ls *.pbs | head -1`")
        
        if self.force_field:
            self.setup_force_field()
