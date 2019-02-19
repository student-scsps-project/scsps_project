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

class ellfish_result():
    def __init__(self, directory, parameter_name):
        self.__directory = directory
        self.__parameter_name = parameter_name

        # Make empty arrays to fill in
        self.__results_list = self.results_file_list()
        self.__shunt_impedance = np.zeros(len(self.__results_list))
        self.__max_h = np.zeros(len(self.__results_list))
        self.__roverQ = np.zeros(len(self.__results_list))
        self.__wake_loss_parameter = np.zeros(len(self.__results_list))
        self.__transit_time = np.zeros(len(self.__results_list))
        self.__ztt= np.zeros(len(self.__results_list))
        self.extract_results_from_files()

    def results_file_list(self):
        '''
        Obtains a list of all the SFO files in the provided directory
        '''
        # Find list of results files, filenames are the values of the parameter
        # file extensions are 1.SFO so must remove the last five characters
        # Ordinary sorting functions would sort "1","5","10","11" -> "1","10","11","5"
        # to fix this we sort based on a key function, the key function is run on all
        # elements and then the list is sorted based on the sorting of those elements.
        # We just extract the number from the filename and then sort numerically.
        results = glob.glob('{}*.SFO'.format(self.__directory))
        results.sort(key=lambda f: float(path.split(f)[1][:-5]))
        return results

    def parameter_list(self):
        results = self.results_file_list()
        # Make a list of parameter values from the now sorted results array
        parameter = np.array([float(path.split(i)[1][:-5]) for i in results])
        return parameter

    def extract_results_from_files(self):
        # Loop through all files, read the text, pick out the value and place it in
        # the corresponding array.
        for n, i in enumerate(self.__results_list):
            with open(i) as f:

                # The output file is large but the properties I currently want to
                # plot are in the last section. To avoid multiple instances of the
                # search terms I'll "select" the last part of the fileself.
                text = f.read()
                text = text.split("All calculated values below refer to the mesh geometry only.")[1]

                temp = float(text.split("Shunt impedance")[1].split("=")[1].split("MOhm/m")[0])
                self.__shunt_impedance[n] = temp
                temp = 0

                temp = float(text.split("Z*T*T")[1].split("=")[1].split("MOhm/m")[0])
                self.__ztt[n] = temp
                temp = 0

                temp = float(text.split("Maximum H ")[1].split("=")[2].split("A/m")[0])
                self.__max_h[n] = temp
                temp = 0

                temp = float(text.split("r/Q")[1].split("=")[1].split("Ohm")[0])
                self.__roverQ[n] = temp
                temp = 0

                temp = float(text.split("Wake loss parameter")[1].split("=")[1].split("V/pC")[0])
                self.__wake_loss_parameter[n] = temp
                temp = 0

                temp = float(text.split("Transit-time factor")[1].split("=")[1].split("\n")[0])
                self.__transit_time[n] = temp
                temp = 0

    def shunt_impedance(self):
        return self.__shunt_impedance

    def max_h(self):
        return self.__max_h

    def rOverQ(self):
        return self.__roverQ

    def wake_loss(self):
        return self.__wake_loss_parameter

    def transit_time(self):
        return self.__transit_time

    def ztt(self):
        return self.__ztt

    def properties(self):
        '''
        Returns a list of the extracted cavity properties and a name for each
        of them in the same order.
        '''
        property_name = ["Shunt Impedance (MOhm/m)", "ZTT (MOhm/m)",
                         "Max H (A/m)", "r/Q (Ohm)", "Wake Loss Parameter (V/pC)",
                         "Transit Time Factor"]
        properties = [self.shunt_impedance, self.ztt, self.max_h, self.rOverQ,
                      self.wake_loss, self.transit_time]
        return (property_name, properties)

    def parameter_name(self):
        return self.__parameter_name


def percent_diff(array):
    return (array-array[0])/array[0]*100

def plot_all_results(ellfish_res, save=False, directory=None, percentage=False):
    '''
    Plots all of the extracted cavty properties.
    '''
    if directory == None:
        save = False

    a, b = ellfish_res.properties()
    for name, func in zip(a, b):
        plt.figure()
        if percentage == True:
            plt.plot(ellfish_res.parameter_list(), percent_diff(func()), '-o')
            plt.ylabel("Percentage Difference")
            name += "_-_PERCENTAGE"
        else:
            plt.plot(ellfish_res.parameter_list(), func(), '-o')
            plt.ylabel(name)
        plt.xlabel(ellfish_res.parameter_name())
        plt.grid()
        plt.tight_layout()
        if save == True:
            plt.savefig(path.join(directory, name.replace('/', 'OVER')+'.png'), bbox_inches='tight')
        plt.show()

# %%
# User defined variables

# Wall Angle
directory = "wall_angle/results/"
parameter_name = "Wall Angle (degree)"
wall_angle = ellfish_result(directory, parameter_name)
del(directory)
del(parameter_name)

# Right Dome B
directory = "right_dome_b/results/"
parameter_name = "Right Dome B (cm)"
right_dome = ellfish_result(directory, parameter_name)
del(directory)
del(parameter_name)

# Dome A/B
directory = "dome_a_over_b/results/"
parameter_name = "Dome A/B"
domeab = ellfish_result(directory, parameter_name)
del(directory)
del(parameter_name)

# IRIS A/B
directory = "iris_a_over_b/results/"
parameter_name = "Iris A/B"
irisab = ellfish_result(directory, parameter_name)
del(directory)
del(parameter_name)


# %%
# Plots

#plot_all_results(wall_angle, False, 'plots/wall_angle')
#plot_all_results(right_dome, False, 'plots/right_dome_b')
#plot_all_results(domeab, False, 'plots/dome_a_over_b')
plot_all_results(irisab, True, 'plots/iris_a_over_b', percentage=False)
plot_all_results(irisab, True, 'plots/iris_a_over_b', percentage=True)
