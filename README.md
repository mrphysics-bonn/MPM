# Automated processing tool for MPM acquisitions

This software can perform the MPM analysis from nifti files in corresponding folders

## processing pipelines

In its current state the software scripts for the following acquisitions are provided

### MPM prepilot

Data processing in the prepiloting phase is performed by the script in *prepre.py*. To call the script use either

3T case
- *python prepre-mpm-3T.py --path PATH  --Nechoes nTE*

7T case
- *python prepre-mpm-7T.py --path PATH  --Nechoes nTE*

where *PATH* is the path to the data folder (see next chapter), *nTE* is the number of echoes used in MPM analysis

The pipeline expects the following data:

- RF receive coil sensitivity profile acquisition(s) at 3T
    - one head coil image in folder 'RF_sens_head'
    - one body coil image in folder 'RF_sens_body'
- 3DREAM acquisition(s)
    - one STE and one FID images in folder 'ThreeDream'
    - one FA map in folder 'ThreeDreamB1'
    - one delta omega map in folder 'ThreeDreamB0' 
- MPM acquisition(s)
    - MTw images in folder 'MTw'
    - PDw images in folder 'PDw'
    - T1w images in folder 'T1w'
    
The pipelines performs the following steps:

1. create a B1 magnitude image
2. perform B0 correction on B1 map and scale B1 map to 100%
3. define the acquired number of echoes in the prepre.py file
4. call hMRI toolbox for MPM analysis including ISC option


The resulting MPM maps can be found in

- *PATH/Results


## Required data structure

This software has a very specific data input and correponding folder name. In the folder

    *PATH/nii


## Needed software

- matlab inclusive SPM/hMRI
    - only needed for final MPM analysis

# MPM
