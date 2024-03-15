# coding: utf-8
""" demo using GREIT """
# Copyright (c) Benyuan Liu. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
from __future__ import division, absolute_import, print_function

import numpy as np
import matplotlib.pyplot as plt

import pyeit.mesh as mesh
from pyeit.eit.fem import EITForward
import pyeit.eit.protocol as protocol
from pyeit.mesh.shape import thorax
import pyeit.eit.greit as greit
from pyeit.mesh.wrapper import PyEITAnomaly_Circle

""" 0. construct mesh """
n_el = 16  # nb of electrodes
use_customize_shape = False
if use_customize_shape:
    # Mesh shape is specified with fd parameter in the instantiation, e.g : fd=thorax
    mesh_obj = mesh.create(n_el, h0=0.1, fd=thorax)
else:
    mesh_obj = mesh.create(n_el, h0=0.1)

# extract node, element, alpha
pts = mesh_obj.node
tri = mesh_obj.element

""" 1. problem setup """
# this step is not needed, actually
# mesh_0 = mesh.set_perm(mesh_obj, background=1.0)

# test function for altering the 'permittivity' in mesh
anomaly = [

]
mesh_new = mesh.set_perm(mesh_obj, anomaly=anomaly, background=1.0)
delta_perm = np.real(mesh_new.perm - mesh_obj.perm)

""" 2. FEM forward simulations """
# setup EIT scan conditions
protocol_obj = protocol.create(n_el, dist_exc=1, step_meas=1, parser_meas="fmmu")

# calculate simulated data
fwd = EITForward(mesh_obj, protocol_obj)
v0 = np.loadtxt('example_data/ref_data.txt')
v1 = np.loadtxt('example_data/diff_left_data.txt')
print(len(v0))
print(len(v1))

""" 3. Construct using GREIT """
eit = greit.GREIT(mesh_obj, protocol_obj)
eit.setup(p=0.80, lamb=0.4, perm=1, jac_normalized=True)
ds = eit.solve(v1, v0, normalize=True)
x, y, ds = eit.mask_value(ds, mask_value=np.NAN)

# show alpha
fig, ax = plt.subplots(constrained_layout=True)

# plot
"""
imshow will automatically set NaN (bad values) to 'w',
if you want to manually do so

import matplotlib.cm as cm
cmap = cm.gray
cmap.set_bad('w', 1.)
plt.imshow(np.real(ds), interpolation='nearest', cmap=cmap)
"""
im = ax.imshow(np.real(ds), interpolation="none", cmap=plt.cm.viridis)
ax.axis("equal")

fig.colorbar(im, ax=ax)
# fig.savefig('../doc/images/demo_greit.png', dpi=96)
plt.show()
