import subprocess
import numpy as np
import re

file_name = 'template.temp'
new_directory = 'right_dome_size'

property = "RIGHT_DOME_B"
values = np.linspace(16, 25, 10)


# Make directory structure
subprocess.run(['mkdir', new_directory])
subprocess.run(['mkdir', new_directory+"/results"])
subprocess.run(['mkdir', new_directory+"/plots"])
subprocess.run(['mkdir', new_directory+"/mesh"])
subprocess.run(['mkdir', new_directory+"/ellfish_files"])
subprocess.run(['mkdir', new_directory+"/other"])

for n, i in enumerate(values):
    print("Running Value {:.3f} ({}/{})".format(i, n+1, len(values)))
    with open(file_name, 'r') as input_file, open('{:.3f}.ell'.format(i), 'w') as output_file:
        for line in input_file:
            if re.match('^FILEname_prefix', line.strip()):
                output_file.write("FILEname_prefix \t\t\t {:.3f}\n".format(i))
            elif re.match('^'+property, line.strip()):
                output_file.write(property + " \t\t\t{:.3f}\n".format(i))
            else:
                output_file.write(line)

    subprocess.run(['wine', 'ELLFISH', '{:.3f}.ell'.format(i)])

    # Move files to appropriate directory
    subprocess.call('mv *.SFO {}/results/'.format(new_directory), shell=True)
    subprocess.call('mv *.T35 {}/plots/'.format(new_directory), shell=True)
    subprocess.call('mv *.SEG {}/mesh/'.format(new_directory), shell=True)
    subprocess.call('mv *.AM {}/mesh/'.format(new_directory), shell=True)
    subprocess.call('mv *.ell {}/ellfish_files/'.format(new_directory), shell=True)
    subprocess.call('mv *.LOG {}/other/'.format(new_directory), shell=True)
    subprocess.call('mv *.TXT {}/other/'.format(new_directory), shell=True)
    subprocess.call('mv *.INF {}/other/'.format(new_directory), shell=True)