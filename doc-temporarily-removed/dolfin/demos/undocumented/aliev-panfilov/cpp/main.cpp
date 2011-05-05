// Copyright (C) 2006-2008 Anders Logg.
// Licensed under the GNU LGPL Version 2.1.
//
// First added:  2006-05-24
// Last changed: 2008-10-07
//
// This demo solves a simple model for cardiac excitation,
// proposed in a 1995 paper by Aliev and Panfilov.

#include <dolfin.h>

using namespace dolfin;

class AlievPanfilov : public ODE
{
public:

  AlievPanfilov() : ODE(2, 300.0)
  {
    // Set parameters
    a    = 0.15;
    eps0 = 0.002;
    k    = 8.0;
    mu1  = 0.07;
    mu2  = 0.3;
  }

  void u0(Array<real>& u)
  {
    u[0] = 0.2;
    u[1] = 0.0;
  }

  void f(const Array<real>& u, real t, Array<real>& y)
  {
    const real eps = eps0 + mu1*u[1] / (u[0] + mu2);

    y[0] = -k*u[0]*(u[0] - a)*(u[0] - 1.0) - u[0]*u[1];
    y[1] = eps*(-u[1] - k*u[0]*(u[0] - a - 1.0));
  }

private:

  real a;
  real eps0;
  real k;
  real mu1;
  real mu2;

};

int main()
{
  AlievPanfilov ode;
  ode.solve();

  return 0;
}