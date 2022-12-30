import sys, os, random
import Logger
#import helper_functions as hlp

class DataModifier:
    def __init__(self, filename):
        self.file = filename
    
        
    """Logic Functions Start"""
    def add_up(self, t, max_iter):
        srt = sorted(self.charge_dict)
        i = 0
        negative = []
        while i < len(srt) and srt[i] < 0:
            i += 1
        negative = srt[:i]
        positive = srt[i:]
        
        i = 0
        result = []
        while t !=0 and i <= max_iter:
            n, p = 0, 0
            while t < 0 and n < len(negative):
                if t <= negative[n] or n == len(negative) - 1:
                    t -= negative[n]
                    result.append(negative[n])
                n += 1
            while t > 0 and p < len(positive):
                if t >= positive[p] or p == len(positive) - 1:
                    t -= positive[p]
                    result.append(positive[p])
                p += 1
            i += 1
                
        if t:
            result = []
        return result
    """Logic Functions End"""
        
    """Parser Functions Start"""
    def get_header(self):
        file_length = len(self.lines)
        line = 0
        while (line < file_length) and (not self.lines[line].startswith("Atoms")):
            line += 1
            
        if line >= file_length:
            print("Error: Incorrect .structure file format. No atom declaration found.")
            sys.exit()
        return '\n'.join(self.lines[:line + 1]).strip('\n')
        
    def get_atom_lines(self):
        return self.plaintext.split(self.header)[1].split("Velocities")[0].strip('\n').split('\n')
        
    def get_velocities(self):
        return self.plaintext.split('\n'.join(self.lines))[1].strip('\n')
        
    def get_atom_num(self):
        split_h = []
        for el in self.header.split('\n'):
            split_h += el.split(' ')
        return int(split_h[split_h.index("atoms") - 1])
    
    def get_coords(self):
        coords = [None, None, None]
        header = [line.split(' ') for line in self.header.split('\n')]
        line = 0
        for _ in range(3):
            done = False
            while not done:
                if line < len(header) and ((len(header[line]) < 3) or ((header[line][2:4] != ["xlo", "xhi"]) and (header[line][2:4] != ["ylo", "yhi"]) and (header[line][2:4] != ["zlo", "zhi"]))):
                    line += 1
                else:
                    done = True
            if line >= len(header):
                print("Error: Incorrect .structure file format. No atom declaration found.")
                sys.exit()
            if header[line][2:4] == ["xlo", "xhi"]:
                coords[0] = (float(header[line][0]), float(header[line][1]))
            elif header[line][2:4] == ["ylo", "yhi"]:
                coords[1] = (float(header[line][0]), float(header[line][1]))
            elif header[line][2:4] == ["zlo", "zhi"]:
                coords[2] = (float(header[line][0]), float(header[line][1]))
            line += 1
        return coords
        
    def get_center(self):
        coords = self.coords
        return ((coords[0][1] -coords[0][0])/2, (coords[1][1] -coords[1][0])/2, (coords[2][1] -coords[2][0])/2)
        
    def get_velocity_dict(self):
        vel = self.velocities.split('\n')
        velocity_dict = {}
        for line in vel:
            split_line = line.split(' ')
            if len(split_line) > 2: #Avoid random empty lines and the Velocity line
                velocity_dict[split_line[0]] = split_line
        
        return velocity_dict
    """Parser Functions End"""
    
    """Bounding functions Start"""
    def bounds_box(self, region_def, coords, origin):
        box = region_def
        return ((coords[0] >= origin[0] - box[0]/2) and (coords[0] <= origin[0] + box[0]/2)) and ((coords[1] >= origin[1] - box[1]/2) and (coords[1] <= origin[1] + box[1]/2)) and ((coords[2] >= origin[2] - box[2]/2) and (coords[2] <= origin[2] + box[2]/2))
        
    def bounds_ellipse(self, region_def, coords, origin):
        axis = region_def
        return ((coords[0] - origin[0])/axis[0])**2 + ((coords[1] - origin[1])/axis[1])**2 + ((coords[2] - origin[2])/axis[2])**2 <= 1
    """Bounding functions End"""
    
    """Modifying Functions Start"""
    def cut_out(self, shape, region_def, origin, bc):
        if len(region_def) != 3:
            print("Incorrect region definition")
            sys.exit()
        
        
            
        f = open(self.file, 'r')
        self.plaintext = f.read()
        self.lines = self.plaintext.split('\n')        
        self.header = self.get_header()
        self.lines = self.get_atom_lines()
        self.velocities = self.get_velocities()
        self.coords = self.get_coords()
        
        if origin == "center":
            origin = self.get_center()
        elif len(origin) != 3:
            print("Incorrect origin definition")
            sys.exit()

        if shape == "box":
            bounder = self.bounds_box
        elif shape == "ellipse":
            bounder = self.bounds_ellipse
        else:
            print("Error: Incorrect shape to cut out.")
            sys.exit()
            
        velocity_dict = self.get_velocity_dict()
        #print('\n'.join([f"{key} :: {value}" for key, value in velocity_dict.items()]))
        if velocity_dict:
            modifying_vel = True
        else:
            modifying_vel = False
            
        new_lines = []
        new_velocities = ["Velocities\n"]
        ctr = 0
        for line in self.lines:
            split_ln = line.split(' ')
            atom_id = split_ln[0]
            coords = list(map(float, split_ln[3:6]))
            if not bounder(region_def = region_def, coords = coords, origin = origin):
                new_lines.append(line)
                if modifying_vel:
                    new_velocities.append(' '.join(velocity_dict[atom_id]))
                ctr += 1

        self.modify_atom_number(ctr)
        
        self.header = self.header.replace('\n', "\n#Cut made\n", 1)
        
        if modifying_vel:
            self.write_to_file(self.header, '\n'.join(new_lines), '\n' + '\n'.join(new_velocities))
        else:
            self.write_to_file(self.header, '\n'.join(new_lines),"")
        lg = Logger.Logger()
        lg.write_line(["CT", "Hole Cutout", f"Modified File: {self.file}", f"Cut Shape: {shape}", f"Hole Center: {tuple([round(coord, 3) for coord in origin])}", f"Region Definition: {region_def}", f"Balanced: {bc if bc else False}"])
        lg.record_file_changes()
        
    
    def modify_name(self):
        name, dtype = self.file.split('.')
        new_name =  '.' + name + ".prev" + '.' + dtype
        if not new_name in os.popen("ls").read():
            print("Saving an old version")
            os.system(f"cp {self.file} \"{new_name}\"")
    
    def modify_atom_number(self, n):
        self.atom_num = n
        header = [line.split(' ') for line in self.header.split('\n')]
        line = 0
        done = False
        while not done:
            if line < len(header) and ((len(header[line]) < 2) or (header[line][1] != "atoms")):
                line += 1
            else:
                done = True
                
        if line >= len(header):
            print("Error: Incorrect .initial file format. No atom declaration found.")
            sys.exit()
        header[line][0] = str(self.atom_num)
        self.header = '\n'.join([' '.join(line) for line in header])
    
    def set_coords(self, coords):
        origin = [crd[0] for crd in self.coords]
        header = [line.split(' ') for line in self.header.split('\n')]
        line = 0
        for _ in range(3):
            done = False
            while not done:
                if line < len(header) and ((len(header[line]) < 3) or ((header[line][2:4] != ["xlo", "xhi"]) and (header[line][2:4] != ["ylo", "yhi"]) and (header[line][2:4] != ["zlo", "zhi"]))):
                    line += 1
                else:
                    done = True
            if line >= len(header):
                print("Error: Incorrect .initial file format. No atom declaration found.")
                sys.exit()
            if header[line][2:4] == ["xlo", "xhi"]:
                header[line][0] = str(origin[0])
                header[line][1] = str(coords[0])
            elif header[line][2:4] == ["ylo", "yhi"]:
                header[line][0] = str(origin[1])
                header[line][1] = str(coords[1])
            elif header[line][2:4] == ["zlo", "zhi"]:
                header[line][0] = str(origin[2])
                header[line][1] = str(coords[2])
            line += 1
            
        self.header = '\n'.join([' '.join(line) for line in header])
    
    def multiply_region(self, scale, space_between = 0.6):
        print("Multiplying")
        f = open(self.file, 'r')
        self.plaintext = f.read()
        self.lines = self.plaintext.split('\n')        
        self.header = self.get_header()
        self.lines = self.get_atom_lines()
        self.velocities = self.get_velocities()
        self.coords = self.get_coords()
        
        
        velocity_dict = self.get_velocity_dict()
        if velocity_dict:
            modifying_vel = True
        else:
            modifying_vel = False
            
        self.set_coords(coords = ((self.coords[0][1] + space_between)*scale[0], (self.coords[1][1] + space_between)*scale[1], (self.coords[2][1] + space_between)*scale[2]))
        atoms_num = 0
        new_lines = ""
        new_velocities = "Velocities\n\n"
        for x in range(scale[0]):
            for y in range(scale[1]):
                for z in range(scale[2]):
                    for line in self.lines:
                        atoms_num += 1
                        splitted = line.split(' ')
                        atom_key = splitted[0]
                        splitted[0] = str(atoms_num)
                        coords = list(map(float, splitted[3:6]))
                        coords[0] = str(coords[0] + (self.coords[0][1] + space_between)*x)
                        coords[1] = str(coords[1] + (self.coords[1][1] + space_between)*y)
                        coords[2] = str(coords[2] + (self.coords[2][1] + space_between)*z)
                        splitted = splitted[:3] + coords + splitted[6:]
                        new_lines += (' '.join(splitted) + '\n')
                        if modifying_vel: 
                            vel_line = velocity_dict[atom_key]
                            vel_line[0] = str(atoms_num)
                            new_velocities += (' '.join(vel_line) + '\n')
                        
                        
        self.modify_atom_number(atoms_num)
        self.header = self.header.replace('\n', "\n#Region multiplied\n", 1)
        if modifying_vel:
            self.write_to_file(self.header, new_lines, new_velocities)
        else:
            self.write_to_file(self.header, new_lines, "")
        lg = Logger.Logger()
        lg.write_line(["ML", "Region Multiplication", f"Modified File: {self.file}", f"Scale: x:{scale[0]}, y:{scale[1]}, z:{scale[2]}"])
        lg.record_file_changes()
    
    def balance_charge(self):
        
        f = open(self.file, 'r')
        self.plaintext = f.read()
        self.lines = self.plaintext.split('\n')        
        self.header = self.get_header()
        self.lines = self.get_atom_lines()
        self.velocities = self.get_velocities()
        self.coords = self.get_coords()

        print(self.velocities)
        if self.velocities:
            modifying_vel = True
        else:
            modifying_vel = False
        
        total_charge = 0
        for line in self.lines:
            total_charge += self.charge_dict[int(line.split(' ')[1]) - 1]
        if total_charge != 0:
            atom_num = self.get_atom_num()
            to_rem = self.add_up(total_charge, max_iter = atom_num)
            self.modify_atom_number(atom_num - len(to_rem))
            new_lines = []
            new_velocities = ["\nVelocities\n"]
            velocities = self.velocities.split('\n')
            vel_dict = self.get_velocity_dict()
            random.shuffle(self.lines)
            for line in self.lines:
                splt = line.split(' ')
                atom_type = int(splt[1])
                if not self.charge_dict[atom_type - 1] in to_rem:
                    new_lines.append(line)
                    if modifying_vel:
                        new_velocities.append(' '.join(vel_dict[splt[0]]))
                else:
                    to_rem.remove(self.charge_dict[atom_type - 1])
            
            self.header = self.header.replace('\n', "\n#Charge balanced\n", 1)
            if modifying_vel:
                self.write_to_file(self.header, '\n'.join(new_lines), '\n'.join(new_velocities))
            else:
                self.write_to_file(self.header, '\n'.join(new_lines), "")
            lg = Logger.Logger()
#            lg.write_line(["BL", "Charge Balancing", f"Modified File: {self.file}", f"Charge Array: {self.charge_dict}"])
            lg.record_file_changes()

        else:
            print("Total charge is already 0")

    def write_to_file(self, new_header, new_lines, new_velocities):
        self.modify_name()
        open(self.file, 'w').write(new_header + '\n\n' + new_lines + '\n' + new_velocities)

    """Modifying Functions End"""
    








