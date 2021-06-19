"""
@Author: Jackson Elowitt
@Date: 6/18/21
@Contact: jkelowitt@protonmail.com

Take all the .log files in a given directory and make a new
directory which has .com files for the log files.
"""
from functions import make_output_folder
from parsing import parse_opt_geom_from_log, yes_no, write_job_to_com
from classes import Atom, Molecule
from glob import glob


def main():
    # From where to where
    dir = input("Enter the directory of the .log files: ")
    new_dir = input("Enter the name of the folder you'd like to save the com files to: ")

    # Get the parameters for the com file

    settings = {
        "charge": "0",
        "mul": "1",
        "job": "Opt Freq",
        "theory": "B3LPY",
        "basis": "6-311G(2df,2p)",
        "cores": "8",
        "memory": "20gb",
        "linda": "1",
    }

    # Display default settings
    print("\nDefault Settings: ")
    for item in settings:
        print(f"\t{item} = {settings[item]}")

    non_default = yes_no("\nUse the default settings")

    # Change default options if desired
    if not non_default:
        done = False
        while not done:
            settings, done = change_dict_values(settings)

    # Get the files to parse
    files = glob(dir + "/*.log")

    # Make the output folder
    make_output_folder(new_dir)

    # Parse geometry and write the files
    for file in files:
        data = parse_opt_geom_from_log(file)
        atoms = [Atom(a[0], (a[1], a[2], a[3])) for a in data]
        name = file.split("\\")[-1][:-4]
        molecule = Molecule(name, atoms)
        write_job_to_com(molecule.atoms, title=molecule.name, output=dir + "\\" + new_dir, **settings)


if __name__ == "__main__":
    main()