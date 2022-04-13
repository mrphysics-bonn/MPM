function call_batch(path_to_batch)
    hmri_path = '/home/wangd/Documents/MATLAB/hMRI-toolbox';
    SPM_path  = '/home/wangd/Documents/MATLAB/spm12';

    addpath(hmri_path);
    addpath(genpath(SPM_path));
    disp("path addded")

    run(path_to_batch)
    disp(matlabbatch)
    spm_jobman('run',matlabbatch)
end
