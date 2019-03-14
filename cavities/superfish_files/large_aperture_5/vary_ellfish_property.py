'''
This program calls ELLFISH using WINE, this will not work with a native windows
install of superfish. If ELLFISH is in the system PATH then it's possible it
could be made to work by removing "'wine'," from the subprocess call.
'''
import os
from os.path import join
import subprocess
import numpy as np
import re
import multiprocessing

def run_sweep(file_name, temp_dir, new_directory, property, values):
    # Make directory structure
    subprocess.run(['mkdir', '-p', temp_dir])
    subprocess.run(['mkdir', '-p', new_directory])
    subprocess.run(['mkdir', '-p', join(new_directory, "results")])
    subprocess.run(['mkdir', '-p', join(new_directory, "plots")])
    subprocess.run(['mkdir', '-p', join(new_directory, "mesh")])
    subprocess.run(['mkdir', '-p', join(new_directory, "ellfish_files")])
    subprocess.run(['mkdir', '-p', join(new_directory, "other")])

    # make the ell file from the temp file
    for n, i in enumerate(values):
        os.chdir(temp_dir)
        print("Running Value {:.3f} ({}/{})".format(i, n+1, len(values)))
        with open(join('../', file_name), 'r') as input_file, open('{:.3f}.ell'.format(i), 'w') as output_file:
            for line in input_file:
                if re.match('^FILEname_prefix', line.strip()):
                    output_file.write("FILEname_prefix \t\t\t {:.3f}\n".format(i))
                elif re.match('^'+property, line.strip()):
                    output_file.write(property + " \t\t\t{:.3f}\n".format(i))
                else:
                    output_file.write(line)

        # break
        # This is the subprocess call to ELLFISH, windows users should remove the
        # first item of the list (that says wine).
        subprocess.run(['ELLFISH', '{:.3f}.ell'.format(i)])

        os.chdir('../')

        # Move files to appropriate directory
        subprocess.call('mv {}/*.SFO {}/results/'.format(      temp_dir,  new_directory), shell=True)
        subprocess.call('mv {}/*.T35 {}/plots/'.format(        temp_dir,  new_directory), shell=True)
        subprocess.call('mv {}/*.SEG {}/mesh/'.format(         temp_dir,  new_directory), shell=True)
        subprocess.call('mv {}/*.AM {}/mesh/'.format(          temp_dir,  new_directory), shell=True)
        subprocess.call('mv {}/*.ell {}/ellfish_files/'.format(temp_dir,  new_directory), shell=True)
        subprocess.call('mv {}/*.LOG {}/other/'.format(        temp_dir,  new_directory), shell=True)
        subprocess.call('mv {}/*.TXT {}/other/'.format(        temp_dir,  new_directory), shell=True)
        subprocess.call('mv {}/*.INF {}/other/'.format(        temp_dir,  new_directory), shell=True)

if __name__ == '__main__':
    jobs = []
    file_name = 'template.temp'
    temp_dir = 'temp_1'
    new_directory = 'right_dome_b'
    property = "RIGHT_DOME_B"
    values = np.linspace(15, 35, 10)
    p = multiprocessing.Process(target=run_sweep, args=(file_name, temp_dir, new_directory, property, values,))
    jobs.append(p)
    del(file_name)
    del(new_directory)
    del(property)
    del(values)

    file_name = 'template.temp'
    temp_dir = 'temp_2'
    new_directory = 'dome_a_over_b/'
    property = "RIGHT_DOME_A/B"
    values = np.linspace(0.4, 1.50, 10)
    p = multiprocessing.Process(target=run_sweep, args=(file_name, temp_dir, new_directory, property, values,))
    jobs.append(p)
    del(file_name)
    del(new_directory)
    del(property)
    del(values)

    file_name = 'template.temp'
    temp_dir = 'temp_3'
    new_directory = 'wall_angle/'
    property = "RIGHT_Wall_angle"
    values = np.linspace(10, 35, 15)
    p = multiprocessing.Process(target=run_sweep, args=(file_name, temp_dir, new_directory, property, values,))
    jobs.append(p)
    del(file_name)
    del(new_directory)
    del(property)
    del(values)

    file_name = 'template.temp'
    temp_dir = 'temp_4'
    new_directory = 'iris_a_over_b/'
    property = "RIGHT_IRIS_A/B"
    values = np.linspace(0.6, 1.0, 10)
    p = multiprocessing.Process(target=run_sweep, args=(file_name, temp_dir, new_directory, property, values,))
    jobs.append(p)
    del(file_name)
    del(new_directory)
    del(property)
    del(values)

    for i in jobs:
        i.daemon=True
        i.start()

    for i in jobs:
        i.join()

    #file_name = 'template.temp'
    #new_directory = 'bore_radius/'
    #property = "BORE_radius"
    #values = np.linspace(20, 30, 11)
