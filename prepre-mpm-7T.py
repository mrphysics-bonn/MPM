#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 21:27:00 2022

@author: wangd
"""
import os
import re
import glob
import nibabel as nib
import numpy as np
import json
import sys
import argparse

ImgPulDur = 1.020e-3  #imaging pulse duration of 3DREAM at 7T
ImgPulFA = 50         #imaging pulse flip angle of 3DREAM at 7T

def main():
    parser = argparse.ArgumentParser(
        description='Processing pipeline for MPM.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--path',   help='path to CEST data, default: pwd ',default=os.getcwd(), required=False)
    parser.add_argument('--Nechoes',   help='number echoes in acquisition, default: pwd ',default=4, required=False)
    
    args = parser.parse_args()
    path = args.path
    nTE  = args.Nechoes
    #print(nTE)
    #print(type(nTE))
    nTE = int(nTE)
    
    prep_data(path)    # prepare data 
    create_batchFile(path, nTE)  # Create batch scripts for hMRI analysis and call MATLAB to perform MPM analysis



def prep_data(path):

    # Calculate B1mag image and B0 correction
    
    create_magnitude_B1(path)
    B0_cor_B1(path)



def create_magnitude_B1(folder_path):
    f1 = os.path.join(folder_path,'nii','ThreeDream', '*-1.nii')
    f1 = glob.glob(f1)
    #print(f1)
    f_1 = nib.load(f1[0])
    F1 = f_1.get_fdata()

    f2 = os.path.join(folder_path,'nii','ThreeDream',  '*-2.nii')
    f2 = glob.glob(f2)
    #print(f2)
    f_2 = nib.load(f2[0])
    F2 = f_2.get_fdata()

    B1 = 2 * F1 + F2

    nib.save(nib.Nifti1Image(B1, f_1.affine), os.path.join(folder_path,'nii','ThreeDream', "mag_B1map.nii"))
    #print(os.path.join(folder_path,'nii','ThreeDream', "mag_B1map.nii"))



def gamma_b1(alpha, tau=1.020e-3):
    return alpha/tau

def cos_omega_eff(omega_eff, delta_omega, tau=1.020e-3):
    return np.cos(omega_eff * tau)+ ((delta_omega / omega_eff)**2) * (1 - np.cos(omega_eff * tau))


def B0_cor_B1(folder_path):
    
    f_B1 = os.path.join(folder_path,'nii','ThreeDreamB1', '*-2.nii')
    f_B1 = glob.glob(f_B1)
    B1 = nib.load(f_B1[0])
    #print(f_B1[0])
    b1 = B1.get_fdata()
    
    f_B0 = os.path.join(folder_path,'nii','ThreeDreamB0', '*-2.nii')
    f_B0 = glob.glob(f_B0)
    #print(f_B0[0])
    b0 = nib.load(f_B0[0]).get_fdata()
    dir = os.path.dirname(f_B1[0])


    tau = ImgPulDur
    fa_nominal = np.deg2rad(10.0)
    fa_actual = fa_nominal * b1 / (ImgPulFA *10.0)
    delta_omega = b0 * 2.0 * np.pi # off-resonance frequency [rad/s]


    #print(gamma_b1_dream, gamma_b1(fa_actual, tau = tau))

    omega_eff = np.sqrt( (delta_omega)**2 + (gamma_b1(fa_actual, tau = tau))**2) # nutation frequency


    cosine = cos_omega_eff(omega_eff=omega_eff, delta_omega=delta_omega, tau=tau)

    fa_actual_with_offresonance = np.arccos(cosine) #[rad]
    print(os.path.join(dir, 'B1map.nii'))
    nib.save(nib.Nifti1Image(100*fa_actual_with_offresonance/fa_nominal, B1.affine) ,os.path.join(dir, 'B1map.nii'))





def create_batchFile(path, nTE):
    #filename = os.path.join(path,"data","spm_batch.m")
    filename = os.path.join(path,"spm_batch.m")
    
    f = open(filename,"w")
    
    #for (f,s) in zip((fshort,flong),("short","long")):
    # begin file
    f.write("%---------------------------------------\n")
    f.write("% This is an automatically generated batchfile\n")
    #f.write("% author: voelzkey\n")
    f.write("% date: xxx\n")
    f.write("%---------------------------------------\n\n")
    
    # load configure toolbox 
    
    p = os.getcwd()
    print(p)
    f.write("matlabbatch{1}.spm.tools.hmri.hmri_config.hmri_setdef.customised = {'%s/hmri_local_defaults_ISC_MPM.m'};\n"%p)
    
    #define output directory
    #f.write("matlabbatch{2}.spm.tools.hmri.create_mpm.subj.output.outdir = {'%s/data'};\n"%path)
    f.write("matlabbatch{2}.spm.tools.hmri.create_mpm.subj.output.outdir = {'%s'};\n"%path)
    
    
    #RF receive setting
    f.write("matlabbatch{2}.spm.tools.hmri.create_mpm.subj.sensitivity.RF_us = '-';\n")



    
    fB1mag = os.path.join(path, 'nii','ThreeDream','mag_B1map.nii')
    
    fB1 = os.path.join(path, 'nii','ThreeDreamB1','B1map.nii')
    #fB1 = glob.glob(fB1)

    # B1 settings
    f.write("matlabbatch{2}.spm.tools.hmri.create_mpm.subj.b1_type.pre_processed_B1.b1input = {\n")
    f.write("                                                                                  '%s,1'\n"%fB1mag)
    f.write("                                                                                  '%s,1'\n"%fB1)
    f.write("                                                                                  };\n")
    f.write("matlabbatch{2}.spm.tools.hmri.create_mpm.subj.b1_type.pre_processed_B1.scafac = 1.0;\n")

    # input data MT
    fMT = os.path.join(path, 'nii','MTw','*.nii')
    fMT = glob.glob(fMT)
    #print(fMT)
    fMT.sort()
    
    f.write("matlabbatch{2}.spm.tools.hmri.create_mpm.subj.raw_mpm.MT = {\n")
    for i in range(nTE):
        f.write("                                                            '%s,1'\n"%fMT[i])
    f.write("                                                            };\n")

    # input data PD
    fPD = os.path.join(path, 'nii','PDw','*.nii')
    fPD = glob.glob(fPD)
    #print(fPD)
    fPD.sort()
    
    f.write("matlabbatch{2}.spm.tools.hmri.create_mpm.subj.raw_mpm.PD = {\n")
    for i in range(nTE):
        f.write("                                                            '%s,1'\n"%fPD[i])
    f.write("                                                            };\n")

    # input data T1
    fT1 = os.path.join(path, 'nii','T1w','*.nii')
    fT1 = glob.glob(fT1)
    #print(fMT)
    fT1.sort()
    
    f.write("matlabbatch{2}.spm.tools.hmri.create_mpm.subj.raw_mpm.T1 = {\n")
    for i in range(nTE):
        f.write("                                                            '%s,1'\n"%fT1[i])
    f.write("                                                            };\n")
        

    # Disable popups and close file
    f.write("matlabbatch{2}.spm.tools.hmri.create_mpm.subj.popup = false;\n")
    f.close()
    
    call_batch(filename)
    #call_batch(f)
    #call_batch(filename_short)


def call_batch(filename):
    import matlab.engine as mat # move matlab import to here if matlab is not installed only this function fails

    eng=mat.start_matlab()
    #print(filename)
    #print(type(filename))
    #print(type(filename.name))
    #eng.call_batch(filename.name,nargout=0)
    eng.call_batch(filename,nargout=0)
    eng.quit()

if __name__ == '__main__':
    sys.exit(main())

