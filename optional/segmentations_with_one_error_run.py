import AVE_ES_functions as ES
import directory_utils as dir_u
import image_manipulation as img_manip
import search_utils as search_u
import dataframe_build as df_statistics
import AVE_config as conf

# optionally run this script to create segmentations containing only 1 manually created error per segmentation.
# The segmentations wil be compared with the ground truth using the metrics in the EvaluateSegmentation tool.
# https://github.com/Visceral-Project/EvaluateSegmentation

# this is the folder name in which the results will be saved within the root directory
set_name = "segmentations_containing_one_error"

def run_segmentations_with_one_error(patient, segmentation_set_name):
    """
    Creates simulated segmentations containing only 1 manually created error per segmentation
    Uses the errors in the list conf.all_errors
    Args:
        patient: patient string, for example "37"
        segmentation_set_name: name of the folder within the patient directory, for example "segmentations_containing_one_error"

    Returns: -

    """
    # create directories for this run
    dir_u.create_all_necessary_directories(patient, segmentation_set_name)
    # get the error nifti path for each error in the list conf.all_errors
    for element in conf.all_errors:
        print(element)
        paths = []
        path = img_manip.convert_abbr_to_path(element, patient)
        paths.append(path)
        #add or subtract the voxels from the ground truth using the add_multiple_nifti function
        img_manip.add_multiple_nifti(
            conf.root + "/" + patient + "/" + conf.ground_truth_folder_and_file_name + "/" + conf.ground_truth_folder_and_file_name + ".nii.gz",
            paths, patient, element, segmentation_set_name, seperator=False)
    #find all the segmentation niftis to compare against the ground truth
    list_of_segmentation_strings = search_u.find_list_to_evaluate(
        conf.root + "/" + patient + "/" + segmentation_set_name + "/" + conf.segmentation_folder_name, file=conf.segmentation_string)

    print("List of segmentation strings to be compared with the ground truth", list_of_segmentation_strings)

    ground_truth_folder_path = conf.root + "/" + patient + "/" + conf.ground_truth_folder_and_file_name

    error_tree_directory = conf.root + "/" + patient + "/" + segmentation_set_name + "/" + conf.segmentation_folder_name

    dir_u.create_a_directory(error_tree_directory, conf.ground_truth_folder_and_file_name)

    dir_u.simple_copy_paste_image(ground_truth_folder_path,
                                  error_tree_directory + "/" + conf.ground_truth_folder_and_file_name,
                                  file="ground_truth.nii.gz")
    # run EvaluateSegmentation to get metric values
    ES.evaluate_segmentation(conf.root + "/" + patient + "/" + segmentation_set_name + "/" + conf.segmentation_folder_name,
                             conf.executable_path, conf.goldstandard_string,
                             list_of_segmentation_strings, conf.string_prior, conf.string_after, conf.comment,
                             name_of_results_folder=conf.ES_results_folder)

    dir_u.copy_paste_with_folder_name(conf.root + "/" + patient + "/" + segmentation_set_name, patient, segmentation_set_name, file="all_metrics")

    # finds the csv file containing metric values for each error
    csv_metrics = search_u.find_file(
        conf.root + "/" + patient + "/" + segmentation_set_name + "/" + conf.evaluation_folder_name + "/" + conf.tree_metric_values,
        file=".csv", search="")

    # build for each metric a dataframe with metric values for each error
    df_statistics.build_metric_tables(csv_metrics, conf.all_metrics,
                                      conf.root + "/" + patient + "/" + segmentation_set_name + "/" + conf.evaluation_folder_name)

# RUN
for patient in conf.patient_list:
    run_segmentations_with_one_error(patient, set_name)













