'''
This finds all the .SFO files in a directory, and extracts a few properties
from them and plots them.

The directory which is specified should contain all the SFO files for a
sweep of a single parameter. The filenames should be the value of that parameter
with the additional 1.SFO which is automatically added by ELLFISH
    For example if I vary Wall Angle from 5 degrees to 7 degrees in steps of
    1 degree, then the directory should contain only
    51.SFO
    61.SFO
    71.SFO

    or

    5.001.SFO
    6.001.SFO
    7.001.SFO
'''
import os.path as path
import numpy as np
import matplotlib.pyplot as plt
import glob

# %%
# User defined variables

# Wall Angle
#directory = "wall_angle/results/"
#parameter_name = "Wall Angle (degree)"

# Right Dome B
#directory = "right_dome_b/results/"
#parameter_name = "Right Dome B (cm)"

# Dome A/B
#directory = "dome_a_over_b/results/"
#parameter_name = "Dome A/B"

directory = "iris_a_over_b/results/"
parameter_name = "Iris A/B"


# %%
# End of User Variables

# Find list of results files, filenames are the values of the parameter
# file extensions are 1.SFO so must remove the last five characters
# Ordinary sorting functions would sort "1","5","10","11" -> "1","10","11","5"
# to fix this we sort based on a key function, the key function is run on all
# elements and then the list is sorted based on the sorting of those elements.
# We just extract the number from the filename and then sort numerically.
results = glob.glob('{}*.SFO'.format(directory))
results.sort(key=lambda f: float(path.split(f)[1][:-5]))

# Make a list of parameter values from the now sorted results array
parameter = np.array([float(path.split(i)[1][:-5]) for i in results])

# Make empty arrays to fill in
shunt_impedance = np.zeros(len(results))
max_h = np.zeros(len(results))
roverQ = np.zeros(len(results))
wake_loss_parameter = np.zeros(len(results))
transit_time = np.zeros(len(results))

# %%
# Loop through all files, read the text, pick out the value and place it in
# the corresponding array.
for n, i in enumerate(results):
    print(i)
    with open(i) as f:

        # The output file is large but the properties I currently want to
        # plot are in the last section. To avoid multiple instances of the
        # search terms I'll "select" the last part of the fileself.
        text = f.read()
        text = text.split("All calculated values below refer to the mesh geometry only.")[1]

        temp = float(text.split("Shunt impedance")[1].split("=")[1].split("MOhm/m")[0])
        shunt_impedance[n] = temp
        temp = 0

        temp = float(text.split("Maximum H ")[1].split("=")[2].split("A/m")[0])
        max_h[n] = temp
        temp = 0

        temp = float(text.split("r/Q")[1].split("=")[1].split("Ohm")[0])
        roverQ[n] = temp
        temp = 0

        temp = float(text.split("Wake loss parameter")[1].split("=")[1].split("V/pC")[0])
        wake_loss_parameter[n] = temp
        temp = 0

        temp = float(text.split("Transit-time factor")[1].split("=")[1].split("\n")[0])
        transit_time[n] = temp
        temp = 0


# %%
# Plots

plt.figure()
plt.plot(parameter, shunt_impedance, '-o')
plt.xlabel(parameter_name)
plt.ylabel("Shunt Impedance (MOhm/m)")
plt.tight_layout()
plt.grid()
#plt.savefig('plots/shunt_impedance.png', bbox_inches='tight')
plt.show()

plt.figure()
plt.plot(parameter, max_h, '-o')
plt.xlabel(parameter_name)
plt.ylabel("Max H (A/m)")
plt.tight_layout()
plt.grid()
#plt.savefig('plots/max_h.png', bbox_inches='tight')
plt.show()

plt.figure()
plt.plot(parameter, roverQ, '-o')
plt.xlabel(parameter_name)
plt.ylabel("r/Q (ohm)")
plt.tight_layout()
plt.grid()
#plt.savefig('plots/rOverQ.png', bbox_inches='tight')
plt.show()

plt.figure()
plt.plot(parameter, wake_loss_parameter, '-o')
plt.xlabel(parameter_name)
plt.ylabel("Wake Loss Parameter (V/pC)")
plt.tight_layout()
plt.grid()
#plt.savefig('plots/wake_loss_parameter.png', bbox_inches='tight')
plt.show()

plt.figure()
plt.plot(parameter, transit_time, '-o')
plt.xlabel(parameter_name)
plt.ylabel("Transit Time Factor")
plt.tight_layout()
plt.grid()
#plt.savefig('plots/transit_time.png', bbox_inches='tight')
plt.show()
