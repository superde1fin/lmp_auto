#import numpy as np
import sys, os, argparse, json
import DataGenerator, Logger, DataModifier, helper_functions
from CONSTANTS import HEADER_STRINGS as hs
from argparse import RawTextHelpFormatter


"""Attribute Assignment Function"""
def generator_attributes_assignment(args):
    try:
        input_atoms = helper_functions.decompose(json.loads(args.molecules_dict))
    except:
        print("Error: Incorrect dictionary format. Example: {\"B2O3\":55, \"Li2O3\":24, \"Al2O3\":21}. (Do not forget single quotes when passed directly)\n")
        sys.exit()
    try:
        input_density = float(args.density)
    except:
        print("Error: Incorrect density format. Example: 3.14592\n")
        sys.exit()

 
    
    if not (args.filename or args.region_coordinates or args.walls_margin or args.bonds or args.angles or args.dihedrals or args.impropers or args.m or args.force_field):
        dg = DataGenerator.DataGenerator(atoms = input_atoms, density = input_density, generate_datafile = True)
        sys.exit()
    else:
        dg = DataGenerator.DataGenerator(atoms = input_atoms, density = input_density)
        
    if args.from_instance:
        dg.scaled = True
        
    if args.m:
        try:
            dg.m = int(args.m)
        except:
            print("Error: Incorrect scale format. Example: 3")
            sys.exit()
    if args.filename:
        if '.' not in args.filename:
            print("Error: No file extension specified. Example: data.initial\n")
            sys.exit()
        else:
            dg.filename = args.filename
    if args.region_coordinates:
        try:
            dg.region_coordinates = helper_functions.str2tuple(args.region_coordinates)
        except:
            print("Error: Incorrect origin format. Example: '(3, 1, 4)'\n")
            sys.exit()
    if args.walls_margin:
        try:
            dg.distance_from_walls = float(args.walls_margin)
        except:
            print("Error: Incorrect walls_margin format. Example: 3.14592\n")
            sys.exit()
    if args.bonds:
        try:
            dg.bonds = int(args.bonds)
        except:
            print("Error: Incorrect bonds value format. Example 3\n")
            sys.exit()
    if args.angles:
        try:
            dg.angles = int(args.angles)
        except:
            print("Error: Incorrect angles value format. Example 1\n")
            sys.exit()
    if args.impropers:
        try:
            dg.impropers = int(args.impropers)
        except:
            print("Error: Incorrect impropers value format. Example 4\n")
            sys.exit()
    if args.dihedrals:
        try:
            dg.dihedrals = int(args.dihedrals)
        except:
            print("Error: Incorrect dihedrals value format. Example 5\n")
            sys.exit()
    if args.force_field:
        if args.force_field.lower() == "true":
            dg.force_field = True
        elif args.force_field.lower() == "false":
            dg.force_field = False
        else:
            print("Error: Incorrect force_field value format. Example True\n")
            sys.exit()

    dg.generate_datafile()
    sys.exit()    

"""Main Function"""
def main():
    #Creating a main console application parser
    #Setting up the header according to terminal width
    console_size = os.get_terminal_size().columns
    if console_size < 49: #length of the small header line
        header = '\r' + hs['empty']
    elif console_size < 73: #length of the medium header line
        header = '\r' + hs['short']
    elif console_size < 157: #length of the long header line
        header = '\r' + hs['medium']
    else:
        header = hs['long']
    parser = argparse.ArgumentParser("lmp_auto.py",
                                     description = """
usage: lmp_auto {mode} {-p/--parameter} {argument}

This application is an unofficial LAMMPS addon that helps to create necessary initial datafiles, modify existing structures, and keep a record of your project.""",
                                     epilog = "This code was created by the researchers at Alfred University Glass Labs and based on the code provided by the Mauro Glass Group.",
                                     usage = f"\r{header}",
                                     formatter_class=RawTextHelpFormatter)

    #Creating a subparsers group "mode" to allow a user to switch between generation, logging, and modifying
    subparsers =   parser.add_subparsers(help = "Mode of data creator operation", dest = "mode", metavar = "")
    
    #Setting up generator arguments
    parser_generator = subparsers.add_parser("generator", help = "Generates all necessary datafiles for Lammps simulation", usage = f"\r{header}\nusage: lmp_auto generator {{-p/--parameter}} {{argument}}")
    parser_generator.add_argument("-sf", "--setup_file", help = "Read input parameters from a setup file. Additional arguments specified explicitly will override file values", metavar = "")
    parser_generator.add_argument("-md", "--molecules_dict", help = "Molecules dictionary in the following format: \'{\"molecule name\":quantity of molecules}\'", metavar = "")
    parser_generator.add_argument("-d", "--density", help = "Expected density of material", metavar = "")
    parser_generator.add_argument("-f", "--filename", help = "Name of the file where initial Lammps data will be written. Default: \"data.initial\"", metavar = "")
    parser_generator.add_argument("-rc", "--region_coordinates", help = "Coordinates of the simulation box origin \'(x, y, z)\'. Default: (0, 0, 0)", metavar = "")
    parser_generator.add_argument("-wm", "--walls_margin", help = "Inner margin legth of the boxs in which no atoms will be generated. Default: 0.1Å", metavar = "")
    parser_generator.add_argument("-b", "--bonds", help = "Lammps bonds specification. Default: 0", metavar = "")
    parser_generator.add_argument("-a", "--angles", help = "Lammps angles specification. Default: 0", metavar = "")
    parser_generator.add_argument("-m", "--m", help = "Scaling factor for the number of molecules", metavar = "")
    parser_generator.add_argument("-dh", "--dihedrals", help = "Lammps dihedrals specification. Default: 0", metavar = "")
    parser_generator.add_argument("-i", "--impropers", help = "Lammps impropers specification. Default: 0", metavar = "")
    parser_generator.add_argument("-fi", "--from_instance", help = "Allows a user to pull simulation input parameters from a logged instance (n)", metavar = "")
    parser_generator.add_argument("-ff", "--force_field", help = "Help setup a .FF file that defines atom interactions. Default: False", metavar = "")
    
    
    #Setting up mutually exclusive logger arguments
    parser_logger = subparsers.add_parser("logger", help = "Helps access and organize the run logs", usage = f"\r{header}\nusage: lmp_auto logger {{-p/--parameter}} {{argument}}")
    logger_group = parser_logger.add_mutually_exclusive_group()
    logger_group.add_argument("-d", "--display", help = "Display last n instances written in the log file (Display all by passing \"all\" keyword)", metavar = "")
    logger_group.add_argument("-c", "--comment", help = "Add a comment line into a log file", metavar = "")
    logger_group.add_argument("-f", "--find", help = "Display the nth instance written in the log file", metavar = "")
    logger_group.add_argument("-cl", "--clear", action = "store_true",  help = "Clear the log file")
    logger_group.add_argument("-vb", "--version-back",  help = "Return to a previous version of a specified file. (Specify the file as an argument)", metavar = "")
    logger_group.add_argument("-vf", "--version-forward",  help = "Switch to a newer version of a specified file. (Specify the file as an argument)", metavar = "")
    
    #Setting up modifier subparsers
    parser_modifier = subparsers.add_parser("modifier", help = "Allows the user to perform system modifications", usage = f"\r{header}\nusage: lmp_auto modifier -f {{file}} {{modifier option}} {{-p/--parameter}} {{argument}}")
    parser_modifier.add_argument("-f", "--file", help = "The .structure/.initial file to be modified", metavar = "")
    parser_modifier.add_argument("-fi", "--from_instance", help = "Allows the user to pull modification parameters from a logged instance", metavar = "")
    modifier_subparsers = parser_modifier.add_subparsers(help = "Different modifier options", dest = "mod_mode", metavar = "")
    
    #Setting up cut arguments
    cut_parser = modifier_subparsers.add_parser("cut", help = "Creates a hole in a sample based the origin and shape type.", usage = f"\r{header}\nusage: lmp_auto modifier -f {{file}} cut {{-p/--parameter}} {{argument}}")
    cut_parser.add_argument("-s", "--shape", help = "Shape of the geometry to be cut out [box, ellipse]", default = "box", metavar = "")
    cut_parser.add_argument("-r", "--region", help = "Region definition parameter [box - '(xside, yside, zside)', ellipse - '(xaxis, yaxis, zaxis)']", required = True, metavar = "")
    cut_parser.add_argument("-o", "--origin", help = "Origin (center) of the body to shape to be cut out. Example: \'(0, 0, 0)\' (Automatically calculate the center of the region by passing \"center\" keyword)", default = "(0, 0, 0)", metavar = "")
    cut_parser.add_argument("-b", "--balance", help = "Balances the charge of the system after the cut. Off by default. Requires a dictionary of charges as an input: \'{\"1\":4, \"2\":-2, \"3\":1, \"4\":1}\'", default = "", metavar = "")
    
    #Setting up multiply commands
    multiply_parser = modifier_subparsers.add_parser("multiply", help = "Extends the simmulation region by copying it in all three dimensions according to input parameters.", usage = f"\r{header}\nusage: lmp_auto modifier -f {{file}} multiply {{-p/--parameter}} {{argument}}")
    multiply_parser.add_argument("-s", "--scale", help = "A tuple that tells the program how many times to copy an existing system in all directions. Example: \'(1, 1, 1)\'", default = "(1, 1, 1)", metavar = "")

    #Setting up shortener commands
    shortener_parser = modifier_subparsers.add_parser("shortener", help = "Helps shorten files for the purpose of less timely anslysis of data.", usage = f"\r{header}\nusage: lmp_auto modifier -f {{file}} shortener {{-p/--parameter}} {{argument}}")
    shortener_group = shortener_parser.add_mutually_exclusive_group()
    shortener_group.add_argument("-sb", "--shorten-block", help = "Shortens files by '(start line, end line, sieve step, block size)'", metavar = "")
    shortener_group.add_argument("-sd", "--shorten-delimiter", help = "Shortens files by '(start line, end line, sieve step, delimiter line)'", metavar = "")
    
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    
    args = parser.parse_args()

    #Generator mode
    if args.mode == "generator":
        #User selected file parameters' or instance input
        if args.setup_file or args.from_instance:
            if args.from_instance:
                lg = Logger.Logger()
                try:
                    parsed_file = lg.pull_instance(int(args.from_instance))
                    if parsed_file["inst_type"] != "GE":
                        raise RuntimeError("Error: Incorrect instance value (Make sure to select a generator log instance). Example: 3")
                    parsed_file["from_instance"] = True
                except:
                    sys.exit()
            else:
                parsed_file = helper_functions.parse_setup_file(args.setup_file)
                parsed_file["from_instance"] = False
            print(args)
            for key, value in parsed_file.items():
                if key not in ["molecules_dict","density","filename","region_coordinates","walls_margin","bonds","angles","dihedrals","impropers","m", "from_instance", "force_field"]:
                    print(f"Incorrect argument {key}. Check available arguments by using \"-h\" or \"--help\"\n")
                    sys.exit()
                if key == "molecules_dict" and not args.molecules_dict: args.molecules_dict = value
                elif key == "density" and not args.density: args.density = value
                elif key == "filename" and not args.filename: args.filename = value
                elif key == "region_coordinates" and not args.region_coordinates: args.region_coordinates = value
                elif key == "walls_margin" and not args.walls_margin: args.walls_margin = value
                elif key == "bonds" and not args.bonds: args.bonds = value
                elif key == "angles" and not args.angles: args.angles = value
                elif key == "dihedrals" and not args.dihedrals: args.dihedrals = value
                elif key == "impropers" and not args.impropers: args.impropers = value
#                elif key == "submit_batch" and not args.submit_batch: args.submit_batch = value
                elif key == "m" and not args.m: args.m = value
                elif key == "from_instance" and not args.from_instance: args.from_instance = value
                elif key == "force_field" and not args.force_field: args.force_field = value
                    
        #User selected manual input
        if args.molecules_dict and args.density:
            generator_attributes_assignment(args)
        else:
            print("Error: Missing required arguments\n")
            sys.exit()
            
    #Logger mode
    elif args.mode == "logger":
        lg = Logger.Logger()
        if args.display:
            if args.display == "all":
                lg.display("all")
                sys.exit()
            try:
                lg.display(int(args.display))
            except:
                print("Error: Incorrect instance quantity format. Example: 3 (or all)\n")
        if args.comment:
            lg.comment(args.comment)
        if args.find:
            try:
                lg.find(int(args.find))
            except:
                print("Error: Incorrect instance number format. Example: 1\n")
        if args.clear:
            answer = input("Are you sure you want to delete the .log file? All progress will be lost permanently.(Yes/No)")
            if answer == "Yes":
                lg.clear()
            else:
                print("The log file was NOT deleted.")
                sys.exit()
        if args.version_back:
            lg.version_back(args.version_back)
        if args.version_forward:
            lg.version_forward(args.version_forward)
    
    elif args.mode == "modifier":
        if args.from_instance:
            lg = Logger.Logger()
            try:
                parsed_file = lg.pull_instance(int(args.from_instance))
                if parsed_file["inst_type"] not in ["ML", "CT", "SR"]:
                    raise RuntimeError(f"Error: Incorrect instance value {parsed_file['inst_type']} (Make sure to select a modifier log instance). Example: 3")
                if not args.file:
                    args.file = parsed_file["filename"]
                if parsed_file["inst_type"] == "ML":
                    args.mod_mode = "multiply"
                elif parsed_file["inst_type"] == "CT":
                   args.mod_mode = "cut" 
                elif parsed_file["inst_type"] == "SR":
                    args.mod_mode = "shortener"
                    if "shorten_block" in parsed_file:
                        args.shorten_block = parsed_file["shorten_block"]
                        args.shorten_delimiter = None
                    elif "shorten_delim" in parsed_file:
                        args.shorten_delimiter = parsed_file["shorten_delim"]
                        args.shorten_block = None
                    else:
                        print("The shortener instance has been tempered with. Please choose another instance.")
                        sys.exit()
                        


            except Exception as e:
                print(e)
                sys.exit()

        if not args.file:
            print("ERROR: Missing a required argument: -f/--file")
            sys.exit()
        try:
            dm = DataModifier.DataModifier(args.file)
        except:
            print(f"Error. No file: {args.file} was found")
            sys.exit()
            
        if args.mod_mode == "cut":
            if args.from_instance:
                try:
                    _ = args.origin
                    changing_inst = True
                except:
                    changing_inst = False
                if not changing_inst:
                    args.origin = parsed_file["origin"]
                    args.shape = parsed_file["shape"]
                    args.region = parsed_file["region"]
                    args.balance = parsed_file["balance"]
                else:
                    if not args.origin: args.origin = parsed_file["origin"]
                    elif not args.shape: args.shape = parsed_file["shape"]
                    elif not args.region: args.region = parsed_file["region"]
                    elif not args.balance: args.balance = parsed_file["balance"]
            if args.origin == "center":
                cntr = "center"
            else:
                cntr = helper_functions.str2tuple(args.origin)
            dm.cut_out(args.shape, helper_functions.str2tuple(args.region), cntr, bc = args.balance)
            if args.balance:
                try:
                    dm.charge_dict = helper_functions.dict2arr(json.loads(args.balance))
                    dm.balance_charge()
                except Exception as e:
                    print(e, "Incorrect charge dictionary format")
                    sys.exit()
                    
        elif args.mod_mode == "multiply":
            if args.from_instance:
                args.scale = parsed_file["scale"]
            dm.multiply_region(helper_functions.str2tuple(args.scale))

        elif args.mod_mode == "shortener":
            if args.shorten_block:
                try:
                    dm.shorten_block(*tuple(map(int, helper_functions.str2tuple_any(args.shorten_block))))
                except:
                    print("Error: Incorrect sortener arguments. Please refer to the help message by running: lmp_auto modifier shortener -h")
                    sys.exit()
            if args.shorten_delimiter:
                try:
                    str_tuple = helper_functions.str2tuple_any(args.shorten_delimiter)
                    int_args = tuple(map(int, str_tuple[:-1]))
                    dm.shorten_delim(*int_args, str_tuple[-1])
                except Exception as e:
                    print(e, "Error: Incorrect sortener arguments. Please refer to the help message by running: lmp_auto modifier shortener -h")

    
    
    
if __name__ == "__main__":
    main()
