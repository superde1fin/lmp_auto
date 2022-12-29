from datetime import date, datetime
"""Logger Class"""
class Logger:
    log_filename = ".generator.log"
    
    def __init__(self):
        try:
            with open(self.log_filename, 'r') as f:
                self.lines = f.readlines()
        except:
            open(self.log_filename, 'w').write("#Log file for Lammps initial data generation\n#Format: Instance number, atoms, density, filename, bonds, angles, dihedrals, impropers, region_coordinates, walls_margin, m, date of run, time of run\n")
            with open(self.log_filename, 'r') as f:
                self.lines = f.readlines()
    
    def display(self, n):
        if n == "all":
            print(''.join(self.lines))
            return
        display_stack = []
        line = len(self.lines)
        k = len(self.lines) - 1
        for i in range(len(self.lines) - 1, len(self.lines) - n - 1, -1):
            if k > 1:
                if self.lines[i][0] == '#':
                    display_stack.append(self.lines[k])
                    k -= 1
                display_stack.append(self.lines[k])
                k -=1
            
        length = len(display_stack)
        print(self.lines[1].split(':')[1].strip())
        for i in range(length):
            print(display_stack.pop(), end = '')
            
    def comment(self, string_tocomm):
        with open(self.log_filename, 'w') as f:
            f.write(''.join(self.lines) + f"#{string_tocomm}\n")
    
    def find(self, n):
        filtered_lines = list(filter(lambda x: (x[0] != '#' and x[0] != '\n'), self.lines))
        if n >= len(filtered_lines):
            print(f"Error: No instance with an id of {n}")
            sys.exit()
        print(filtered_lines[n])
        
    def clear(self):
        open(self.log_filename, 'w').write("#Log file for Lammps initial data generation\n#Format: Instance number, atoms, density, filename, bonds, angles, dihedrals, impropers, region_coordinates, walls_margin, m, date of run, time of run\n")
        
    def write_line(self, arg_arr):
        file_lines = list(filter(lambda x: (x[0] != '#' and x[0] != '\n'), self.lines))
        if not len(file_lines):
            index = 0
        else:
            index = int(file_lines[-1].split(' | ')[0]) + 1
        with open(self.log_filename, 'w') as f:
            arg_arr[0] = str(arg_arr[0]).replace('\'', '\"')
            f.write(''.join(self.lines) + str(index) + ' | ' + ' | '.join([str(el) for el in arg_arr]) + f" | {date.today().strftime('%m/%d/%Y')} | {datetime.now().strftime('%H:%M:%S')}\n")
    
    def pull_instance(self,n):
        filtered_lines = list(filter(lambda x: (x[0] != '#' and x[0] != '\n'), self.lines))
        if n >= len(filtered_lines):
            print(f"Error: No instance with an id of {n}")
            sys.exit()
        values = filtered_lines[n].split(" | ")[1:-2]
        keys = self.lines[1].split(':')[1].replace(' ', '').split(',')[1:-2]
        args_dict = {}
        for key, value in zip(keys, values):
            if value == "ML":
                print(f"Error: Not a generator log instance {n}")
                sys.exit()
            if key == "atoms":
                args_dict["molecules_dict"] = value
            elif key:
                args_dict[key] = value
            
        return args_dict
