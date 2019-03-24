# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:19:45 2019
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib2tikz import save as tikz_save

# %%
# Load field-on-axis data from an SFO file.

filename = 'HALF_CAVITY1.SFO'
with open(filename) as f:
    content = f.readlines()

# Find lines where field on axis starts and ends
start = 0
stop = 0
for n, i in enumerate(content):
    if i.find('Electric field along R') > -1:
        start = n + 4

    if i.find('Total cavity stored energy') > -1:
        stop = n-1

# Extract Superfish data from SFO file

sf_axis_e_field = np.zeros((stop - start, 2))
for n, i in enumerate(content[start:stop]):
    temp = i.strip(' ')
    split = temp.find(' ')
    sf_axis_e_field[n, 0] = temp[0:split]
    sf_axis_e_field[n, 1] = temp[split:]

# %% Field scaling function
# CST uses a stored energy of 1 J, but superfish uses whatever is required for
# the requested field. Copy the stored field from SUPERFISH and scale the CST
# result for comparison.

superfish_stored_E = 115.3699795 * 2  # times two since superfish is half-cell
cst_stored_E = 1


def scale_field(stored_sf_energy, field, cst_stored_energy=1):
    '''
    CST Fields must be scaled to match the stored energy density in the
    superfish model. This comes from U = 0.5 * epsilon_0 * E^2.
    '''
    return field * np.sqrt(stored_sf_energy) / np.sqrt(cst_stored_energy)


# %% Load CST E Field on axis

# Load the field data
cst_axis_e_field = np.genfromtxt('cst_field_on_axis.txt',
                                 skip_header=3, delimiter='\t')

# Scale the field
scaled_cst_field = scale_field(superfish_stored_E, cst_axis_e_field[:, 1])


# %% Shunt Impedance
# Verify that superfish uses ZTT rather than Rs for r/Q

Q = 0.9055e10   # Quality factor, taken from SFO file
TTF = 0.61744   # transit time factor, taken from SFO file
half_length = 0.375  # m, value from SF, IMPORTANT: THIS IS HALF CELL LENGTH
power = 16.0165  # W, dissipated power, taken from SUPERFISH SFO file

# Integrate field on axis to get total voltage for **HALF** cavity
sf_voltage = np.trapz(sf_axis_e_field[:, 1],
                      x=sf_axis_e_field[:, 0]*1e-2)  # Ohm

# Calculate the accelerating field
sf_E_acc = sf_voltage / half_length / 1e6  # MV/m

# Calculate the shunt impedance from calculated voltage
Rs = sf_voltage**2/power/half_length

# Include the transit-time factor
ztt = Rs*TTF**2

# Compare results for r/Q and ztt/Q
print("Rs \t\t= {:.2e} Ohm/m".format(Rs))
print("R*L/Q \t\t= {:.2f} Ohm".format(Rs*half_length/Q))
print("ZTT*L/Q \t= {:.2f} Ohm".format(ztt*half_length/Q))

# %%
# Plot superfish field on axis and scaled CST field

plt.figure(figsize=(8, 6))
plt.plot(sf_axis_e_field[:, 0], sf_axis_e_field[:, 1]/1e6, linewidth=5, label='SUPERFISH')
plt.plot(cst_axis_e_field[:, 0], scaled_cst_field/1e6, '--', linewidth=3, label='CST Eigenmode Solver')
plt.ylabel(r"$E_z$ (MV/m)")
plt.xlabel("Z Position (cm)")
plt.grid()
plt.legend(loc=0)
plt.tight_layout()
# plt.savefig('E_z_on_axis.eps', bbox_inches='tight')
tikz_save("field_on_axis.tex", figurewidth='5cm')
plt.show()

print("\n")

# %% "Accelerating Field"
# This comes from the voltage eigenmode post-processing step without
# accounting for beta.

# Calculate the voltage by integrating the E field along the axis
# Multiply by 2 because this output file is only for half a cell
# divide by 1E6 for MV. The position column in the CST output file is in cm
# hence the /1e2.
cst_voltage = 2*np.trapz(cst_axis_e_field[:, 1],
                         x=cst_axis_e_field[:, 0]/1e2)/1e6

# Scale the field for the different stored energies
scaled_cst_voltage = cst_voltage * np.sqrt(superfish_stored_E)

# The accelerating field is the total voltage divided by the cavity "length"
scaled_cst_E_acc = scaled_cst_voltage/(2*half_length)

print("SUPERFISH Accelerating E Field \t= {:.2f} MV/m".format(sf_E_acc))
print("CST Scaled Accelerating E Field = {:.2f} MV/m".format(scaled_cst_E_acc))
print("\n")


# %%
# Compare the peak surface electric field

sf_peak_e_field = 12.8655       # From output SFO file
cst_peak_e_field = 8.518e5/1e6  # divide by 1e6 for MV/m, from CST postprocessing (Max field on face)
scaled_cst_peak_e_field = cst_peak_e_field * np.sqrt(superfish_stored_E)

print('Superfish Peak Surface E Field \t= {:.2f} MV/m'.format(sf_peak_e_field))
print('CST Peak Surface E Field \t= {:.2f} MV/m'.format(scaled_cst_peak_e_field))
print('Peak E percentage different \t= {:.2%}'.format(
    (scaled_cst_peak_e_field - sf_peak_e_field)/sf_peak_e_field))
print("SUPERFISH E_pk/E_ac \t\t= {:.2f}".format(sf_peak_e_field/sf_E_acc))
print("CST E_pk/E_acc \t\t\t= {:.2f}".format(scaled_cst_peak_e_field / scaled_cst_E_acc))
print("\n")

# %%
# Compare the peak surface H field

sf_peak_h_field = 30971.1     # A/m, from output SFO file
cst_peak_h_field = 2099.6893  # A/m, from CST postprocessing step
scaled_cst_peak_h_field = cst_peak_h_field * np.sqrt(superfish_stored_E)

# Calculate B from H, convert to millitesla
sf_peak_b_field = 4*np.pi*1e-7 * sf_peak_h_field * 1e3                  # mT
scaled_cst_peak_b_field = 4*np.pi*1e-7 * scaled_cst_peak_h_field * 1e3  # mT

print('Superfish Peak Surface H Field \t= {:.2f} A/m'.format(sf_peak_h_field))
print('CST Peak Surface H Field \t= {:.2f} A/m'.format(scaled_cst_peak_h_field))
print('Peak H percentage different \t= {:.2%}'.format(((scaled_cst_peak_h_field - sf_peak_h_field) / sf_peak_h_field)))
print("SUPERFISH B_pk/E_acc \t\t= {:.2f} mT/(MV/m)".format(sf_peak_b_field / sf_E_acc))
print("CST B_pk/E_acc \t\t\t= {:.2f} mT/(MV/m)".format(scaled_cst_peak_b_field / scaled_cst_E_acc))

