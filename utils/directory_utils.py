import shutil
import os
from pathlib import Path
import AVE_config as conf


# copy paste a file from directory to to_directory with the searchword file
def simple_copy_paste_image(directory, to_directory, file="001.nii"):
    for x, y, z in (os.walk(directory)):
        for item in z:
            if file in item:
                image_to_copy = os.path.join(x, item)
                shutil.copy(image_to_copy, to_directory)


# function to copy and paste files with a certain search keyword
# to the evaluation folder and in separate folders within evaluation
def copy_paste_with_folder_name(searchdirectory, patient, run_name, file="001.nii",):
    for x, y, z in (os.walk(searchdirectory)):
        for item in z:
            if file in item:
                image_to_copy = os.path.join(x, item)
                # first leaves out(cuts) the filename of the path then (gets parent)
                cut = Path(image_to_copy).parent
                # gets the last element after / (gets folder name)
                folder_name = os.path.basename(cut)
                # folder_name becomes the file name while copying
                if ".csv" in image_to_copy:
                    shutil.copy(image_to_copy, conf.root + "/" + patient + "/" + run_name + "/"
                                + conf.evaluation_folder_name + "/" + conf.tree_metric_values
                                + "/" + folder_name + ".csv")


# creates a folder in base_directory with name directory_name_to_create
def create_a_directory(base_directory, directory_name_to_create):
    if not os.path.exists(base_directory + "/"+ directory_name_to_create):
        os.makedirs(base_directory + "/"+directory_name_to_create)
        print("....Created "+base_directory + "/" + directory_name_to_create)


# creates necessary directories for the run
def create_all_necessary_directories(patient, run_name):
    create_a_directory(conf.root + "/" + patient + "/" + run_name + "/" + conf.segmentation_folder_name, conf.ground_truth_folder_and_file_name)
    create_a_directory(conf.root + "/" + patient + "/" + conf.errors_folder_name, conf.artery_segment_folder)
    create_a_directory(conf.root + "/" + patient + "/" + run_name, conf.evaluation_folder_name)
    create_a_directory(conf.root + "/" + patient + "/" + conf.errors_folder_name, conf.errors_to_subtract_folder)
    create_a_directory(conf.root + "/" + patient + "/" + run_name + "/" + conf.evaluation_folder_name, conf.tree_metric_values)
    create_a_directory(conf.root + "/" + patient + "/" + run_name + "/" + conf.evaluation_folder_name, conf.metric_dataframes)
    print("Directories created")

