import meep as mp
import math
import random
import argparse

def main(args):

    resolution = 20 # pixels/unit length (1 um)

    h = args.hh
    w = args.w
    a = args.a
    d = args.d
    N = args.N
    N = N + 1

    nSi = 3.45
    Si = mp.Medium(index=nSi)
    nSiO2 = 1.45
    SiO2 = mp.Medium(index=nSiO2)

    sxy = 16
    sz = 4
    cell_size = mp.Vector3(sxy, sxy, sz)

    geometry = []

    # rings of Bragg grating
    for n in range(N,0,-1):
        geometry.append(mp.Cylinder(material=Si, center=mp.Vector3(0,0,0), radius=n*a, height=h))
        geometry.append(mp.Cylinder(material=mp.air, center=mp.Vector3(0,0,0), radius=n*a-d, height=h))

    # remove left half of Bragg grating rings to form semi circle
    geometry.append(mp.Block(material=mp.air, center=mp.Vector3(-0.5*N*a,0,0), size=mp.Vector3(N*a,2*N*a,h)))
    geometry.append(mp.Cylinder(material=Si, center=mp.Vector3(0,0,0), radius=a-d, height=h))

    # angle sides of Bragg grating
    
    # rotation angle of sides relative to Y axis (degrees)
    rot_theta = -1*math.radians(args.rot_theta)
    
    pvec = mp.Vector3(0, 0.5*w, 0)
    cvec = mp.Vector3(-0.5*N*a, 0.5*N*a+0.5*w, 0)
    rvec = cvec-pvec
    rrvec = rvec.rotate(mp.Vector3(0,0,1), rot_theta)
    
    geometry.append(mp.Block(material=mp.air, center=pvec+rrvec, size=mp.Vector3(N*a,N*a,h),
                             e1=mp.Vector3(0.9396926207859084,-0.3420201433256687,0),
                             e2=mp.Vector3(0.3420201433256687,0.9396926207859084,0),
                             e3=mp.Vector3(0,0,1)))

    pvec = mp.Vector3(0, -0.5*w, 0)
    cvec = mp.Vector3(-0.5*N*a, -1*(0.5*N*a+0.5*w), 0)
    rvec = cvec-pvec
    rrvec = rvec.rotate(mp.Vector3(0,0,1), -1*rot_theta)

    geometry.append(mp.Block(material=mp.air, center=pvec+rrvec, size=mp.Vector3(N*a,N*a,h),
                             e1=mp.Vector3(0.9396926207859084,0.3420201433256687,0),
                             e2=mp.Vector3(-0.3420201433256687,0.9396926207859084,0),
                             e3=mp.Vector3(0,0,1)))
    
    # input waveguide
    geometry.append(mp.Block(material=mp.air, center=mp.Vector3(-0.25*sxy,0.5*w+0.5*a,0), size=mp.Vector3(0.5*sxy,a,h)))
    geometry.append(mp.Block(material=mp.air, center=mp.Vector3(-0.25*sxy,-1*(0.5*w+0.5*a),0), size=mp.Vector3(0.5*sxy,a,h)))
    geometry.append(mp.Block(material=Si, center=mp.Vector3(-0.25*sxy,0,0), size=mp.Vector3(0.5*sxy,w,h)))

    # substrate
    geometry.append(mp.Block(material=SiO2, center=mp.Vector3(0,0,-0.5*sz+0.25*(sz-h)), size=mp.Vector3(mp.inf,mp.inf,0.5*(sz-h))))

    dpml = 1.0
    boundary_layers = [ mp.PML(dpml) ]

    # mode frequency
    fcen = 1/1.55
    
    sources = [ mp.EigenModeSource(src=mp.GaussianSource(fcen, fwidth=0.2*fcen),
                                   component=mp.Ey,
                                   size=mp.Vector3(0,sxy-2*dpml,sz-2*dpml),
                                   center=mp.Vector3(-0.5*sxy+dpml,0,0),
                                   eig_match_freq=True,
                                   eig_parity=mp.ODD_Y,
                                   eig_kpoint=mp.Vector3(1.5,0,0),
                                   eig_resolution=32) ]
    
    
    symmetries = [ mp.Mirror(mp.Y,-1) ]
    
    sim = mp.Simulation(resolution=resolution,
                        cell_size=cell_size,
                        boundary_layers=boundary_layers,
                        geometry=geometry,
                        sources=sources,
                        dimensions=3,
                        symmetries=symmetries)

    nearfield = sim.add_near2far(fcen, 0, 1, mp.Near2FarRegion(mp.Vector3(0,0,0.5*sz-dpml), size=mp.Vector3(sxy-2*dpml,sxy-2*dpml,0)))
    
    sim.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ey, mp.Vector3(), 1e-6))

    r = 1000 * (1 / fcen)  # 1000 wavelengths out from the source
    npts = 100  # number of points in [0,2*pi) range of angles

    for n in range(npts):
        ff = sim.get_farfield(nearfield, mp.Vector3(r * math.cos(math.pi * (n / npts)), 0, r * math.sin(math.pi * (n / npts))))
        print("farfield: {}, {}, ".format(n, math.pi * n / npts), end='')
        print(", ".join([str(f).strip('()').replace('j', 'i') for f in ff]))
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-hh', type=float, default=0.22, help='wavelength height (default: 0.22 um)')
    parser.add_argument('-w', type=float, default=0.50, help='wavelength width (default: 0.50 um)')
    parser.add_argument('-a', type=float, default=1.0, help='Bragg grating periodicity/lattice parameter (default: 1.0 um)')
    parser.add_argument('-d', type=float, default=0.5, help='Bragg grating thickness (default: 0.5 um)')
    parser.add_argument('-N', type=int, default=5, help='number of grating periods')
    parser.add_argument('-rot_theta', type=float, default=20, help='rotation angle of sides relative to Y axis (default: 20 degrees)')    
    args = parser.parse_args()
    main(args)