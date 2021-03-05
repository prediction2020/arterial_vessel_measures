# CONFIG FILE
# linux root
root = "/home/user/Desktop/folder"

# folder within root where analysis results should be saved
results_folder = root + "/" + "Results"

# variables to configure for segmentation simulation
patient_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

set_name_list = ["segmentation_set"]

# BOUNDARY CONDITION 1, see code documentation for details
total_segmentation_count_in_the_set_upper_limit = 305
total_segmentation_count_in_the_set_lower_limit = 295

# BOUNDARY CONDITION 2, see code documentation for details
error_count_list = [2, 3, 4, 5, 6, 7]

# BOUNDARY CONDITION 3, see code documentation for details
min_total_segmentation_count_per_group = 45
max_total_segmentation_count_per_group = 60


# MAIN RANK CORRELATION ANALYSIS
# name of the file containing visual scores and segmentation strings.
visual_scoring_csv_file_name = "visual_scores.csv"

visual_correlation_analysis_folder_name = "visual_score_correlation_analysis"

# dictionary mapping folder names to results folder names
run_dictionary = {"metric_dfs": "correlation_analysis",
                  "metric_dfs_filtered_high_quality_1_5": "correlation_analysis_filtered_high_quality_1_5",
                  "metric_dfs_filtered_low_quality_6_10": "correlation_analysis_filtered_low_quality_6_10"}

# Sub-analysis with subgroups of bad and good quality segmentations, values represent visual score ranges
subgroup_dictionary = {"metric_dfs_filtered_high_quality_1_5": [1, 5],
                       "metric_dfs_filtered_low_quality_6_10": [6, 10]}

# Sub-analysis index of dispersion(Iod) and median values
visual_scores = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

folder_name_of_analysis_IoD = "Subanalysis_index_of_dispersion_and_median_values"

csv_file_name_to_save_median = "all_patient_median_metric_values_of_visual_scores.csv"

csv_file_name_to_save_IoD = "index_of_dispersion_dataframe.csv"

# nifti file names and folder names
patient_images_folder_name = "patient_images"
patient_TOF_nifti = "patient_TOF.nii.gz"

# define file name of the annotated ground truth
annotated_ground_truth_file_name = "annotated_vessel_tree.nii.gz"

# ground truth file and the folder in which the annotated ground truth is located have the same name
ground_truth_folder_and_file_name = "ground_truth"

# all types of errors are located within the folder with the name specified with errors_folder_name variable
errors_folder_name = "errors"

# these folders are subdirectories of errors_folder_name directory
errors_to_add_folder = "errors_to_add"
errors_to_subtract_folder = "errors_to_subtract"
error_already_as_tree_folder = "already_error_trees"
# errors that depend on changing the radius of segments should be located in this folder within errors before the run
artery_segment_errors = "segment_radius_errors"

# artery segments are taken from the annotated ground_truth and saved within this folder
# this variable is used in error_creation_and_preparation
artery_segment_folder = "segments"

# niftis containing the segments have following file names
Pcom_segment_file_name = "Pcom.nii.gz"
M1_segment_file_name = "M1.nii.gz"
Carotid_segment_file_name = "Carotid.nii.gz"


# Vesseli-IDs to manipulate certain vessel segmnents, Vessel IDs can be found in the Vessel_IDs.txt document in GIT under same directory as this file.
# Vessel ids represent the color of the labels manually segmented using ITK-SNAP.
Pcom = 18
M1 = 4
ICA = 5

# the folder where the segmentations and ground truth is saved during the run:
# evaluate segmentation takes this folder as root folder
segmentation_folder_name = "Error_Simulations"

# Main results are located within this folder in run_name folder
evaluation_folder_name = "Evaluation"

# folders for better overview in evaluation also used in code so dont remove
# all segmentation comparison results saved into metric specific dataframes are located in this folder
metric_dataframes = "metric_dfs"

# csv files for each error containing all metrics are found here
tree_metric_values = "tree_metric_values"


# random voxel_error file names for each intensity
random_voxels_subtle = "random_voxels_error_subtle.nii.gz"
random_voxels_moderate = "random_voxels_error_moderate.nii.gz"
random_voxels_severe = "random_voxels_error_severe.nii.gz"


# ERROR TYPES
# some errors need to be added to the ground truth and
# some errors need to be subtracted from the ground truth,
# other errors manipulate the radius of artery segments.

# string identifiers for errors to be subtracted from the ground truth
errors_to_subtract = ["small_vessels_error"]

# string identifiers for errors to be added to the ground truth
errors_to_add = ["random_voxels_error", "meningea_media_error",
                 "hyperintens_meninges_error", "eye_error", "seperation_error",
                 "skull_error", "sagittal_sinus_error", "sigmoid_error"]

# string identifiers for errors manipulating the radius of vessel segments
segment_radius_errors = ["M1_error_missing", "M1_error_under", "M1_error_over",
                         "Pcom_error_missing", "Pcom_error_under", "Pcom_error_over",
                         "ICA_error_missing", "ICA_error_under", "ICA_error_over"]


# mapping of abbreviations and their corresponding error strings
map_dictionary = {"T": "sagittal_sinus_error",
                  "N": "meningea_media_error", "H": "hyperintens_meninges_error",
                  "K": "skull_error", "V": "small_vessels_error", "S": "seperation_error",
                  "G": "sigmoid_error", "E": "eye_error", "R": "random_voxels_error",
                  "P": "Pcom_error_missing", "P9": "Pcom_error_under", "P99": "Pcom_error_over",
                  "C": "ICA_error_missing", "C9": "ICA_error_under", "C99": "ICA_error_over",
                  "M": "M1_error_missing", "M9": "M1_error_under", "M99": "M1_error_over",
                }


# a list containing all errors simulated in a run
all_errors = ['P0', 'P91', 'P92', 'P93', 'P991', 'P992',
              'P993', 'C0', 'C91', 'C92', 'C93', 'C991', 'C992', 'C993', 'M0', 'M91', 'M92', 'M93', 'M991', 'M992',
              'M993', 'T1', 'T2', 'T3', 'N1', 'N2', 'N3', 'H1', 'H2', 'H3', 'K1', 'K2', 'K3', 'G1', 'G2', 'G3', 'R1', 'R2',
              'R3', 'V1', 'V2', 'V3', 'S1', 'S2', 'S3', 'E1', 'E2', 'E3']


# Some combinations of errors are not possible because they manipulate the same segment.
# The key is mutually exclusive with any elements of the list in the value.
# For example P0 cannot be combined with "P91", "P991", "P92", "P992", "P93" or  "P993".
# The unwanted_dict below is used in ... to remove unwanted combinations from the segmentation pool.
unwanted_dict = {
    "N1": ["N2", "N3"],
    "N2": ["N1", "N3"],
    "N3": ["N1", "N2"],

    "H1": ["H2", "H3"],
    "H2": ["H1", "H3"],
    "H3": ["H1", "H2"],

    "K1": ["K2", "K3"],
    "K2": ["K1", "K3"],
    "K3": ["K1", "K2"],

    "E1": ["E2", "E3"],
    "E2": ["E1", "E3"],
    "E3": ["E1", "E2"],

    "V1": ["V2", "V3"],
    "V2": ["V1", "V3"],
    "V3": ["V1", "V2"],

    "T1": ["T2", "T3"],
    "T2": ["T1", "T3"],
    "T3": ["T1", "T2"],

    "G1": ["G2", "G3"],
    "G2": ["G1", "G3"],
    "G3": ["G1", "G2"],

    "S1": ["S2", "S3"],
    "S2": ["S1", "S3"],
    "S3": ["S1", "S2"],

    "R1": ["R2", "R3"],
    "R2": ["R1", "R3"],
    "R3": ["R1", "R2"],

    "C0": ["C91", "C991", "C92", "C992", "C93", "C993"],
    "C91": ["C0", "C991", "C92", "C992", "C93", "C993"],
    "C92": ["C0", "C91", "C991", "C992", "C93", "C993"],
    "C93": ["C0", "C91", "C991", "C92", "C992", "C993"],
    "C991": ["C0", "C91", "C92", "C992", "C93", "C993"],
    "C992": ["C0", "C91", "C991", "C92", "C93", "C993"],
    "C993": ["C0", "C91", "C991", "C92", "C992", "C93"],

    "M0": ["M91", "M991", "M92", "M992", "M93", "M993"],
    "M91": ["M0", "M991", "M92", "M992", "M93", "M993"],
    "M92": ["M0", "M91", "M991", "M992", "M93", "M993"],
    "M93": ["M0", "M91", "M991", "M92", "M992", "M993"],
    "M991": ["M0", "M91", "M92", "M992", "M93", "M993"],
    "M992": ["M0", "M91", "M991", "M92", "M93", "M993"],
    "M993": ["M0", "M91", "M991", "M92", "M992", "M93"],

    "P0": ["P91", "P991", "P92", "P992", "P93", "P993"],
    "P91": ["P0", "P991", "P92", "P992", "P93", "P993"],
    "P92": ["P0", "P91", "P991", "P992", "P93", "P993"],
    "P93": ["P0", "P91", "P991", "P92", "P992", "P993"],
    "P991": ["P0", "P91", "P92", "P992", "P93", "P993"],
    "P992": ["P0", "P91", "P991", "P92", "P93", "P993"],
    "P993": ["P0", "P91", "P991", "P92", "P992", "P93"]}




# PERFORMANCE MEASURES/METRICS
# All metrics to be calculated with Evaluate_Segmentations during the run.
# Here also "HDRFDST@0.95@" should be specified to calculate the 95th quantile of the Hausdorff Distance
metrics_to_evaluate = ["DICE", "JACRD", "FMEASR", "SNSVTY", "SPCFTY", "FALLOUT", "PRCISON", "ACURCY", "AVGDIST", "bAVD",
                       "HDRFDST@0.95@", "PROBDST", "MAHLNBS", "ICCORR", "KAPPA", "AUC", "MUTINF", "VARINFO", "RNDIND",
                       "ADJRIND", "VOLSMTY", "GCOERR", "TP", "TN", "FP", "FN"]

evaluation_string = ",".join(metrics_to_evaluate)


# list of metrics including Sensibility and Conformity
all_metrics = ["DICE", "JACRD", "FMEASR", "SNSVTY", "SPCFTY", "FALLOUT", "PRCISON", "ACURCY", "AVGDIST",
               "bAVD", "HDRFDST", "PROBDST", "MAHLNBS", "ICCORR", "KAPPA", "AUC", "MUTINF", "VARINFO",
               "RNDIND", "ADJRIND", "VOLSMTY", "GCOERR", "TP", "TN", "FP", "FN", "SENSBIL", "CFM"]

# metrics that cannot be used with this framework or are redundant
not_usable_metrics = ["TP", "TN", "FP", "FN", "SEGVOL", "REFVOL", "FALLOUT"]

# usable for the framework
all_usable_metrics = set(all_metrics) - set(not_usable_metrics)

distance_based_metrics = ["AVGDIST", "bAVD", "HDRFDST", "MAHLNBS", "PROBDST", "GCOERR", "VARINFO"]
# all remaining metrics from "all_metrics" after subtracting no_penalization_metrics and distance_based_metrics
similarity_based_metrics = list((set(all_metrics)-set(not_usable_metrics)) - set(distance_based_metrics))


# config VARIABLES for the evaluate segmention tool
# define path for the "EvaluateSegmentation" executable file for the OS system used.
# Currently there is an up-to-date version provided in Ubuntu/linux only.
# For other OS executable file should be built from source code.
# https://github.com/Visceral-Project/EvaluateSegmentation
executable_path = r"/home/orhun/Nextcloud/NIFTI/Team_Research/Project_Orhun/Metrics_Project/ES"

# define the ground truth string. Please use here the full name of the file
# Be advised that the name must be the same for all patients!
goldstandard_string = "ground_truth.nii.gz"

# all files to be compared to the ground truth must have the file name specified in segmentatation_string
segmentation_string = "segmentation.nii.gz"

# results folder where ES results should be saved
ES_results_folder = "/" + "ES_results"

# define patient identifiers. For this, in your paths define the strings before and after the patient name.
# example: root/patients/PEG0005/TOF_Source
# in this case the string_prior is "patients/" and the string_after is "/TOF_Source
string_prior = segmentation_folder_name + "/"

string_after = ""

comment = ""

