# coding: utf-8
""" demo on dynamic eit using JAC method """
# Copyright (c) Benyuan Liu. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
from __future__ import absolute_import, division, print_function

import matplotlib.pyplot as plt
import numpy as np
import pyeit.eit.jac as jac
import pyeit.mesh as mesh
from pyeit.eit.fem import EITForward
from pyeit.eit.interp2d import sim2pts
from pyeit.mesh.shape import thorax, unit_circle
import pyeit.eit.protocol as protocol
from pyeit.mesh.wrapper import PyEITAnomaly_Circle

import serial
from datetime import datetime
import time
from matplotlib.animation import FuncAnimation

"""-2. Initial vars """
arduino = serial.Serial('COM8', 115200 ,timeout=4)
v0 = np.loadtxt('examples/example_data/ref_data.txt')
fig, ax = plt.subplots(constrained_layout=True)
n_el = 16
"""-1. Functions """

def readfromArduino():
    while(True):
        try:
            data = arduino.readline().decode('ascii')
            print("data: ", data)
            break
        except UnicodeDecodeError:
            print("UnicodeDecodeError found! Retrying...")
            continue
    return data

def get_difference_img_array(n_el = n_el, NewFrameSearchFlag = 1, idx = 0):
    difference_image_array = ''
    # Read difference image f1:
    while idx < n_el:
        data = readfromArduino()
        #skip until the empty line is found to catch the whole frame
        while(NewFrameSearchFlag == 1):
            if len(data) > 4:
                print("Searching for new frame.")
                data = readfromArduino()
                continue
            else:
                print("New frame found.")
                data = readfromArduino()
                NewFrameSearchFlag = 0
                break


        data=data.strip('\r\n')
        difference_image_array += data
        difference_image_array += ' '
        idx = idx + 1
        #print("String: {0}".format(data))
 
    return difference_image_array

def convert_data_in(s):
    data=s
    items=[]
    for item in data.split(' '):
        item = item.strip()
        if not item:
            continue
        try:
            items.append(float(item))
        except ValueError:
            print("Value Error found! Handling...")
            items.append(float(0))
    return np.array(items)


""" 0. build mesh """
n_el = 16  # nb of electrodes
use_customize_shape = False
if use_customize_shape:
    # Mesh shape is specified with fd parameter in the instantiation, e.g : fd=thorax
    mesh_obj = mesh.create(n_el, h0=0.08, fd=thorax)
else:
    mesh_obj = mesh.create(n_el, h0=0.08)

# extract node, element, alpha
pts = mesh_obj.node
tri = mesh_obj.element
x, y = pts[:, 0], pts[:, 1]

""" 1. problem setup """
# mesh_obj["alpha"] = np.random.rand(tri.shape[0]) * 200 + 100 # NOT USED
anomaly = PyEITAnomaly_Circle(center=[0.5, 0.5], r=0.1, perm=1000.0)
mesh_new = mesh.set_perm(mesh_obj, anomaly=anomaly)

""" 2. FEM simulation """
# setup EIT scan conditions
protocol_obj = protocol.create(n_el, dist_exc=1, step_meas=1, parser_meas="std")

# calculate simulated data
fwd = EITForward(mesh_obj, protocol_obj)

#v0 = fwd.solve_eit()
#v1 = fwd.solve_eit(perm=mesh_new.perm)
""" 3. JAC solver """
# Note: if the jac and the real-problem are generated using the same mesh,
# then, data normalization in solve are not needed.
# However, when you generate jac from a known mesh, but in real-problem
# (mostly) the shape and the electrode positions are not exactly the same
# as in mesh generating the jac, then data must be normalized.
eit = jac.JAC(mesh_obj, protocol_obj)
eit.setup(p=0.5, lamb=0.8, method="kotre", perm=1000, jac_normalized=True)

def animating(i):  
    while arduino.inWaiting()==0:
        print("waiting")
        time.sleep(0.5)
        pass
    time_start_0 = time.time()

    s1 = get_difference_img_array()
    time_end_0 = time.time()
    print("Get diff arr: ", time_end_0 - time_start_0)   

    time_start_0 = time.time()
    v1 = convert_data_in(s1)
    time_end_0 = time.time()
    print("Convert data: ", time_end_0 - time_start_0)

    time_start_0 = time.time()
    try:
        ds = eit.solve(v1, v0, normalize=True)
    except Exception as e:
        ani.event_source.stop()  # Stop the current animation
        ani.event_source.start()  # Start a new animation
    time_end_0 = time.time()
    print("Solve: ", time_end_0 - time_start_0)
    
    time_start_0 = time.time()
    ds_n = sim2pts(pts, tri, np.real(ds))
    time_end_0 = time.time()
    print("sim2pts: ", time_end_0 - time_start_0)   
    # plot ground truth
    ax.clear()
    time_start_0 = time.time()
    # plot EIT reconstruction
    im = ax.tripcolor(x, y, tri, ds_n, shading="flat")
    for i, e in enumerate(mesh_obj.el_pos):
        ax.annotate(str(i + 1), xy=(x[e], y[e]), color="r")
    ax.set_aspect("equal")
    time_end_0 = time.time()
    print("plot: ", time_end_0 - time_start_0)
    # plt.savefig('../doc/images/demo_jac.png', dpi=96)

ani = FuncAnimation(fig, animating, interval = 100, cache_frame_data= False)
plt.show()
