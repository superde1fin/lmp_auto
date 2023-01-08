from datetime import date, datetime
import glob, os, sys, subprocess
"""Logger Class"""
class Logger:
    log_filename = ".automator.log"
    
    def __init__(self):
        try:
            with open(self.log_filename, 'r') as f:
                self.lines = f.readlines()
        except:
            open(self.log_filename, 'w').write("#Lammps Automator log file.\n#General prefixes format: Instance Number, Instance Type, Type Description\n#Generator Format: Instance Number, Instance Type, Instance Description, atoms, density, filename, bonds, angles, dihedrals, impropers, region_coordinates, walls_margin, m, date of run, time of run\n")
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
        open(self.log_filename, 'w').write("#Lammps Automator log file.\n#General prefixes format: Instance Number, Instance Type, Type Description\n#Generator Format: Instance Number, Instance Type, Instance Description, atoms, density, filename, bonds, angles, dihedrals, impropers, region_coordinates, walls_margin, m, date of run, time of run\n")
        
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
        inst_type = values[0]
        values = values[2:]
        args_dict = {}
        args_dict["inst_type"] = inst_type
        if inst_type == "GE":
            keys = self.lines[2].split(':')[1].replace(' ', '').split(',')[3:-2]
            for key, value in zip(keys, values):
                if key == "atoms":
                    args_dict["molecules_dict"] = value
                elif key:
                    args_dict[key] = value
        elif inst_type == "CT":
            args_dict["filename"] = values[0].split(':')[1].strip()
            args_dict["shape"] = values[1].split(':')[1].strip()
            args_dict["origin"] = values[2].split(':')[1].strip()
            args_dict["region"] = values[3].split(':')[1].strip()
            balance_dict = '{' + values[4].split('{')[1].strip() 
            args_dict["balance"] = None if "False" in balance_dict else balance_dict


        elif inst_type == "ML":
            args_dict["filename"] = values[0].split(':')[1].strip()
            args_dict["scale"] = '(' + ','.join([val.split(':')[-1] for val in values[1].split(',')]) + ')'

            
            
        return args_dict
    
    def record_file_changes(self):
        filename = glob.glob(".*.prev.*")
        if filename:
            filename = filename[0]
            name4save = filename.replace(".prev", '')
            if not os.path.exists(".versions"):
                os.system("mkdir -p .versions/old")
                os.system("mkdir -p .versions/new")
            subprocess.call(["rm",  ".versions/new/.*{name4save}"], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
            files = os.popen("ls -all .versions/old").read().strip()
            files = files.split('\n')[3:]
            if files:
                version = max([int(line.split('.')[1]) for line in files]) + 1
            else:
                version = 0
            os.popen(f"mv {filename} .versions/old/.{version}{name4save}")
        else:
            print("No modifications have been made, or the previous datafile was removed")
            sys.exit()

    def version_back(self, filename):
        if os.path.exists(".versions"):
            old_files = os.popen("ls -all .versions/old").read().strip().split('\n')[3:]
            new_files = os.popen("ls -all .versions/new").read().strip().split('\n')[3:]
            old_version = 0 if not old_files else max([int(line.split('.')[1]) for line in old_files])
            new_version = 0 if not new_files else max([int(line.split('.')[1]) for line in new_files]) + 1
            if glob.glob(f".versions/old/.*.{filename}"):
                os.system(f"cp {filename} .versions/new/.{new_version}.{filename}")
                os.system(f"mv .versions/old/.{old_version}.{filename} {filename}")
            else:
                print(f"No previous versions of file {filename} available")
                sys.exit()
        else:
            print("No previous versions available")
            sys.exit()


    def version_forward(self, filename):
        if os.path.exists(".versions"):
            old_files = os.popen("ls -all .versions/old").read().strip().split('\n')[3:]
            new_files = os.popen("ls -all .versions/new").read().strip().split('\n')[3:]
            old_version = 0 if not old_files else max([int(line.split('.')[1]) for line in old_files]) + 1
            new_version = 0 if not new_files else max([int(line.split('.')[1]) for line in new_files])
            if glob.glob(f".versions/new/.*.{filename}"):
                os.system(f"cp {filename} .versions/old/.{old_version}.{filename}")
                os.system(f"mv .versions/new/.{new_version}.{filename} {filename}")
            else:
                print(f"No future versions of file {filename} available")
                sys.exit()
        else:
            print("No future versions available")
            sys.exit()


















