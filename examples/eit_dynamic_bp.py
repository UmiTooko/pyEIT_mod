# coding: utf-8
""" demo code for back-projection """
# Copyright (c) Benyuan Liu. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
from __future__ import absolute_import, division, print_function

import matplotlib.pyplot as plt
import numpy as np
import pyeit.eit.bp as bp
import pyeit.eit.protocol as protocol
import pyeit.mesh as mesh
from pyeit.eit.fem import EITForward
from pyeit.mesh.shape import thorax
from pyeit.mesh.wrapper import PyEITAnomaly_Circle

""" 0. build mesh """
n_el = 16  # nb of electrodes
use_customize_shape = False
if use_customize_shape:
    # Mesh shape is specified with fd parameter in the instantiation, e.g : fd=thorax
    mesh_obj = mesh.create(n_el, h0=0.1, fd=thorax) #       f located in wrapper.py
else:
    mesh_obj = mesh.create(n_el, h0=0.1)

""" 1. problem setup """
anomaly = PyEITAnomaly_Circle(center = [0.5, 0.5], r=0.1, perm=1000.0) # r là bán kính, perm là độ điện thẩm
mesh_new = mesh.set_perm(mesh_obj, anomaly=anomaly, background=1.0)

""" 2. FEM forward simulations """
# setup EIT scan conditions
# adjacent stimulation (dist_exc=1), adjacent measures (step_meas=1)
protocol_obj = protocol.create(n_el, dist_exc=1, step_meas=1, parser_meas="std")

# calculate simulated data
fwd = EITForward(mesh_obj, protocol_obj)
v0 = np.loadtxt('examples/example_data/ref_data.txt')
v1 = np.loadtxt('examples/example_data/diff_left_data.txt')
print(len(v0))
print(len(v1))



""" 3. naive inverse solver using back-projection """
eit = bp.BP(mesh_obj, protocol_obj)
eit.setup(weight="none")
# the normalize for BP when dist_exc>4 should always be True
ds = 224.0 * eit.solve(v1, v0, normalize=True)

# extract node, element, alpha
pts = mesh_obj.node
tri = mesh_obj.element

# draw
fig, ax = plt.subplots(constrained_layout=True)

# reconstructed

im = ax.tripcolor(pts[:, 0], pts[:, 1], tri, ds)
ax.set_title(r"Reconstituted $\Delta$ Conductivities")
ax.axis("equal")
fig.colorbar(im, ax=ax)
plt.show()
