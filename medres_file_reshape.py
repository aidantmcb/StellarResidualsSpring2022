from astropy.io import fits
from astropy.table import Table
import numpy as np
import numpy.ma as ma
import os
import tqdm
import glob

current_path = 'ResidualsFiles/'
new_path = 'Residuals/'
meta_path = new_path + 'meta.fits'

cols = ['TEFF_MIN', 'TEFF_MAX', 'LOGG_MIN', 'LOGG_MAX', 'M_H_MIN', 'M_H_MAX', 
       'NBIN', 'STDEV_MEDIAN', 'STDEV_MEAN', 'FNAME']

size = 26640 # number of individual files
table_contents = np.zeros((size, len(cols)), dtype = 'object')
counter = 0

def updateMetaTable(index, items, contents = table_contents):
    contents[index, :] = items
    return contents

fnames = glob.glob(current_path + '*')
fnames.remove(current_path + 'meta_table.fits')

data_names = ['MEDIAN', 'MEAN', 'STDEV', 'MED_ABS_DEV', 'PERC16', 'PERC84', 'NPIX']

for name in tqdm.tqdm(fnames, total = len(fnames)):
    hdul = fits.open(name)
    header = hdul[1].header
    teff_min, teff_max = (header['TMIN'], header['TMAX'])
    CRVAL1 = header['CRVAL1']
    CDELT1 = header['CDELT1']
    
    hdul = np.array(hdul)[1:].reshape(30,12)
    
    for hdul_bin in hdul:
        header = hdul_bin[0].header
        logg_min, logg_max = (header['GMIN'], header['GMAX'])

        
        for hdu in hdul_bin:
            header = hdu.header
            m_h_min, m_h_max = (header['MMIN'], header['MMAX'])
            nstars = header['NBIN']
            
            hdu0 = fits.PrimaryHDU()
            hdu0.header['NBIN'] = nstars
            hdu0.header['TEFF_MIN'] = teff_min
            hdu0.header['TEFF_MAX'] = teff_max
            hdu0.header['LOGG_MIN'] = logg_min
            hdu0.header['LOGG_MAX'] = logg_max
            hdu0.header['M_H_MIN'] = m_h_min
            hdu0.header['M_H_MAX'] = m_h_max
            hdu0.header['CRVAL1'] = CRVAL1
            hdu0.header['CDELT1'] = CDELT1

            hdulist = fits.HDUList([hdu0])
            
            for i in range(1, 7):
                if hdu.data is not None:
                    h = fits.ImageHDU(hdu.data[i-1])
                else: 
                    h = fits.ImageHDU()
                    
                h.header['NAME'] = data_names[i-1]
                h.header['NBIN'] = nstars
                h.header['TEFF_MIN'] = teff_min
                h.header['TEFF_MAX'] = teff_max
                h.header['LOGG_MIN'] = logg_min
                h.header['LOGG_MAX'] = logg_max
                h.header['M_H_MIN'] = m_h_min
                h.header['M_H_MAX'] = m_h_max
                h.header['CRVAL1'] = CRVAL1
                h.header['CDELT1'] = CDELT1
   
                hdulist.append(h)
            if hdu.data is None:
                stdev_median = np.nan
                stdev_mean = np.nan
            else:
                median = ma.array(hdulist[1].data, mask = hdulist[1].data == 0.0)
                mean = ma.array(hdulist[2].data, mask = hdulist[2].data == 0.0)
                stdev_median = ma.std(median, ddof = 1)
                stdev_mean = ma.std(median, ddof = 1)
            
            
            res_name = 'TEFFBIN{tmin}_{tmax}_LOGGBIN{gmin}_{gmax}_M_HBIN{mmin}_{mmax}.fits'.format(
                                                                tmin = teff_min, tmax= teff_max, 
                                                                gmin = logg_min, gmax = logg_max, 
                                                                mmin = m_h_min, mmax = m_h_max)
            fname_res = new_path + res_name
            hdulist.writeto(fname_res, overwrite = True)
            
            row_update = [teff_min, teff_max, logg_min, logg_max, m_h_min, m_h_max, nstars, stdev_median, stdev_mean, res_name]
            table_contents[counter,:] = row_update
            counter = counter + 1

datatype = [int, int, float, float, float, float, int, float, float, str]
meta_table = Table(names = cols, data = table_contents)
# tabcols = meta_table.columns
for i in range(len(cols)):
    col = cols[i]
    meta_table[col] = meta_table[col].astype(datatype[i])
meta_table.write(meta_path, format = 'fits', overwrite = True)


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