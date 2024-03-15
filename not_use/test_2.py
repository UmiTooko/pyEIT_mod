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


def main():
    arduino = serial.Serial('COM9', 115200 ,timeout=4)
    fig, ax = plt.subplots()
    
    line, = ax.plot([], [], 'b-')

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

    def animating(i):
        data_array = readfromArduino()
        ax.set_xlim(0, len(data_array))
        ax.set_ylim(0, 1) 
        arduino.write("f")

    ani = FuncAnimation(fig, animating, fargs=(1,), interval = 1000, cache_frame_data= False)
    plt.show()

if __name__ == "__main__":
    main()