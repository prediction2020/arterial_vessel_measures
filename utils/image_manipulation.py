import nibabel as nib
import numpy as np
import AVE_config as conf
from utils import search_utils as search_u
from utils import directory_utils as dir_u

# binarizes image_to_01 and saves it under path_binary_image_result
def get_ground_truth(image_to_01, path_binary_image_result):
    image = nib.load(image_to_01)
    image_data = image.get_data()
    array = np.zeros(image.shape)
    array[image_data > 0] = 1
    img = nib.Nifti1Image(array, image.affine)
    nib.save(img, path_binary_image_result)
    print("....Creating ground_truth from annotated nifti.....")

# adds error_nifti to input_nifti, input nifti can be a path or an image array
def add_nifti(input_nifti, error_nifti):
    if isinstance(input_nifti, str):
        image = nib.load(input_nifti)
        image_data = image.get_data()
    else:
        image_data = input_nifti
    image_error = nib.load(error_nifti)
    image_error_data = image_error.get_data()
    image_data[image_error_data == 1] = 1
    return image_data

# takes the annotated ground truth as input and
# saves the vessel segment with the vesselid_to_save
# under path_vessel_segment_nifti_result
# vessel ids are label colours from the software ITK SNAP
# for example M1 = 4.
def save_vessel_segments(annotated_ground_truth,vesselid_to_save, path_vessel_segment_nifti_result):
    image = nib.load(annotated_ground_truth)
    image_data = image.get_data()
    array = np.zeros(image.shape)
    array[image_data == vesselid_to_save] = 1
    vessel_segment = array
    img = nib.Nifti1Image(vessel_segment, image.affine)
    nib.save(img, path_vessel_segment_nifti_result)
    print("....Saving individual vessel segments")


# error_mask is subtracted from input_nifti and saved under path_subtracted_image_result
def subtract_mask(input_nifti, error_mask, path_subtracted_image_result):
    if isinstance(input_nifti, str):
        image = nib.load(input_nifti)
        image_data = image.get_data()
    else:
        image_data = input_nifti
    image_error_segment = nib.load(error_mask)
    image_data_error_segment = image_error_segment.get_data()
    image_data[image_data_error_segment==1] = 0
    binary_nifti = image_data
    img = nib.Nifti1Image(binary_nifti, image_error_segment.affine)
    if "nii" in path_subtracted_image_result:
        nib.save(img, path_subtracted_image_result)
        return path_subtracted_image_result
    else:
        return binary_nifti

# introduces n random voxels where n is the 0,5%,1%,2%(subtle,moderate,severe) percentage of the number of voxels in image_for_voxel_count,
# path_error_image_result is the result path for the error image and defines also the error intensity: subtle, moderate,severe
def random_voxels(image_for_voxel_count, patient_original_nifti_path, path_error_image_result):
    image = nib.load(image_for_voxel_count)
    image_data = image.get_data()
    patient_original_nifti = patient_original_nifti_path
    image_original_nifti = nib.load(patient_original_nifti)
    image_original_nifti_data = image_original_nifti.get_data()

    num_ones = np.count_nonzero(image_data)
    if "severe" in path_error_image_result:
        intensity = int(num_ones / 33)
    if "moderate" in path_error_image_result:
        intensity = int(num_ones / 50)
    if "subtle" in path_error_image_result:
        intensity = int(num_ones / 100)

    flattened_image = image_original_nifti_data.flatten()
    image_original_nifti_data[image_original_nifti_data <= 40] = 0
    image_original_nifti_data[image_original_nifti_data > 40] = 1

    image_original_nifti_data.flat[
        np.random.choice(len(image_original_nifti_data.flatten()), len(image_original_nifti_data.flatten()) - intensity,
                         replace=False)] = 0

    img = nib.Nifti1Image(image_original_nifti_data, image_original_nifti.affine)
    nib.save(img, path_error_image_result)
    print("....Creating random voxels error with intensity:" + str(intensity))


#some errors result from directly manipulating the ground truth by adding false positives .
#The ground truth needs to be subtracted from these error_niftis to make a combinable error nifti
def create_addable_error_from_segmentation(patient):
    already_error_tree_dict = search_u.find_error_file(conf.root + "/" + patient + "/" + conf.errors_folder_name + "/"+ conf.error_already_as_tree_folder, file="nii", search="error")
    for key, value in already_error_tree_dict.items():
        if "seperation" in value:
            subtract_mask(key, conf.root + "/" + patient + "/" + conf.ground_truth_folder_and_file_name + "/" + conf.ground_truth_folder_and_file_name+ ".nii.gz",
                          conf.root + "/" + patient + "/" + conf.errors_folder_name + "/" + conf.errors_to_add_folder + "/" + value)
        print("....Created errors_to_add and saved results to"
              + conf.root + "/" + patient + "/" + conf.errors_folder_name + "/" + conf.errors_to_add_folder)


#some errors result from directly manipulating the ground truth by adding false negatives(erasing voxels) .
#The error nifti needs to be subtracted from the ground truth to make a combinable error nifti
def create_subtraction_error_from_segmentation(patient):
    already_error_tree_dict = search_u.find_error_file(conf.root + "/" + patient + "/" + conf.errors_folder_name + "/" + conf.error_already_as_tree_folder, file="nii", search="error")
    for key, value in already_error_tree_dict.items():
        if "small" in value:
            subtract_mask(conf.root+"/"+patient+"/"+conf.ground_truth_folder_and_file_name + "/" + conf.ground_truth_folder_and_file_name + ".nii.gz",
                          key,
                          conf.root + "/" + patient + "/" + conf.errors_folder_name + "/" + conf.errors_to_subtract_folder + "/" + value)
        print("....Created errors_to_subtract and saved results to" + conf.root + "/" + patient + "/" + conf.errors_folder_name + "/" + conf.errors_to_subtract_folder)



def add_multiple_nifti(input_nifti, error_nifti_list, patient, output_path_list, set_or_run_name, seperator):
    # load input nifti
    image = nib.load(input_nifti)
    image_data = image.get_fdata()
    only_Pcom_segment_path = conf.root + "/" + patient + "/" + conf.errors_folder_name + "/" + conf.artery_segment_folder + "/" + conf.Pcom_segment_file_name
    only_M1_segment_path = conf.root + "/" + patient + "/" + conf.errors_folder_name + "/" + conf.artery_segment_folder + "/" + conf.M1_segment_file_name
    only_Carotid_segment_path = conf.root + "/" + patient + "/" + conf.errors_folder_name + "/" + conf.artery_segment_folder + "/" + conf.Carotid_segment_file_name

    # loop through all errors in nifti_list and depending on error type do the required operations on niftis
    for x in error_nifti_list:
        image_error = nib.load(x)
        image_error_data = image_error.get_fdata()
        if 'add' in x:
            image_data[image_error_data == 1] = 1
        if 'subtract' in x:
            image_data[image_error_data == 1] = 0
        if 'radius' in x:
            if 'Pcom' in x:
                if "missing" in x:
                    subtracted = subtract_mask(image_data, only_Pcom_segment_path, '')
                    image_data = subtracted
                # if Pcom should be manipulated as simulated error then first the Pcom segment is subtracted from the ground truth and the error simulated segment is added.Same for other segments below
                subtracted = subtract_mask(image_data, only_Pcom_segment_path, '')
                image_data = add_nifti(subtracted, x)
            if 'M1' in x:
                if "missing" in x:
                    subtracted = subtract_mask(image_data, only_M1_segment_path, '')
                    image_data = subtracted
                subtracted = subtract_mask(image_data, only_M1_segment_path, '')
                image_data = add_nifti(subtracted, x)
            if 'ICA' in x:
                if "missing" in x:
                    subtracted = subtract_mask(image_data, only_Carotid_segment_path, '')
                    image_data = subtracted
                subtracted = subtract_mask(image_data, only_Carotid_segment_path, '')
                image_data = add_nifti(subtracted, x)
    # save file name ["T1","L0","K2"] ====> T1_L0_K2 (output_file_name)
    output_file_name = output_path_list
    if seperator:
        seperator = '_'
        output_file_name = seperator.join(output_path_list)

    print('....Created ' + output_file_name + ' error and saved to segmentations folder')
    # create directoey and save the file
    dir_u.create_a_directory(conf.root + "/" + patient + "/" + set_or_run_name + "/" + conf.segmentation_folder_name,
                             output_file_name)
    img = nib.Nifti1Image(image_data, image.affine)
    nib.save(img,
             conf.root + "/" + patient + "/" + set_or_run_name + "/" + conf.segmentation_folder_name + '/' + output_file_name + '/' + conf.segmentation_string)

def convert_abbr_to_path(abbrv, patient):
    segment_radius_errors_folder = conf.root + "/" + patient + "/" + conf.errors_folder_name + "/" + conf.artery_segment_errors

    print("ABBRv", abbrv)

    # leave out the number at the end of each error to have the base letter ["T1"]==["T"]
    abb = abbrv[:-1]
    # a dictionary in config is defined to map strings(error names) with error abbreviations
    error_name = conf.map_dictionary[abbrv[:-1]]
    print(error_name)
    # now come all conditions for where the paths are located and depending on which error type is used
    if error_name in conf.segment_radius_errors:
        if 'missing' in error_name:
            error_path = segment_radius_errors_folder + '/' + error_name + '.nii.gz'

    if error_name in conf.segment_radius_errors and "under" in error_name:
        if '1' in abbrv:
            error_name = conf.map_dictionary[abb] + '_subtle'
        if '2' in abbrv:
            error_name = conf.map_dictionary[abb] + '_moderate'
        if '3' in abbrv:
            error_name = conf.map_dictionary[abb] + '_severe'
        error_path = segment_radius_errors_folder + '/' + error_name + '.nii.gz'


    if error_name in conf.segment_radius_errors and "over" in error_name:
        if '1' in abbrv:
            error_name = conf.map_dictionary[abb] + '_subtle'
        if '2' in abbrv:
            error_name = conf.map_dictionary[abb] + '_moderate'
        if '3' in abbrv:
            error_name = conf.map_dictionary[abb] + '_severe'
        error_path = segment_radius_errors_folder + '/' + error_name + '.nii.gz'


    if error_name in conf.errors_to_add:
        if '1' in abbrv:
            error_name = conf.map_dictionary[abb] + '_subtle'
        if '2' in abbrv:
            error_name = conf.map_dictionary[abb] + '_moderate'
        if '3' in abbrv:
            error_name = conf.map_dictionary[abb] + '_severe'
        error_path = conf.root + "/" + patient + "/" + conf.errors_folder_name + "/" + conf.errors_to_add_folder + '/' + error_name + '.nii.gz'


    if error_name in conf.errors_to_subtract:
        if '1' in abbrv:
            error_name = conf.map_dictionary[abb] + '_subtle'
        if '2' in abbrv:
            error_name = conf.map_dictionary[abb] + '_moderate'
        if '3' in abbrv:
            error_name = conf.map_dictionary[abb] + '_severe'
        error_path = conf.root + "/" + patient + "/" + conf.errors_folder_name + "/" + conf.errors_to_subtract_folder + '/' + error_name + '.nii.gz'

    # returns a path list of all niftis which are to be included in creating an error simulation image
    return error_path


#creates all random voxel errors
def random_voxels_error_creation(patient):
    ground_truth_path = conf.root+"/" + patient + "/"+conf.ground_truth_folder_and_file_name + "/" + conf.ground_truth_folder_and_file_name + ".nii.gz"
    patient_TOF_MRI = conf.root + "/" + patient + "/" + conf.patient_images_folder_name + "/" + conf.patient_TOF_nifti
    errors_to_add_folder_path = conf.root + "/" + patient + "/" + conf.errors_folder_name+"/" + conf.errors_to_add_folder

    random_voxels(ground_truth_path,
                  patient_TOF_MRI,
                  errors_to_add_folder_path + "/" + conf.random_voxels_subtle)

    random_voxels(ground_truth_path,
                  patient_TOF_MRI,
                  errors_to_add_folder_path + "/" + conf.random_voxels_moderate)

    random_voxels(ground_truth_path,
                  patient_TOF_MRI,
                  errors_to_add_folder_path + "/" + conf.random_voxels_severe)


#saves all vessel segments Pcom M1 and ICA in different nifti files
def save_all_vessel_segments(patient):
    colored_nifti_path = conf.root + "/" + patient + "/" + conf.ground_truth_folder_and_file_name + "/" + conf.annotated_ground_truth_file_name
    only_Pcom_segment_path = conf.root + "/" + patient + "/" + conf.errors_folder_name + "/" + conf.artery_segment_folder + "/" + conf.Pcom_segment_file_name
    only_M1_segment_path = conf.root + "/" + patient + "/" + conf.errors_folder_name + "/" + conf.artery_segment_folder + "/" + conf.M1_segment_file_name
    only_Carotid_segment_path = conf.root + "/" + patient + "/" + conf.errors_folder_name + "/" + conf.artery_segment_folder + "/" + conf.Carotid_segment_file_name

    save_vessel_segments(colored_nifti_path, conf.Pcom, only_Pcom_segment_path)
    save_vessel_segments(colored_nifti_path, conf.M1, only_M1_segment_path)
    save_vessel_segments(colored_nifti_path, conf.ICA, only_Carotid_segment_path)


