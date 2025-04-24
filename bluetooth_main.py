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

""" -3. CLI """
def parse_args():
    parser = argparse.ArgumentParser(description="University of Engineering and Technology VNU - Electronic Impedance Tomography")
    parser.add_argument("--port", type=str, required=True, help="Serial port for Arduino.")
    parser.add_argument("--ref", help="Measure ref_data.", default = False, action="store_true")
    parser.add_argument("--n_el", type = int,help="Number of electrodes.", default = 16)

    parser.add_argument("--h0", type = float, help="Mesh size.", default = 0.06)
    parser.add_argument("--p", type = float, help="Value p in Jacobian.", default = 0.2)
    parser.add_argument("--lamb", type = float, help="Value lambda in Jacobian.", default = 0.005)
    parser.add_argument("--baud", type = float, help="Baudrate.", default = 115200)
    return parser.parse_args()


def main():

    arg = parse_args()

    """-2. Initial vars """
    print("Chương trình đang được khởi chạy, vui lòng chờ...\n")
    time.sleep(2)

    arduino = serial.Serial(arg.port, 115200 ,timeout=7)
    time.sleep(2)
    fig, ax = plt.subplots(constrained_layout=True)
    n_el = arg.n_el


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
                #print(data)
                break
            except UnicodeDecodeError:
                print("UnicodeDecodeError found! Retrying...")
                continue
        return data
    

    
    def get_difference_img_array(n_el = n_el, NewFrameSearchFlag = 1, idx = 0):
        difference_image_array = ''
        # Read the voltage data:
        while idx < n_el:
            data = readfromArduino()
            #Skip until the header (which is a single character 's') is found
            while(NewFrameSearchFlag == 1):
                if len(data) > 30:
                    print("Searching for new frame.")
                    data = readfromArduino()
                    continue
                else:
                    print("New frame found.")
                    data = readfromArduino()
                    NewFrameSearchFlag = 0
                    break
            #Start to take the data right after the header, by doing so, no loss of frame should occurred
            data=data.strip('\r\n')
            difference_image_array += data
            difference_image_array += ' '
            idx = idx + 1
            
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
            #Handle any unexpected error regarding value so the program won't quit
            except ValueError:
                print("Value Error found! Handling...")
                items.append(float(0))
        return np.array(items)

 
    mesh_obj = mesh.create(n_el, h0=arg.h0)

    # extract node, element, alpha
    pts = mesh_obj.node
    tri = mesh_obj.element
    x, y = pts[:, 0], pts[:, 1]

    protocol_obj = protocol.create(n_el, dist_exc=1, step_meas=1, parser_meas="fmmu")
    cmap=plt.cm.magma

    eit = jac.JAC(mesh_obj, protocol_obj)
    if arg.truth == True:
        arg.perm = 10
    eit.setup(p=arg.p, lamb=arg.lamb, method="kotre", perm = arg.perm, jac_normalized=True)

    arduino.write('f'.encode('utf-8'))                  #Send first finish flag to start the arduino

    def animating(i):  
        arduino.write('f'.encode('utf-8'))

        #s_time = time.time()
        print("The time when it starts calculating = ", time.time())
        while arduino.inWaiting()==0:
            #print("waiting")
            pass

        s1 = get_difference_img_array()

        v1 = convert_data_in(s1)
        try:
            ds = eit.solve(v1, v0, normalize=True)
            ds_n = sim2pts(pts, tri, np.real(ds))
        
        except Exception as e:
                print("Data error, try again!")
                return
        #fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
        #axs[0].hist(ds_n, bins=100)

        #print("Run time until the calculation is finished = {}\n".format(time.time() - s_time))
        print("Run time until the calculation is finished = {}\n".format(time.time()))



        im = ax.tripcolor(x, y, tri, ds_n, shading="flat", cmap=cmap)

        for i, e in enumerate(mesh_obj.el_pos):
            ax.annotate(str(i + 1), xy=(x[e], y[e]), color="r")
        ax.set_aspect("equal")
        plt.title("p = {} | lambda = {}".format(arg.p, arg.lamb))


        arduino.write('f'.encode('utf-8'))       #Send the finish flag to announce the arduino that the plotting is done

        #print("Sent ", 'f'.encode('utf-8'))
        #print("Run time until the displaying is finished = {}\n".format(time.time() - s_time))
        print("Run time until the displaying is finished = {}\n".format(time.time()))


        s1 = get_difference_img_array()
        ref_v = ''
        with open('data/ref_data.txt', 'w') as f:
            for val in s1:
                ref_v +=val
            f.write(ref_v)
        return
   
    if 1:
        ani = FuncAnimation(fig, animating, fargs=(1,), interval = arg.interval, cache_frame_data= False)
        plt.show()

if __name__ == "__main__":
    main()