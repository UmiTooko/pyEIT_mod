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
from matplotlib.colors import TwoSlopeNorm

import argparse
import os
""" -3. CLI """
def parse_args():
    parser = argparse.ArgumentParser(description="University of Engineering and Technology - Electronic Impedance Tomography")
    parser.add_argument("--port", type=str, required=True, help="Serial port for Arduino")
    parser.add_argument("--ref", help="Measure ref_data", default = False, action="store_true")
    parser.add_argument("--h0", type = float, help="Mesh size", default = 0.065)
    parser.add_argument("--p", type = float, help="Value p in Jacobian", default = 0.8)
    parser.add_argument("--lamb", type = float, help="Value lambda in Jacobian", default = 0.02)
    parser.add_argument("--perm", type = float, help="Value permittivity.", default = 1000)


    parser.add_argument("--static", help="Reconstructed 1 frame.", default = False, action="store_true")
    parser.add_argument("--dir", type = str, help="Save figure to a folder (for static and ref mode)")
    parser.add_argument("--realtime", help="Run realtime.", default = False, action="store_true")
    parser.add_argument("--interval", type=int, default=50, help="Animation interval in milliseconds (for realtime mode)")
    return parser.parse_args()

def main():

    arg = parse_args()
    if (arg.ref == True and arg.static == True) or (arg.realtime == True and arg.static == True) or (arg.ref == True and arg.realtime == True):
        print("Chỉ có thể chạy một trong ba chức năng cùng lúc: ref, realtime, static. Hãy thử lại.")
        return
    if (arg.ref == False and arg.static == False and arg.realtime == False):
        print("Hãy chọn một trong ba chức năng: ref, static, realtime.")
        return
    
    if not os.path.exists("images"):
        os.makedirs("images")
        print("Created images folder")
    if not os.path.exists("data"):
        os.makedirs("data")
        print("Created data folder")

    
    """-2. Initial vars """
    arduino = serial.Serial(arg.port, 115200 ,timeout=4)
    fig, ax = plt.subplots(constrained_layout=True)
    n_el = 16
    #norm = TwoSlopeNorm(vcenter=0)

    if(arg.ref == False):
        v0 = np.loadtxt('data/ref_data.txt')

    """-1. Functions """

    '''To read data from Arduino via COM port

    Each frame is 16 lines, each line has 13 value, 
    in total there are 208 values representing the voltage measured from electrodes. 
    '''

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

    #Convert data to np type
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
    mesh_obj = mesh.create(n_el, h0=arg.h0)

    # extract node, element, alpha
    pts = mesh_obj.node
    tri = mesh_obj.element
    x, y = pts[:, 0], pts[:, 1]

    """ 1. problem setup """


    """ 2. FEM simulation """
  
    protocol_obj = protocol.create(n_el, dist_exc=1, step_meas=1, parser_meas="fmmu")

    """ 3. JAC solver """

    eit = jac.JAC(mesh_obj, protocol_obj)
    eit.setup(p=arg.p, lamb=arg.lamb, method="kotre", perm = arg.perm, jac_normalized=True)


    def animating(i, flag):  
        while arduino.inWaiting()==0:
            print("waiting")
            #time.sleep(0.5)
            pass

        s1 = get_difference_img_array()

        v1 = convert_data_in(s1)

        try:
            ds = eit.solve(v1, v0, normalize=True)
        except Exception as e:
            if i == 1:
                ani.event_source.stop()  # Stop the current animation
                ani.event_source.start()  # Start a new animation
            else:
                print("Lỗi dữ liệu, hãy thử lại!")

        ds_n = sim2pts(pts, tri, np.real(ds))
        # Clear the graph after each animating frame
        ax.clear()

        # plot EIT reconstruction
        im = ax.tripcolor(x, y, tri, ds_n, shading="flat", cmap=plt.cm.magma)
        for i, e in enumerate(mesh_obj.el_pos):
            ax.annotate(str(i + 1), xy=(x[e], y[e]), color="r")
        ax.set_aspect("equal")
        #fig.colorbar(im, ax=ax, ticks = [0])




    
    if arg.ref == True:
        while arduino.inWaiting()==0:
            print("waiting")
            time.sleep(0.5)
            pass
        s1 = get_difference_img_array()
        ref_v = ''
        with open('data/ref_data.txt', 'w') as f:
            for val in s1:
                ref_v +=val
            f.write(ref_v)
        return
    elif arg.static == True:
        animating(0, flag = 0)
        plt.savefig('./images/{}__{}__{}.png'.format(str(arg.h0).replace(".", "_"), str(arg.p).replace(".", "_"), str(arg.lamb).replace(".", "_")), dpi=96)
        plt.show()
    elif arg.realtime == True:
        ani = FuncAnimation(fig, animating, fargs=(1,), interval = arg.interval, cache_frame_data= False)
        plt.show()

if __name__ == "__main__":
    main()