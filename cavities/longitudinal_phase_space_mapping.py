#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 00:08:57 2018

@author: dave
"""
import matplotlib.pyplot as plt
import numpy as np
import pint
pq = pint.UnitRegistry()

# %%
# Define functions for calculating changes in phase and energy deviation

def phase_advance(h, slippage, gamma, dE, total_energy):
    beta = np.sqrt(1-1/gamma**2)
    return 2*np.pi*h*slippage/(total_energy * beta**2) * dE

def energy_gain(V0, phi, phi_s, charge):
    return charge*V0 * (np.sin(phi) - np.sin(phi_s))

def slippage(kinetic_energy, momentum_compaction):
    g = gamma(kinetic_energy, mass)
    return momentum_compaction - 1/g**2

def gamma(kinetic_energy, mass):
    gamma = ((kinetic_energy + mass*pq.c**2)/(mass*pq.c**2)).to(pq.dimensionless)
    return gamma


# %%

# Specify some RF constants
phi_s = 30*pq.degree
h = 1 * pq.dimensionless
V0 = 100*pq.kV

# Specify some constants of the beam properties
mass = 1*pq.m_p
charge = 1*pq.e

# Initial Parameters
initial_kinetic_energy = 45*pq.MeV
phi_0 =  135*pq.degree
dE_0 = 0.000 * initial_kinetic_energy

# Specify some simulation properties
number_of_turns = 500


# %%
# Run through the simulation
kinetic_energy = np.zeros(number_of_turns) * pq.GeV
dE = np.zeros(number_of_turns) * pq.GeV
phi = np.zeros(number_of_turns) * pq.radian

kinetic_energy[0] = initial_kinetic_energy
dE[0] = dE_0
phi[0] = phi_0

for i in range(1, number_of_turns):
    kinetic_energy[i] = kinetic_energy[i-1] + charge * V0 * np.sin(phi_s)
    dE[i] = dE[i-1] + energy_gain(V0, phi[i-1], phi_s, charge)
    dphi = phase_advance(h = h,
                         slippage=slippage(kinetic_energy[i], 0.04340),
                         gamma = gamma(kinetic_energy[i], mass),
                         dE = dE[i],
                         total_energy = kinetic_energy[i] + mass*pq.c**2).to(pq.radian)
    phi[i] = phi[i-1] + dphi

# %%
# Plot the result
plt.plot(phi.to(pq.radian), dE/kinetic_energy)
plt.grid()
plt.xlabel("Phase (degree)")
plt.ylabel(r"Fractional Kinetic Energy")
plt.show()
