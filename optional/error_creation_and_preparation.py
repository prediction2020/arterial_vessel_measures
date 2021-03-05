from utils import directory_utils as dir_u
from utils import image_manipulation as img_manip

import AVE_config as conf


#FILE PREPARATION PART OF CODE
#Creating segmentations by introducing errors to ground truths
for patient in conf.patient_list:
    #Create all necessary directories
    dir_u.create_all_necessary_directories(patient)

    #create from annotated colored vessel tree a binary ground truth and save it to ground_truth_path
    colored_nifti_path = conf.root+"/"+patient+"/"+conf.ground_truth_folder_and_file_name + "/" + conf.annotated_ground_truth_file_name
    ground_truth_path = conf.root + "/" + patient + "/" + conf.ground_truth_folder_and_file_name + "/" + conf.ground_truth_folder_and_file_name + ".nii.gz"

    img_manip.get_ground_truth(colored_nifti_path,ground_truth_path)

    #create random voxels errors in intensities: subtle moderate severe
    img_manip.random_voxels_error_creation(patient)

    #saves vessel segments as separate niftis. Used in the code for segment_radius_errors(see configs) and large vessel error
    img_manip.save_all_vessel_segments(patient)

    #copies ground truth to error_tree_directory for comparison with evaluate_segmentation
    ground_truth_folder_path = conf.root + "/" + patient + "/" +conf.ground_truth_folder_and_file_name
    error_tree_directory= conf.root + "/" + patient + "/" + conf.run_name + "/"+ conf.segmentation_folder_name
    dir_u.simple_copy_paste_image(ground_truth_folder_path, error_tree_directory+"/"+conf.ground_truth_folder_and_file_name,file="ground")

    #Errors resulting from direct manipulation of the ground truth: Seperation error, Small vessels error.
    #The difference between ground truth and errors needs to be saved as another mask so that these masks can be combined arbitraryly with other errors.Please see niftis in error_already_as_tree_folder in config to get a better idea.

    #Seperation error creation : Seperation error is an error resulting from direct manipulation of the ground truth and the difference from the ground truth results in only false positives therefore it is an addable error.
    img_manip.create_addable_error_from_segmentation(patient)

    #Small vessels error creation : Small vessels is an error resulting from direct manipulation of the ground truth and the difference from the ground truth results in only false negative voxels  which need to be subtracted from the ground truth
    img_manip.create_subtraction_error_from_segmentation(patient)






