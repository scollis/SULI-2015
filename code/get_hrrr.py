#!/home/scollis/anaconda/bin/python
from __future__ import print_function
import netCDF4
#import time

def grab_hrrr_slice(outname, reftime_index, time1_index):
    """ Grab select variables and reftime/time1 slice from HRRR file. """

    ncep_hrrr = netCDF4.Dataset('http://thredds-jumbo.unidata.ucar.edu/thredds/dodsC/grib/NCEP/HRRR/CONUS_2p5km/TwoD')

    # create the output NetCDF file, open for writing
    out_dset = netCDF4.Dataset(outname, 'w')

    # create the dimensions in the output netCDF file
    for dim in ['x', 'y', 'isobaric']:
        out_dset.createDimension(dim, len(ncep_hrrr.dimensions[dim]))

    # copy selected data for select variables to output NetCDF file
    var_names = ['Planetary_boundary_layer_height_surface',
                 'Dewpoint_temperature_isobaric',
                 'Temperature_isobaric',
                 'Pressure_reduced_to_MSL_msl',
                 'u-component_of_wind_isobaric',
                 'v-component_of_wind_isobaric']

    for var_name in var_names:
        print(var_name)
        in_var = ncep_hrrr.variables[var_name]
        in_units = ncep_hrrr.variables['time'].units
        print(in_units)
        out_var = out_dset.createVariable(var_name, in_var.dtype, in_var.dimensions[2:])
        out_units = out_dset.createVariable(var_name + 'timestamp', 'S1') 
        out_units[:] = in_units[:]
        out_var[:] = in_var[reftime_index, time1_index][:]
        out_var.units = ncep_hrrr.variables['time'].units
    pblh = out_dset.variables['Planetary_boundary_layer_height_surface'][0, 0:20]
    print(pblh)
    out_dset.timestamp = str(ncep_hrrr.variables['time'][reftime_index, time1_index]) + " :: " + ncep_hrrr.variables['time'].units    
    out_dset.close()

if __name__ == "__main__":
    file_num = open('/data/san_store/dap_hrrr/current.txt', 'r+')
    cnum = file_num.readlines()
    num = int(cnum[-1])
    print('hello world')
    # reftime index to copy to output file
    time1_index = 0     # time1 index to copy to output file
    for time1_index in range(10):
        grab_hrrr_slice('/data/san_store/dap_hrrr/selected_data_%03d_%03d.nc' %(num, time1_index), -1, time1_index)
    #time.sleep(3600)
    num += 1
    file_num.write(str(num) + '\n')
    file_num.close()
