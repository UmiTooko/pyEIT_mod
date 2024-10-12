# coding: utf-8
""" demo on dynamic eit using JAC method """
# Copyright (c) Benyuan Liu. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
from __future__ import absolute_import, division, print_function

import time 
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

import numpy as np
import pyeit.eit.jac as jac
import pyeit.mesh as mesh
from pyeit.eit.fem import EITForward
from pyeit.eit.interp2d import sim2pts
from pyeit.mesh.shape import thorax, rectangle, circle
import pyeit.eit.protocol as protocol
from pyeit.mesh.wrapper import PyEITAnomaly_Circle



def amplify_normal_distribution(x, mean, std_dev, start, finish):
    distance_from_mean = np.abs(x - mean)
    amplification_factor = np.clip(1 + distance_from_mean * distance_from_mean / std_dev, start, finish)  # Clip to ensure values stay within desired range
    amplified_value = x * amplification_factor
    return amplified_value

""" 0. build mesh """
n_el = 16  # nb of electrodes

#the higher of p and the lower of lamb -> good shape image. Should be tunning

p = 0.2  
lamb = 0.00005

h0 = 0.06

use_customize_shape = circle # Use "thorax" for thorax shape.

mesh_obj = mesh.create(n_el, h0=h0, fd = use_customize_shape)

# extract node, element, alpha
pts = mesh_obj.node
tri = mesh_obj.element

x, y = pts[:, 0], pts[:, 1]

""" 1. problem setup """
# mesh_obj["alpha"] = np.random.rand(tri.shape[0]) * 200 + 100 # NOT USED
#anomaly = PyEITAnomaly_Circle(center=[0.5, 0.5], r=0.05, perm=1000.0)
#mesh_new = mesh.set_perm(mesh_obj, anomaly=anomaly)

""" 2. FEM simulation """
# setup EIT scan conditions
protocol_obj = protocol.create(n_el, dist_exc=1, step_meas=1, parser_meas="rotate_meas") # use fmmu or rotate_meas

# calculate simulated data
#fwd = EITForward(mesh_obj, protocol_obj)


#v0 = fwd.solve_eit()
#v1 = fwd.solve_eit(perm=mesh_new.perm)

v0 = np.loadtxt('data/ref_data.txt')
v1 = np.loadtxt('data/diff_data.txt')

time_s = time.time()
""" 3. JAC solver """
# Note: if the jac and the real-problem are generated using the same mesh,
# then, data normalization in solve are not needed.
# However, when you generate jac from a known mesh, but in real-problem
# (mostly) the shape and the electrode positions are not exactly the same
# as in mesh generating the jac, then data must be normalized.

eit = jac.JAC(mesh_obj, protocol_obj)
eit.setup(p=p,lamb=lamb, method="kotre", perm=1, jac_normalized=True)
ds = eit.solve(v1, v0, normalize=True, log_scale=False)

#ds = eit.solve_gs(v1, v0)
#ds = eit.jt_solve(v1, v0, normalize=True)
#ds = eit.gn(v1)
ds_n = sim2pts(pts, tri, np.real(ds))

print('ds_n_0=\n', ds_n)
#max_dsn = np.max(ds_n)
#min_dsn = np.min(ds_n)
#
## Avoid division by zero
#ds_n = np.where(ds_n > 0, ds_n / max_dsn, -ds_n / min_dsn)
#
#
#print('ds_n_1=\n', ds_n)
# plot ground truth
#

mean_dsn = np.mean(ds_n)
print("Mean dsn: ", mean_dsn)
std_dsn = np.std(ds_n)
print("Std dsn, ", std_dsn)
print(ds_n)

#fig, axes = plt.subplots(2,2,tight_layout=True)
#axs[0,0].hist(ds_n, bins=100)
#axs[0,0].set_xlim(- max(ds_n) * 1.5, max(ds_n) * 1.5)
#axs[0,0].set_ylim(0, 50)
#quit()
#if 0:
#    print(ds_n)
#    max_dsn = max(ds_n)
#    min_dsn = min(ds_n)
#    
#    average_positive =   1 * mean_dsn + std_dsn * 1
#    average_negative =   1 * mean_dsn - std_dsn * 1
#    #if average_positive < 0.4:
#    #    average_positive +=0.4
#    #if average_negative > -0.4:
#    #    average_negative -=0.4
#    print('avg: ',mean_dsn)
#    print('avg+: ',average_positive)
#    print('avg-: ',average_negative)
#    for i in range(len(ds_n)):
#        if ds_n[i] > average_positive:
#            ds_n[i] = 10 
#        elif ds_n[i] < average_negative:
#            ds_n[i] = -10 
#        else:
#            ds_n[i] = 0
#
if 0:

    average_positive =   1 * mean_dsn + std_dsn * 0.8
    average_negative =   1 * mean_dsn - std_dsn * 0.8
    print("avg+ ",average_positive)
    print("avg- ",average_negative)
    for i in range(len(ds_n)):
        if ds_n[i] > average_positive:
            ds_n[i] = amplify_normal_distribution(ds_n[i], mean_dsn, std_dsn, 1.75,2)
        if ds_n[i] < average_negative:
            ds_n[i] = amplify_normal_distribution(ds_n[i], mean_dsn, std_dsn, 1.75,2)
        else:
            ds_n[i] = amplify_normal_distribution(ds_n[i], mean_dsn, std_dsn, 0.25,.5)

#axs[1].hist(ds_n, bins=100)

#if 0:
#    point_val = []
#    for j in range(499,532):            #Coordinate range for line going from electrode 1 to 9
#        point_val.append(ds_n[j])
#    axs[1,1].plot(np.linspace(0,17,532 - 499),point_val)
#    axs[1,1].set_xlim(0, 17)
#    #axs[0,1].set_ylim(-1, 1)
#    #axs[0,1].set_aspect('equal')
#
#if 0:
#    point_val = []
#    #max_dsn = max(sqrt(ds_n * ds_n))
#    for j in range(1137,1238):            #Coordinate range for line going from electrode 1 to 9 for h0 = 0.45 
#        point_val.append(ds_n[j] / 1)
#        #ds_n[j] = 10
#    axs[1,1].plot(np.linspace(0,17,1238 - 1137),point_val)
#    axs[1,1].set_xlim(0, 17)
#    axs[1,1].set_ylim(-1, 1)
#    axs[1,1].set_aspect('equal')

#plt.show()

fig, ax = plt.subplots(constrained_layout=True)

norm = TwoSlopeNorm(vcenter=0)
#norm = TwoSlopeNorm(vmin = -max_dsn * 50, vcenter=0, vmax = max_dsn * 50)
# plot EIT reconstruction
im = ax.tripcolor(x, y, tri, ds_n, norm = None, shading="flat", cmap=plt.cm.magma)
for i, e in enumerate(mesh_obj.el_pos):
    ax.annotate(str(i + 1), xy=(x[e], y[e]), color="r")
ax.set_aspect("equal")
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
fig.colorbar(im, ax=ax)

plt.title("p = {} | lambda = {}".format(p, lamb))

#for d in data:
#    print(d)
#plt.savefig('./images/{}_{}.png'.format(str(p)[2:], str(lamb)[2:]), dpi=96)
plt.show()
