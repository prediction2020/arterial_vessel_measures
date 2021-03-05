import os
from pathlib import Path
import pandas as pd


# finds files(used to find error_files) and gives a dictionary as output
# this function is used only for manual error preparation
def find_error_file(directory, file="001.nii", search="string"):
    """
    finds files(used to find error_files) and gives a dictionary as output
    Args:
        directory: directory in which error nifti files are located
        file: specify file type using a string, for example "nii"
        search: search string should also be included in the file name

    Returns:
    """
    file_list = []
    suffix = []
    for x, y, z in (os.walk(directory)):
        for item in z:
            if file in item and search in item:
                image_to_find = os.path.join(x, item)
                file_list.append(image_to_find)
                suffix.append(item)
    error_suffix_dict = dict(zip(file_list, suffix))
    print("This is error suffix dict", error_suffix_dict)
    return error_suffix_dict


def find_list_to_evaluate(directory, file="001.nii"):
    """
    Finds files in a "directory" with the "file" name.
    returns a list of the folder names in the previous directory.
    For example for path root/patient/E1/segmentation.nii.gz
    the folder_name gives E1 which is the error string.
    See code documentation for details.

    Args:
        directory: the folder containing the segmentations should be given as the "directory" argument
        file: file name of the segmentation nifti

    Returns: a list of folder names containing the files.

    """
    segmentation_strings = []
    for x, y, z in (os.walk(directory)):
        for item in z:
            if file in item:
                image_to_evaluate = os.path.join(x, item)
                # first leaves out(cuts) the filename of the path then
                cut = Path(image_to_evaluate).parent
                # gets the last element after /
                folder_name = os.path.basename(cut)
                segmentation_strings.append(folder_name)
                print("....Getting segmentation paths to compare with ground_truth")
    return segmentation_strings


# In this code it is used to get all the csv files in the evaluation folder
def find_file(directory, file="001.nii", search="string"):
    """
    finds list of files in a directory with file extension containing the search string
    Args:
        directory: directory to search
        file: specify file type using a string, for example "nii"
        search: search string should be in the file name

    Returns: list of matching files

    """
    file_list = []
    for x, y, z in (os.walk(directory)):
        for item in z:
            if file in item and search in item:
                image_to_find = os.path.join(x, item)
                file_list.append(image_to_find)
    return file_list


# gets all the values of a metric (for example DICE) for every segmentation
# and makes a dictionary with error name and metric value
def find_metric_to_dict(list_of_csv_files, metric="DICE"):
    metric_value_list = []
    tree_names = []
    for path in list_of_csv_files:
        # gets the error name from the file name of the csv
        # to create a list(later to zip the to lists to create a dictionary)
        file_with_extension = os.path.basename(path)
        file_without_extension = os.path.splitext(file_with_extension)[0]
        tree_names.append(file_without_extension)
        # reads csv into dataframe
        metricsdataframe = pd.read_csv(path)
        # extracts from the csv the value of the metric
        metric_value = metricsdataframe.at[0, metric]
        metric_value_list.append(metric_value)
    # dictionary_of_a_metric contains all the values of one particular metric #
    # for the segmentations that are simulated in this run
    dictionary_of_a_metric = dict(zip(tree_names, metric_value_list))
    return dictionary_of_a_metric





