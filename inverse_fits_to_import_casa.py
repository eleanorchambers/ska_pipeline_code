from astropy.io import fits

f=fits.open('sim_3_3_z0p45_XY.fits')

f[0].data.data[...,0]*=-1
f[0].data.data[...,1]*=-1

f.verify('fix')

f.writeto('sim_3_3_z0p45_XY_rev.fits')



