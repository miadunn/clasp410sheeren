#!/usr/bin/env python3
'''
This file contains tools and methods for solving our heat/diffusion equation, and 
applying the model to Kangerlussuaq, Greenland.

To reproduce figures in the lab write-up, run the following commands:

Figure 1: run Lab4.py
Figure 2: plot_kanger()
Figure 3: plot_profile(tmax=14600)
Figure 4: plot_kanger(tmax=14600)
Figure 5: plot_profile_05(tmax=14600)
          plot_profile_1(tmax=14600)
          plot_profile_3(tmax=14600)

'''

import numpy as np
import matplotlib.pyplot as plt

def heatdiff(xmax, tmax, dx, dt, c2=1, debug=False, kanger=False, kanger_cc=0):
    '''
    Solve the heat equation, and returns the spatial grid, time grid and array of tempertures in °C.
    Parameters:
    ===========
    xmax: int
        The maximum value of the ground depth in meters.
    tmax: int
        The maximum time value in seconds by default, measured in days 
        when the model is applied to Greenland.
    dx: int
        The change in ground depth in m.
    dt: int
        The change in time step in seconds by default, measured in days
        when the model is applied to Greenland.
    c2: int, default=1
        diffusivity constant, in m^2/s by default, 
        in m2/day when the model is applied to Greenland. 
    debug: boolean, default=False
        Turn on debug output. 
    kanger: boolean, default=False
        Set to true when the model is being applied to Kangerlussuaq, Greenland.

    Returns:
    ========
    xgrid: Numpy array of size M
        Array of ground depths from 0m (at the surface) to xmax.
    tgrid: Numpy array of size N
        Array of times from 0 to tmax.
    U: Numpy array of temperatures in °C.
        Array of temperatures from the surface of the earth to at xmax.

    '''
    #If we are applying the heat diffusion function to Greenland, convert the units from those for the 
    #permafrost thermal diffusivity, which are in mm^2/s, to m^2/day
    sec_to_days = 24*60*60
    mm2_to_m2 = 10**6


    if kanger or kanger_cc:
        c2 = (0.25*sec_to_days)/mm2_to_m2
    #Checking to see if selected criteria is numerically stablle or not:
    if dt > dx**2 / (2*c2):
        raise ValueError('dt is too large! Must be less than dx^2 / (2*c2) for stability')
    #Start by calculating size of array: MxN
    M = int(np.round(xmax / dx + 1))
    N = int(np.round(tmax / dt + 1))
    

    xgrid, tgrid = np.arange(0, xmax+dx, dx), np.arange(0, tmax+dt, dt)
    

    #Debugging commands utilized when debug is set to True:
    if debug:
        print(f'Our grid goes from 0 to {xmax}m and 0 to {tmax}s')
        print(f'Our spatial step is {dx} and our time step is {dt}')
        print(f'There are {M} points in space and {N} points in time.')
        print('Here is our spatial grid:')
        print(xgrid)
        print('Here is our time grid: ')
        print(tgrid)

    #Initialize our data array:
    U = np.zeros((M, N))

    #Set boundary conditions depending on if the model is being applied to Greenland or not:
    if kanger:
        kanger_temperature = t_kanger + kanger_cc
        kanger_surface_temps = temp_kanger(tgrid, kanger_temperature)
        for i, temp in enumerate(kanger_surface_temps):
            U[0, i] = temp
        U[-1,:] = 5
    
    
    else:
        U[0, :] = 0
        U[-1, :] = 0

        #Set initial conditions:
        U[:, 0] = 4*xgrid - 4*xgrid**2

    #Set our "r" constant:
    r = c2 * dt / dx**2

    #Solve! Forward difference ahoy.
    for j in range(N-1):
        U[1:-1, j+1] = (1-2*r) * U[1:-1, j] + \
        r * (U[2:, j] + U[:-2, j])

    #Return grid and result:
    return xgrid, tgrid, U
        
# Kangerlussuaq average temperature:
t_kanger = np.array([-19.7, -21.0, -17, -8.4, 2.3, 8.4,
10.7, 8.5, 3.1, -6.0, -12.0, -16.9])
t_kanger_05 = np.array([-19.7, -21.0, -17, -8.4, 2.3, 8.4,
10.7, 8.5, 3.1, -6.0, -12.0, -16.9]) + 0.5
t_kanger_1 = np.array([-19.7, -21.0, -17, -8.4, 2.3, 8.4,
10.7, 8.5, 3.1, -6.0, -12.0, -16.9]) + 1
t_kanger_3 = np.array([-19.7, -21.0, -17, -8.4, 2.3, 8.4,
10.7, 8.5, 3.1, -6.0, -12.0, -16.9]) + 3
def temp_kanger(t, t_kanger):
    '''
    For an array of times in days, return timeseries of temperature for
    Kangerlussuaq, Greenland.

    Parameters:
    ===========
    t: Numpy array
        Array of times in days.

    Returns: 
    ========
    temperatures: Numpy array of temperatures in °C.
        Array of temperatures for Kangerlussuaq, Greenland.
    '''
    time = t-1
    t_amp = (t_kanger - t_kanger.mean()).max()
    temperature = t_amp*np.sin(np.pi/180 * time - np.pi/2) + t_kanger.mean()
    return temperature

#Appling heat diffusion model to the validation problem:
x, time, heat = heatdiff(1, 0.2, 0.04, 0.0002)
print(heat)
#Plotting the heatmap for our solution to the validation problem:
plt.clf()
plt.pcolor(time, x, heat, shading='nearest')
plt.title("Solver Validation Heat Map")
plt.xlabel('Time(s)')
plt.ylabel('Position (m)')
plt.tight_layout()
plt.colorbar(label='Temperature (°C)')
plt.show()

def plot_kanger(xmax=100, tmax=1825, dx=0.1, dt=0.2):
    '''
    Plotting the space-time heat map for Kangerlussuaq, Greenland.
    Parameters:
    ===========
    xmax: int
        The maximum value of the ground depth in meters.
    tmax: int
        The maximum time value in seconds by default, measured in days 
        when the model is applied to Greenland.
    dx: int
        The change in ground depth in m.
    dt: int
        The change in time step in seconds by default, measured in days
        when the model is applied to Greenland.
    '''
    position, time, temp = heatdiff(xmax, tmax, dx, dt, kanger=True)
    print(temp)
    print(position)
    print(time)
    #Creating heat map plot
    plt.clf()
    #Only plotting every ten points in order to conserve computer memory:
    plt.pcolor((time/365)[::10], position[::10], temp[::10, ::10], cmap='seismic', vmin=-25, vmax=25)
    plt.gca().invert_yaxis()  # This will invert the y-axis
    plt.title("Ground Temperature: Kangerlussuaq, Greenland")
    plt.xlabel('Time (Years)')
    plt.ylabel('Depth (m)')
    plt.tight_layout()
    plt.colorbar(label='Temperature (°C)')
    plt.show()

    return

def plot_profile(xmax=100, tmax=1825, dx=0.1, dt=0.2):
    '''
    Plotting the seasonal temprature profile for Kangerlussuaq.
    Parameters:
    ===========
    xmax: int
        The maximum value of the ground depth in meters.
    tmax: int
        The maximum time value in seconds by default, measured in days 
        when the model is applied to Greenland.
    dx: int
        The change in ground depth in m.
    dt: int
        The change in time step in seconds by default, measured in days
        when the model is applied to Greenland.
    '''
    position, time, temp = heatdiff(xmax, tmax, dx, dt, kanger=True)
    
    # Set indexing for the final year of results:
    loc = int(-365/dt) # Final 365 days of the result.
    # Extract the minimum and maximum values over the final year:
    winter = temp[:, loc:].min(axis=1)
    summer = temp[:, loc:].max(axis=1)
    #Determining the depth of the active layer:
    summer_active = np.abs(summer[position <= 10])
    summer_permafrost = np.abs(summer[position > 10])
    active_layer_index = np.argmin(summer_active)
    active_layer = position[position <= 10][active_layer_index]
    #Determing the depth of the permafrost layer:
    permafrost_layer_index = np.argmin(summer_permafrost)
    permafrost_layer = position[position > 10][permafrost_layer_index]
    print(active_layer)
    print(permafrost_layer)
    
    # Create a temperature profile plot:
    plt.clf()
    plt.plot(winter, position, label='Winter')
    plt.plot(summer, position, label='Summer', color='red', linestyle='--')

    plt.legend(loc="lower left")
    plt.grid(True)  # Adds a default grid
    plt.xlim(-8,6)
    plt.ylim(0,70)
    plt.gca().invert_yaxis()  # This will invert the y-axis
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Depth (m)')
    plt.title('Ground Temperature: Kangerlussuaq')
    plt.show()

    return


#Steady state is reached after approximately 40 years or 14600 days.

def plot_profile_05(xmax=100, tmax=1825, dx=0.1, dt=0.2):
    '''
    Plotting the seasonal temprature profile with a temperature shift of 0.5°C.
    Parameters:
    ===========
    xmax: int
        The maximum value of the ground depth in meters.
    tmax: int
        The maximum time value in seconds by default, measured in days 
        when the model is applied to Greenland.
    dx: int
        The change in ground depth in m.
    dt: int
        The change in time step in seconds by default, measured in days
        when the model is applied to Greenland.
    '''

    position_05, time_05, temp_05 = heatdiff(xmax, tmax, dx, dt, kanger=True, kanger_cc=0.5)
    
    # Set indexing for the final year of results:
    loc = int(-365/dt) # Final 365 days of the result.
    # Extract the minimum and maximum values over the final year:
    winter_05 = temp_05[:, loc:].min(axis=1)
    summer_05 = temp_05[:, loc:].max(axis=1)
    #Determining the depth of the active layer:
    summer_active_05 = np.abs(summer_05[position_05 <= 10])
    summer_permafrost_05 = np.abs(summer_05[position_05 > 10])
    active_layer_index_05 = np.argmin(summer_active_05)
    active_layer_05 = position_05[position_05 <= 10][active_layer_index_05]
    #Determing the depth of the permafrost layer:
    permafrost_layer_index_05 = np.argmin(summer_permafrost_05)
    permafrost_layer_05 = position_05[position_05 > 10][permafrost_layer_index_05]
    print(active_layer_05)
    print(permafrost_layer_05)
    # Create a temperature profile plot:
    plt.clf()
    plt.plot(winter_05, position_05, label='Winter')
    plt.plot(summer_05, position_05, label='Summer', color='red', linestyle='--')

    plt.legend(loc="lower left")
    plt.grid(True)  # Adds a default grid
    plt.xlim(-8,6)
    plt.ylim(0,70)
    plt.gca().invert_yaxis()  # This will invert the y-axis
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Depth (m)')
    plt.title('Ground Temperature: Kangerlussuaq with 0.5°C Shift')
    plt.show()

    return

def plot_profile_1(xmax=100, tmax=1825, dx=0.1, dt=0.2):
    '''
    Plotting the seasonal temprature profile with a temperature shift of 1°C.
    Parameters:
    ===========
    xmax: int
        The maximum value of the ground depth in meters.
    tmax: int
        The maximum time value in seconds by default, measured in days 
        when the model is applied to Greenland.
    dx: int
        The change in ground depth in m.
    dt: int
        The change in time step in seconds by default, measured in days
        when the model is applied to Greenland.
    '''

    position_1, time_1, temp_1 = heatdiff(xmax, tmax, dx, dt, kanger=True, kanger_cc=1)
    
    # Set indexing for the final year of results:
    loc = int(-365/dt) # Final 365 days of the result.
    # Extract the minimum and maximum values over the final year:
    winter_1 = temp_1[:, loc:].min(axis=1)
    summer_1 = temp_1[:, loc:].max(axis=1)
    #Determining the depth of the active layer:
    summer_active_1 = np.abs(summer_1[position_1 <= 10])
    summer_permafrost_1 = np.abs(summer_1[position_1 > 10])
    active_layer_index_1 = np.argmin(summer_active_1)
    active_layer_1 = position_1[position_1<= 10][active_layer_index_1]
    #Determing the depth of the permafrost layer:
    permafrost_layer_index_1 = np.argmin(summer_permafrost_1)
    permafrost_layer_1 = position_1[position_1 > 10][permafrost_layer_index_1]
    print(active_layer_1)
    print(permafrost_layer_1)
    # Create a temperature profile plot:
    plt.clf()
    plt.plot(winter_1, position_1, label='Winter')
    plt.plot(summer_1, position_1, label='Summer', color='red', linestyle='--')

    plt.legend(loc="lower left")
    plt.grid(True)  # Adds a default grid
    plt.xlim(-8,6)
    plt.ylim(0,70)
    plt.gca().invert_yaxis()  # This will invert the y-axis
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Depth (m)')
    plt.title('Ground Temperature: Kangerlussuaq with 1°C Shift')
    plt.show()

    return

def plot_profile_3(xmax=100, tmax=1825, dx=0.1, dt=0.2):
    '''
    Plotting the seasonal temprature profile with a temperature shift of 3°C.
    Parameters:
    ===========
    xmax: int
        The maximum value of the ground depth in meters.
    tmax: int
        The maximum time value in seconds by default, measured in days 
        when the model is applied to Greenland.
    dx: int
        The change in ground depth in m.
    dt: int
        The change in time step in seconds by default, measured in days
        when the model is applied to Greenland.
    '''

    position_3, time_3, temp_3 = heatdiff(xmax, tmax, dx, dt, kanger=True, kanger_cc=3)
    
    # Set indexing for the final year of results:
    loc = int(-365/dt) # Final 365 days of the result.
    # Extract the minimum and maximum values over the final year:
    winter_3 = temp_3[:, loc:].min(axis=1)
    summer_3 = temp_3[:, loc:].max(axis=1)
    #Determining the depth of the active layer:
    summer_active_3 = np.abs(summer_3[position_3 <= 10])
    summer_permafrost_3 = np.abs(summer_3[position_3 > 10])
    active_layer_index_3 = np.argmin(summer_active_3)
    active_layer_3 = position_3[position_3<= 10][active_layer_index_3]
    #Determing the depth of the permafrost layer:
    permafrost_layer_index_3 = np.argmin(summer_permafrost_3)
    permafrost_layer_3 = position_3[position_3 > 10][permafrost_layer_index_3]
    print(active_layer_3)
    print(permafrost_layer_3)
    # Create a temperature profile plot:
    plt.clf()
    plt.plot(winter_3, position_3, label='Winter')
    plt.plot(summer_3, position_3, label='Summer', color='red', linestyle='--')

    plt.legend(loc="lower left")
    plt.grid(True)  # Adds a default grid
    plt.xlim(-8,6)
    plt.ylim(0,70)
    plt.gca().invert_yaxis()  # This will invert the y-axis
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Depth (m)')
    plt.title('Ground Temperature: Kangerlussuaq with 3°C Shift')
    plt.show()

    return

