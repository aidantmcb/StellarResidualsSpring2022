from astropy.io import fits
import numpy as np
import os
import tqdm
import glob

current_path = 'ResidualsFiles/'
new_path = 'ResidualsFiles/Test/'
meta_path = new_path + 'meta.fits'

# teff_bins = np.concatenate([np.arange(3000, 5000, 50), np.arange(5000,10000, 150), [10000]])
# logg_bins = np.around(np.arange(-1, 5.2, 0.2), 2)
# m_h_bins = np.around(np.concatenate([np.arange(-2.3, -1.1, 0.3), np.arange(-1.1, 0.5, 0.2), [0.5]]), 2)

fnames = glob.glob(current_path + '*')

for name in tqdm(fnames, total = len(fnames)):
    hdul = fits.open(name)
    header = hdul[1].header
    teff_min, teff_max = (header['TMIN'], header['TMAX'])
    
    teff_dir = new_path + 'TEFF_{min}_{max}/'.format(min = str(teff_min), max = str(teff_max))
    os.mkdir(teff_dir)
    
    hdul = np.array(hdul)[1:].reshape(30,12)
    
    for hdul_bin in hdul:
        header = hdul_bin[0].header
        logg_min, logg_max = (header['GMIN'], header['GMAX'])
        logg_dir = teff_dir + 'LOGG_{min}_{max}/'.format(min = str(logg_min), max = str(teff_max))
        
        for hdu in hdul_bin:
            
            
        
        
#     hdu = hdulist[j, k].item()
                                                  
    
    break



##### DATA STRUCTURE ######
# hdul[0] - primary HDU (meta)
# hdul[1] - median residual HDU
# hdul[2] - mean residual HDU
# hdul[3] - stdev HDU
# hdul[4] - mean abs dev HDU
# hdul[5] - 16th percentile HDU
# hdul[6] - 84th percentile HDU
# hdul[7] - stars per pix HDU
#####