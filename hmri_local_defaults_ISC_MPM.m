function hmri_local_defaults_example_1
% These local settings have been defined for the hMRI toolbox for tutorial
% purpose only. Please read carefully the comments in the code below before
% reusing these parameters for your own processing.  

% PURPOSE
% To set user-defined (site- or protocol-specific) defaults parameters
% which are used by the hMRI toolbox. Customized processing parameters can
% be defined, overwriting defaults from hmri_defaults. Acquisition
% protocols can be specified here as a fallback solution when no metadata
% are available. Note that the use of metadata is strongly recommended. 
%
% RECOMMENDATIONS
% Parameters defined in this file are identical, initially, to the ones
% defined in hmri_defaults.m. It is recommended, when modifying this file,
% to remove all unchanged entries and save the file with a meaningful name.
% This will help you identifying the appropriate defaults to be used for
% each protocol, and will improve the readability of the file by pointing
% to the modified parameters only.
%
% WARNING
% Modification of the defaults parameters may impair the integrity of the
% toolbox, leading to unexpected behaviour. ONLY RECOMMENDED FOR ADVANCED
% USERS - i.e. who have a good knowledge of the underlying algorithms and
% implementation. The SAME SET OF DEFAULT PARAMETERS must be used to
% process uniformly all the data from a given study. 
%
% HOW DOES IT WORK?
% The modified defaults file can be selected using the "Configure toolbox"
% branch of the hMRI-Toolbox. For customization of B1 processing
% parameters, type "help hmri_b1_standard_defaults.m". 
%
% DOCUMENTATION
% A brief description of each parameter is provided together with
% guidelines and recommendations to modify these parameters. With few
% exceptions, parameters should ONLY be MODIFIED and customized BY ADVANCED
% USERS, having a good knowledge of the underlying algorithms and
% implementation. 
% Please refer to the documentation in the github WIKI for more details. 
%__________________________________________________________________________
% Written by E. Balteau, 2017.
% Cyclotron Research Centre, University of Liege, Belgium

% Global hmri_def variable used across the whole toolbox
global hmri_def


%% Defining the imperfect spoiling correction parameters for the SC-EPI and FLASH protocol
hmri_def.imperfectSpoilCorr.enabled = true;

hmri_def.MPMacq_set.names{8} = 'EPI_3T_ISC';
hmri_def.MPMacq_set.tags{8}  = 'EPI_3T_ISC';
hmri_def.MPMacq_set.vals{8}  = [39  39   4  25];
hmri_def.imperfectSpoilCorr.EPI_3T_ISC.tag = 'EPI_3T_ISC';
hmri_def.imperfectSpoilCorr.EPI_3T_ISC.P2_a = [19.3875     -25.0483      22.8227];
hmri_def.imperfectSpoilCorr.EPI_3T_ISC.P2_b = [-0.0579      0.0251      0.9919];
hmri_def.imperfectSpoilCorr.EPI_3T_ISC.enabled = hmri_def.imperfectSpoilCorr.enabled;


hmri_def.MPMacq_set.names{9} = 'GRE_3T_ISC';
hmri_def.MPMacq_set.tags{9}  = 'GRE_3T_ISC';
hmri_def.MPMacq_set.vals{9}  = [18  18   4  25];
hmri_def.imperfectSpoilCorr.GRE_3T_ISC.tag = 'GRE_3T_ISC';
hmri_def.imperfectSpoilCorr.GRE_3T_ISC.P2_a = [65.3995     -82.5342      40.3983];
hmri_def.imperfectSpoilCorr.GRE_3T_ISC.P2_b = [-0.1322      0.0791      0.9737];
hmri_def.imperfectSpoilCorr.GRE_3T_ISC.enabled = hmri_def.imperfectSpoilCorr.enabled;


hmri_def.MPMacq_set.names{10} = 'EPI_7T_ISC';
hmri_def.MPMacq_set.tags{10}  = 'EPI_7T_ISC';
hmri_def.MPMacq_set.vals{10}  = [36  36   4  25];
hmri_def.imperfectSpoilCorr.EPI_7T_ISC.tag = 'EPI_7T_ISC';
hmri_def.imperfectSpoilCorr.EPI_7T_ISC.P2_a = [16.7109     -21.7757      17.9092];
hmri_def.imperfectSpoilCorr.EPI_7T_ISC.P2_b = [-0.0496      0.0254      0.9915];
hmri_def.imperfectSpoilCorr.EPI_7T_ISC.enabled = hmri_def.imperfectSpoilCorr.enabled;


hmri_def.MPMacq_set.names{11} = 'GRE_7T_ISC';
hmri_def.MPMacq_set.tags{11}  = 'GRE_7T_ISC';
hmri_def.MPMacq_set.vals{11}  = [16  16   4  25];
hmri_def.imperfectSpoilCorr.GRE_7T_ISC.tag = 'GRE_7T_ISC';
hmri_def.imperfectSpoilCorr.GRE_7T_ISC.P2_a = [65.8683      -85.368      38.7393];
hmri_def.imperfectSpoilCorr.GRE_7T_ISC.P2_b = [-0.1336      0.1001      0.9656];
hmri_def.imperfectSpoilCorr.GRE_7T_ISC.enabled = hmri_def.imperfectSpoilCorr.enabled;

end
