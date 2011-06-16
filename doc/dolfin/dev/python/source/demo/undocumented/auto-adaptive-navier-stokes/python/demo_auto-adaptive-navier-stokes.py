# Copyright (C) 2010 Marie E. Rognes
#
# This file is part of DOLFIN.
#
# DOLFIN is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DOLFIN is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with DOLFIN. If not, see <http://www.gnu.org/licenses/>.

from dolfin import *
import time

class Noslip(SubDomain):
    def inside(self, x, on_boundary):
        return (x[1] < DOLFIN_EPS or x[1] > 1.0 - DOLFIN_EPS) or \
               (on_boundary and abs(x[0] - 1.5) < 0.1 + DOLFIN_EPS)

class Outflow(SubDomain):
    def inside(self, x, on_boundary):
        return x[0] > 4.0 - DOLFIN_EPS

parameters["allow_extrapolation"] = True;

# Material parameters
nu = Constant(0.02)

# Mesh
mesh = Mesh("channel_with_flap.xml")

# Define function spaces (Taylor-Hood)
V = VectorFunctionSpace(mesh, "CG", 2)
Q = FunctionSpace(mesh, "CG", 1)
W = V * Q

# Define unknown and test function(s)
(v, q) = TestFunctions(W)
w_h = Function(W)
(u_h, p_h) = (as_vector((w_h[0], w_h[1])), w_h[2])

# Prescribed pressure
p0 = Expression("(4.0 - x[0])/4.0")

# Define variational forms
n = FacetNormal(mesh)
a = (nu*inner(grad(u_h), grad(v)) - div(v)*p_h + q*div(u_h))*dx
a = a + inner(grad(u_h)*u_h, v)*dx
L = - p0*dot(v, n)*ds
F = a - L

dw = TrialFunction(W)
dF = derivative(F, w_h, dw) # FIXME

# Define boundary conditions
bc = DirichletBC(W.sub(0), Constant((0.0, 0.0)), Noslip())

# Define variational problem (with new notation)
pde = VariationalProblem(F, dF, bc)

outflow = Outflow()
outflow_markers = MeshFunction("uint", mesh, mesh.topology().dim() - 1)
outflow_markers.set_all(1)
outflow.mark(outflow_markers, 0)

# Define new measure with associated subdomains
dss = ds[outflow_markers]

# Define goal and reference
M = u_h[0]*dss(0)
pde.parameters["adaptivity"]["reference"] = 0.40863917;
pde.parameters["adaptivity"]["plot_mesh"] = False;

# Solve to given tolerance
tol = 1.e-05
pde.solve(w_h, tol, M)