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
    '''
    h = harmonic number
    slippage = slippage factor
    gamma = relativistic gamma factor
    dE = energy offset
    total_energy = kinetic energy + rest mass energy
    '''
    beta = np.sqrt(1-1/gamma**2)
    return 2*np.pi*h*slippage/(total_energy * beta**2) * dE

def energy_gain(V0, phi, phi_s, charge):
    return charge*V0 * (np.sin(phi) - np.sin(phi_s))

def slippage(kinetic_energy, momentum_compaction, mass):
    g = gamma(kinetic_energy, mass)
    return momentum_compaction - 1/g**2

def gamma(kinetic_energy, mass):
    gamma = ((kinetic_energy + mass*pq.c**2)/(mass*pq.c**2)).to(pq.dimensionless)
    return gamma

def longitudinal_mapping(initial_kinetic_energy, initial_energy_offset,
                         initial_phase_offset, mass, momentum_compaction,
                         V0, synchronous_phase, h, charge, number_of_turns):
    '''
    mass = particle mass
    momentum_compaction = momentum compaction factor
    numb
    V0 = RF gap voltage magnitude
    synchronous phase = phase of synchronous particle
    h = harmonic number
    charge = particle charge
    number_of_turns = number of turns to simulate
    '''
    kinetic_energy = np.zeros(number_of_turns) * pq.GeV
    dE = np.zeros(number_of_turns) * pq.GeV
    phi = np.zeros(number_of_turns) * pq.radian

    kinetic_energy[0] = initial_kinetic_energy
    dE[0] = initial_energy_offset
    phi[0] = initial_phase_offset

    for i in range(1, number_of_turns):
        kinetic_energy[i] = kinetic_energy[i-1] + charge * V0 * np.sin(synchronous_phase)
        dE[i] = dE[i-1] + energy_gain(V0, phi[i-1], synchronous_phase, charge)
        dphi = phase_advance(h = h,
                             slippage=slippage(kinetic_energy[i], momentum_compaction, mass),
                             gamma = gamma(kinetic_energy[i], mass),
                             dE = dE[i],
                             total_energy = kinetic_energy[i] + mass*pq.c**2).to(pq.radian)
        phi[i] = phi[i-1] + dphi

    return (kinetic_energy, dE, phi)


# %%

if __name__ == '__main__':

    results = longitudinal_mapping(initial_kinetic_energy=45*pq.MeV,
                                   initial_energy_offset=0.000*pq.GeV,
                                   initial_phase_offset=135*pq.degree,
                                   mass=1*pq.m_p,
                                   momentum_compaction=0.04340,
                                   V0=100*pq.kV,
                                   h=1,
                                   synchronous_phase = 30*pq.degree,
                                   charge=1*pq.e,
                                   number_of_turns=500
                                   )
    kinetic_energy, dE, phi = results
    # %%
    # Plot the result
    plt.figure(figsize=(12, 8))
    plt.plot(phi.to(pq.radian), (dE/kinetic_energy).to(pq.dimensionless))
    plt.grid()
    plt.xlabel("Phase (degree)")
    plt.ylabel(r"Fractional Kinetic Energy")
    plt.show()
