from itertools import combinations
import random
from utils import directory_utils as dir_u
from utils import AVE_ES_functions as ES
from utils  import image_manipulation as img_manip
from utils import search_utils as search_u
from utils import dataframe_build as df_statistics
import AVE_config as conf
import pandas as pd
import asyncio


# This is the main python file to execute for the simulating segmentation variations
# and getting performance measure values using the EvaluateSegmentation executable

# FUNCTIONS
def remove_unwanted_combinations(list_of_combinations, unwanted_combination_dictionary):
    """
    This functions removes unwanted error combinations from a list of error combinations strings
    For example: before: ["C0_K2_V2_E2","P0_P991_K3_V1"]
                 after:  ["C0_K2_V2_E2"]
    The segmentation P0_P991_K3_V1 contains two mutually exclusive errors P0 and P991 and the string is therefore removed from the list.

    Args:
        list_of_combinations: List of error combination strings(segmentation identifiers)
                              from which the unallowed/unwanted strings are removed.

        unwanted_combination_dictionary: Dictionary defined in AVE_config which defines the mutually exclusive errors

    Returns: new list with only allowed segmentation strings

    """
    # loops through the unwanted_combination_dictionary and combinations to check for unwanted error combinations
    unwantedList = []
    for combination in list_of_combinations:
        for unwantedKey, listOfUnwantedValues in unwanted_combination_dictionary.items():
            if unwantedKey in combination:
                for unwantedValue in listOfUnwantedValues:
                    if unwantedValue in combination:
                        unwantedList.append(combination)
    new = list(set(list_of_combinations) - set(unwantedList))
    # returns the new_combination list free of unwanted error combinations
    return new


def get_all_simulated_errors_save_in_a_list(planned_combinations_dictionary):
    """
    This function gets all single errors included in a planned combinations dictionary
    and returns them in a list

    Args:
        planned_combinations_dictionary:
        For example: {... 3: [("E1","K2","P0"), ("V1","E1", "H2")] ...}

    Returns: flat_list_of_all_errors: ["E1","K2","P0","V1","E1","H2"]

    """
    planned_combinations_list = list(planned_combinations_dictionary.values())
    flat_list_of_all_errors = []
    for x in planned_combinations_list:
        for k in x:
            for i in k:
                flat_list_of_all_errors.append(i)
    return flat_list_of_all_errors

# counts how many times an error in conf.all_errors occurs in a list flat_list_of_all_errors
# and returns a dictionary with keys as error strings and values number of occurence of the error in the list
def get_number_of_occurrence_for_each_simulated_error(flat_list_of_all_errors):
    e_dict = {}
    for k in conf.all_errors:
        e_dict[k] = flat_list_of_all_errors.count(k)
    return e_dict

# returns a list the keys of the dictionary d which have the value val
# used to get the error names that have already reached the maximum cap of occurence.
def get_key(d, val):
    already_capped_error_list = []
    for key, value in d.items():
        if val == value:
            already_capped_error_list.append(key)
    return already_capped_error_list

# checks if a and b have common elements.
def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    if len(a_set.intersection(b_set)) > 0:
        return (True)
    return (False)



def create_simulated_segmentation_pool(iterable_to_choose_errors_from, unwanted_dict,
                                       number_of_errors_in_segmentation):
    """
    # Function to plan simulated segmentations variations, calculates all possible combinations of errors to generate segmentation strings.

    Args:
        iterable_to_choose_errors_from: Errors to be included should be given as a list, for example: conf.all_errors
        unwanted_dict: mutually exclusive errors should be specified here, for example : conf.unwanted_dict
        number_of_errors_in_segmentation: how many errors should each segmentation contain, input an integer from 2 to 7.

    Returns: simulated_segmentation_pool: if number_of_errors_in_segmentation is 3 simulated_segmentation_pool will look like this {3: [ ('P993', 'C992', 'M91'), ('P91', 'H2', 'G1')] }

    """
    # For the low error counts it is computationally feasible to calculate all the possible combinations.
    # an empty dictionary is created to save all combinations containing 2-6 errors.
    simulated_segmentation_pool = {}

    all_combinations = combinations(iterable_to_choose_errors_from, number_of_errors_in_segmentation)
    all_comb_list = []
    for i in all_combinations:
        all_comb_list.append(i)
    # removes unwanted/restricted combinations from the combination list for every count of combinations
    all_comb_list = remove_unwanted_combinations(all_comb_list, unwanted_dict)
    # assigns the error count as the key of the dictionary: simulated_segmentation_pool and the created combinations list: all_comb_list as the value corresponding to the dictionary.
    simulated_segmentation_pool[number_of_errors_in_segmentation] = all_comb_list
    print(all_comb_list)
    print("Calculating all possible simulated segmentations containing " + str(
        number_of_errors_in_segmentation) + "errors")
    return simulated_segmentation_pool


# returns the dict without the keys specified in key_list
def without(dict, key_list):
    new_d = dict.copy()
    for key in key_list:
        if key in dict:
            new_d.pop(key)
    return new_d


# PLANNING A SET OF SIMULATED SEGMENTATIONS
# Choose the first random simulated segmentation
# gets one random segmentation string from all possible segmentations to initiate the planning of a balanced segmentation set
def plan_first_simulated_segmentation(all_possible_comb_dict,error_count_within_segmentation):
    first_simulated_segmentation_dict={}
    segmentation_pool_for_first_simulated_segmentation = all_possible_comb_dict[error_count_within_segmentation]
    # first_simulated_segmentation_dict contains the error groups which will be contained in the first simulated segmentation. It looks like the following {3: [('E', 'C', 'M99')]}
    first_simulated_segmentation_dict[error_count_within_segmentation] = random.sample(segmentation_pool_for_first_simulated_segmentation, 1)
    return first_simulated_segmentation_dict

# save properties of the created segmentation set in a text file in "information.txt".
# This is to ensure that the boundary conditions for the segmentation set are fulfilled.
# Example output looks like this:
# This is the current error counts in the simulation
# {2: 48, 3: 48, 4: 48, 5: 47, 6: 56, 7: 50}
# This dictionary tracks the number of occurrence for each error:
# {'P0': 28, 'P91': 28, 'P92': 28, 'P93': 28, 'P991': 27, 'P992': 28, 'P993': 26, 'C0': 27, 'C91': 27, 'C92': 28, 'C93': 27, 'C991': 29, 'C992': 26, 'C993': 26, 'M0': 25, 'M91': 29, 'M92': 26, 'M93': 26, 'M991': 27, 'M992': 27, 'M993': 28, 'T1': 28, 'T2': 29, 'T3': 27, 'N1': 30, 'N2': 29, 'N3': 30, 'H1': 29, 'H2': 30, 'H3': 29, 'K1': 30, 'K2': 29, 'K3': 28, 'G1': 29, 'G2': 29, 'G3': 28, 'R1': 30, 'R2': 29, 'R3': 28, 'V1': 27, 'V2': 29, 'V3': 29, 'S1': 30, 'S2': 29, 'S3': 30, 'E1': 28, 'E2': 29, 'E3': 30}
# Total number of simulated segmentations in the set:
# 297
def get_error_counts_and_occurence_of_errors_for_a_simulation_set_save_as_txt(error_count_list,balanced_error_simulation_set,patient,segmentation_set):
    current_error_counts_simulated = dict.fromkeys(error_count_list, 0)
    for key in balanced_error_simulation_set:
        current_error_counts_simulated[key] = len(balanced_error_simulation_set[key])

    flat_list_of_all_errors = get_all_simulated_errors_save_in_a_list(balanced_error_simulation_set)

    occurrence_dict_of_errors = get_number_of_occurrence_for_each_simulated_error(flat_list_of_all_errors)

    print(sum(current_error_counts_simulated.values()))
    with open(conf.root + "/" + patient + "/" + segmentation_set+"/"+"information.txt", 'w') as f:
        print("This is the current error counts in the simulation", file=f)
        print(current_error_counts_simulated, file=f)
        print("This dictionary tracks the number of occurrence for each error:", file=f)
        print(occurrence_dict_of_errors, file=f)
        print("Total number of simulated segmentations in the set:", file=f)
        print(str(sum(current_error_counts_simulated.values())), file=f)
        f.close()

# create an empty dataframe with segmentation strings as index "Segmentation" and column name "Score"
# where the user will input the visual scores the segmentation variations receive.
def create_empty_dataframe_for_visual_scores(csv_metrics, evaluation_folder):
    # any metric dataframe is taken to extract the segmentation strings
    metric_name = "DICE"

    dictionary_of_a_metric = search_u.find_metric_to_dict(csv_metrics, metric_name)

    df = pd.DataFrame.from_dict(dictionary_of_a_metric, orient="index")
    df.rename(columns={0: "Score"}, inplace=True)

    df["Score"].values[:] = 0
    df.index.name = "Segmentation"

    df.to_csv(evaluation_folder + "/" + conf.metric_dataframes + "/" + "visual_scores.csv")

# a function that calls the function create_simulated_segmentation_pool to get all possible error combinations.
def get_all_possible_error_combinations():
    # define empty dictionary where all possible error combinations will be stored
    all_possible_combinations_dict = {}

    # All theoretically possible combinations of the errors in the list all_errors(total number 48) are calculated
    # using the function create_simulated_segmentation_pool for simulated segmentations containing 2,3,4,5,6,7 errors respectively.
    segmentation_pool_simulated_segmentation_2 = create_simulated_segmentation_pool(conf.all_errors, conf.unwanted_dict, 2)
    segmentation_pool_simulated_segmentation_3 = create_simulated_segmentation_pool(conf.all_errors, conf.unwanted_dict, 3)
    segmentation_pool_simulated_segmentation_4 = create_simulated_segmentation_pool(conf.all_errors, conf.unwanted_dict, 4)
    segmentation_pool_simulated_segmentation_5 = create_simulated_segmentation_pool(conf.all_errors, conf.unwanted_dict, 5)
    segmentation_pool_simulated_segmentation_6 = create_simulated_segmentation_pool(conf.all_errors, conf.unwanted_dict, 6)
    segmentation_pool_simulated_segmentation_7 = create_simulated_segmentation_pool(conf.all_errors, conf.unwanted_dict, 7)

    # the resulting dictionaries segmentation_pool_simulated_segmentation 1-7 are stored in the dictionary all_possible_combinations_dict
    # this dict looks like following {2: [('T1', 'E3'), ('K2', 'G1'), ...all possible segmentations with 2 errors... ],
    #                                3: [ ('P993', 'C992', 'M91'), ('P91', 'H2', 'G1'), ...all possible segmentations with 3 errors... ],
    #                                ....
    #                                7: [(...all possible segmentations with 7 errors ...)],}
    all_possible_combinations_dict = {**segmentation_pool_simulated_segmentation_2, **segmentation_pool_simulated_segmentation_3,
                                      **segmentation_pool_simulated_segmentation_4, **segmentation_pool_simulated_segmentation_5,
                                      **segmentation_pool_simulated_segmentation_6, **segmentation_pool_simulated_segmentation_7}
    return all_possible_combinations_dict


# this is the main function that ensures a balanced representation of errors in the created segmentaiton sets.
# 4 boundary conditions are defined in the code documentation.
def create_balanced_combination_group_for_simulation(all_possible_comb_dict, error_count_per_segmentation, max_number_of_error_occurrence_in_run = 4 ):
    # start palnning the set with one segmentation selected from all possible error combinations
    planned_simulated_segmentation_dictionary = plan_first_simulated_segmentation(all_possible_comb_dict, error_count_per_segmentation)
    segmentation_pool_simulated_segmentation = {}

    segmentation_pool_simulated_segmentation[error_count_per_segmentation] = all_possible_comb_dict[error_count_per_segmentation]
    # keeps track of how many times there were no possible segmentations to add to the planned dictionary if it exceeds a certain number it is
    failed_attempts_to_add_segmentation = 0
    # a variable to configure to restart the planning after the number of failed attempts to add segmentation to planning
    restart_run_after_x_failed_attempts = 30

    #add new simulated segmentations to the planned run dictionary until all errors are represented in a balanced way.
    while True:
        #flat_list_of_all_errors is a list to count the occurrence of errors in the planned_simulated_segmentation_dictionary.
        flat_list_of_all_errors = get_all_simulated_errors_save_in_a_list(planned_simulated_segmentation_dictionary)

        occurrence_dict_of_errors = get_number_of_occurrence_for_each_simulated_error(flat_list_of_all_errors)
        print("This dictionary tracks the number of occurrence for each error: ", occurrence_dict_of_errors)
        # occurrence_list_of_errors is used to break out of the while loop to confirm that the planned set of simulations is balanced
        occurrence_list_of_errors = list(occurrence_dict_of_errors.values())
        #the error name of the least represented error(error with lowest number of occurence until now) is saved to the variable least_represented_error
        least_represented_error = min(occurrence_dict_of_errors, key = occurrence_dict_of_errors.get)
        print("This is the least represented error: ", least_represented_error)

        # gives a list of errors that have already reached the maximum number limit of occurrence in the planned simulation
        already_capped_error_list = get_key(occurrence_dict_of_errors, max_number_of_error_occurrence_in_run)
        occurrence_dict_of_errors_without_capped_errors = without(occurrence_dict_of_errors, already_capped_error_list)

        same_error_group_list = []

        first_letter_of_error_name = least_represented_error[:1]

        for x in conf.all_errors:
            if first_letter_of_error_name in x:
                same_error_group_list.append(x)

        occurrence_dict_of_errors_without_capped_errors_without_least_represented_error_group = without(
            occurrence_dict_of_errors_without_capped_errors, same_error_group_list)

        min_value = occurrence_dict_of_errors[least_represented_error]


        min_represented_e_list = []
        for key in occurrence_dict_of_errors_without_capped_errors_without_least_represented_error_group:
            # print(key)
            if occurrence_dict_of_errors_without_capped_errors_without_least_represented_error_group[key] == min_value:
                min_represented_e_list.append(key)
            if occurrence_dict_of_errors_without_capped_errors_without_least_represented_error_group[key] == min_value + 1:
                min_represented_e_list.append(key)

        if len(min_represented_e_list) >= 1:
            second_least_represented_error = random.choice(min_represented_e_list)
            third_least_represented_error = random.choice(min_represented_e_list)

        # most_represented_error = max(occurrence_dict_of_errors_without_capped_errors, key=occurrence_dict_of_errors.get)
        # print("this is the most represented error", most_represented_error)

        #gives the occurrence number of errors that are most represented until now in the planned simulation,
        if len(occurrence_dict_of_errors_without_capped_errors) > 0:
            max_represented_value = max(occurrence_dict_of_errors_without_capped_errors.values())
        #print("this is max represented value", max_represented_value)

        max_represented_error_list = [error_name  for error_name, occurrence_num in occurrence_dict_of_errors_without_capped_errors.items() if occurrence_num == max_represented_value]

        #empty dictionary initialized with values 0 from the "error_count_list", current_error_counts_simulated keeps track of how many simulated segmentations aere currently planned in the planned_simulated_segmentation_dictionary
        current_error_counts_simulated = {}

        #for key in planned_simulated_segmentation_dictionary:
        current_error_counts_simulated[error_count_per_segmentation] = len(planned_simulated_segmentation_dictionary[error_count_per_segmentation])
        print("This is the current segmentation count in the simulation group (boundary condition 3)", current_error_counts_simulated[error_count_per_segmentation])
        total_segmentation_count = current_error_counts_simulated[error_count_per_segmentation]


        #in each iteration the available_seg_pool is filled with simulated segmentations from segmentation_pool_simulated_segmentation
        available_seg_pool = []
        #loop through all simulated segmentations in the merged_simulated_segmentation_pool
        for simulated_segmentation in segmentation_pool_simulated_segmentation[error_count_per_segmentation]:
            # only simulated segmentations not already included in the planned segmentation dicitonary can be added.
            # (otherwise the same segmentation variation would occur more than one time in a segmentation set.)
            if simulated_segmentation not in planned_simulated_segmentation_dictionary[error_count_per_segmentation]:
                #print(simulated_segmentation)
                # only simulated segmentations containing the least represented errors are added.
                # The 3 least represented errors until this point in the planned_simulated_segmentation_dictionary are identified
                # and should be included in the next simulated segmentation variation to be added.
                if least_represented_error in simulated_segmentation:
                    if second_least_represented_error in simulated_segmentation:
                        if error_count_per_segmentation == 2:
                            # if an error has reached its max_number_of_error_occurrence_in_run the error cannot be included in the simulated segmentation
                            if not common_member(already_capped_error_list, simulated_segmentation):
                                # the 15 most represented errors cannot be in the simulated segmentation, this way the simulated segmentation is forced to contain errors that are represented less until now in the planned_simulated_segmentation_dictionary
                                if max_represented_value == max_number_of_error_occurrence_in_run - 1:
                                    available_seg_pool.append(simulated_segmentation)
                                if not common_member(max_represented_error_list[:15], simulated_segmentation):
                                    available_seg_pool.append(simulated_segmentation)
                        else:
                            if third_least_represented_error in simulated_segmentation:
                                # if an error has reached its max_number_of_error_occurrence_in_run the error cannot be included in the simulated segmentation
                                if not common_member(already_capped_error_list, simulated_segmentation):
                                    #the 15 most represented errors cannot be in the simulated segmentation, this way the simulated segmentation is forced to contain errors that are represented less until now in the planned_simulated_segmentation_dictionary
                                    if max_represented_value == max_number_of_error_occurrence_in_run - 1:
                                        available_seg_pool.append(simulated_segmentation)
                                    if not common_member(max_represented_error_list[:15], simulated_segmentation):
                                        available_seg_pool.append(simulated_segmentation)

        print("Length of the available segmentation pool", len(available_seg_pool))

        #if there are not any available segmentations and there enough tries have been made to add a segmentation variation to the planning the while loop ends returning the final simulated segmentation dictionary for the run.
        if len(available_seg_pool) == 0:
            # everytime there are no available segmentations to add to the planning the variable is increased to keep track of failed attempts.
            failed_attempts_to_add_segmentation += 1
            # if the boundary condition 3 is fulfilled
            if conf.max_total_segmentation_count_per_group >= total_segmentation_count >= conf.min_total_segmentation_count_per_group:
                # the following 3 if statements are to account for the variable number of errors in a segmentation. See boundary condition 4 in code documentation.
                if min(occurrence_list_of_errors) == max_number_of_error_occurrence_in_run:
                    to_save = planned_simulated_segmentation_dictionary
                    return to_save

                if error_count_per_segmentation == 5:
                    if min(occurrence_list_of_errors) + 1 >= max_number_of_error_occurrence_in_run:
                        to_save = planned_simulated_segmentation_dictionary
                        return to_save

                if error_count_per_segmentation > 5:
                    if min(occurrence_list_of_errors) + 2 >= max_number_of_error_occurrence_in_run:
                        to_save = planned_simulated_segmentation_dictionary
                        return to_save

            if failed_attempts_to_add_segmentation > restart_run_after_x_failed_attempts:
                #print(count_available_seg_pool_length)
                planned_simulated_segmentation_dictionary = plan_first_simulated_segmentation(all_possible_comb_dict, error_count_per_segmentation)
                failed_attempts_to_add_segmentation = 0
                print("RESTARTING")
            continue

        #the simulated segmentation is randomly picked from the available_seg_pool
        random_picked_simulated_segmentation = random.sample(available_seg_pool, k = 1)
        #print(list(random_picked_simulated_segmentation[0]))
        random_picked_simulated_segmentation = list(random_picked_simulated_segmentation[0])
        #print("this is planned_combinations_dict",planned_simulated_segmentation_dictionary)

        #sets the value to [] if the key doesnt exist in the dictionary yet
        planned_simulated_segmentation_dictionary.setdefault(error_count_per_segmentation, [])

        #the random_picked_simulated_segmentation is added to the planned_simulated_segmentation_dictionary
        planned_simulated_segmentation_dictionary[error_count_per_segmentation].append(random_picked_simulated_segmentation)


# funtion to get the total number of segmentations in the set. See boundary conditon 1 in the code documentation.
def size_of_planned_segmentation_set(balanced_simulation_set):
    size_of_set = dict.fromkeys(conf.error_count_list, 0)
    for x in balanced_simulation_set:
        size_of_set[x] = len(balanced_simulation_set[x])
    print(sum(size_of_set.values()))
    number_of_total_segmentations = sum(size_of_set.values())
    print("Size of the segmentation set is:" ,number_of_total_segmentations)
    return number_of_total_segmentations

# summary function that calls the function create_balanced_combination_group_for_simulation for each error count group in boundary condition 2.

def func_balanced_set(all_possible_combinations_dict):
    segmentations_with_2_errors = create_balanced_combination_group_for_simulation(all_possible_combinations_dict,2, 2)
    segmentations_with_3_errors = create_balanced_combination_group_for_simulation(all_possible_combinations_dict,3, 3)
    segmentations_with_4_errors = create_balanced_combination_group_for_simulation(all_possible_combinations_dict,4, 4)
    segmentations_with_5_errors = create_balanced_combination_group_for_simulation(all_possible_combinations_dict,5, 5)
    segmentations_with_6_errors = create_balanced_combination_group_for_simulation(all_possible_combinations_dict,6, 8)
    segmentations_with_7_errors = create_balanced_combination_group_for_simulation(all_possible_combinations_dict,7, 8)

    balanced_error_simulation_set = {**segmentations_with_2_errors ,**segmentations_with_3_errors,
                              **segmentations_with_4_errors ,**segmentations_with_5_errors,
                              **segmentations_with_6_errors, **segmentations_with_7_errors}
    return balanced_error_simulation_set


# using asyncio utilize all threads of the system CPU for parallel calculation
# background is required to achive parallel run together with asyncio
def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped

@background

# run function to create balanced segmentation sets complying with the boundary conditions for each patient.
# The function also runs EvaluateSegmentation tool and saves results in the defined directories.
def run(all_possible_combinations_dict, patient, segmentation_set):
    dir_u.create_all_necessary_directories(patient, segmentation_set)

    # BOUNDARY CONDITION 1
    n = 0
    while True:
        n += 1
        balanced_error_simulation_set = func_balanced_set(all_possible_combinations_dict)
        total_number_of_segmentations_in_the_set = size_of_planned_segmentation_set(balanced_error_simulation_set)
        if conf.total_segmentation_count_in_the_set_lower_limit <= total_number_of_segmentations_in_the_set <= conf.total_segmentation_count_in_the_set_upper_limit:
            print("DONE", balanced_error_simulation_set)
            get_error_counts_and_occurence_of_errors_for_a_simulation_set_save_as_txt(conf.error_count_list,balanced_error_simulation_set,patient,segmentation_set)
            break
        # after two tries adjust boundary condition warning and stop code
        if n > 2:
            print("The chosen range for total number of segmentations is not possible")
            raise Exception()

    #save properties of the created set in a text file
    get_error_counts_and_occurence_of_errors_for_a_simulation_set_save_as_txt(conf.error_count_list,balanced_error_simulation_set,patient,segmentation_set)

    for key, value in balanced_error_simulation_set.items():
        for element in value:
            paths = []
            print(element)
            for error_code in element:
                print(error_code)
                path = img_manip.convert_abbr_to_path(error_code, patient)
                paths.append(path)
            img_manip.add_multiple_nifti(
                conf.root + "/" + patient + "/" + conf.ground_truth_folder_and_file_name + "/" + conf.ground_truth_folder_and_file_name + ".nii.gz",
                paths, patient, element, segmentation_set, seperator=True)

    list_of_segmentation_strings = search_u.find_list_to_evaluate(conf.root + "/" + patient + "/" + segmentation_set + "/" + conf.segmentation_folder_name, file= conf.segmentation_string)

    ground_truth_folder_path = conf.root + "/" + patient + "/" + conf.ground_truth_folder_and_file_name

    error_tree_directory = conf.root + "/" + patient + "/" + segmentation_set + "/" + conf.segmentation_folder_name

    dir_u.create_a_directory(error_tree_directory, conf.ground_truth_folder_and_file_name)

    dir_u.simple_copy_paste_image(ground_truth_folder_path,
                                  error_tree_directory + "/" + conf.ground_truth_folder_and_file_name,
                                  file="ground_truth.nii.gz")

    ES.evaluate_segmentation(conf.root + "/" + patient + "/" + segmentation_set + "/" + conf.segmentation_folder_name,conf.executable_path, conf.goldstandard_string,
                             list_of_segmentation_strings, conf.string_prior, conf.string_after, conf.comment, name_of_results_folder=conf.ES_results_folder)

    dir_u.copy_paste_with_folder_name(conf.root + "/" + patient + "/" + segmentation_set, patient,segmentation_set, file="all_metrics")

    # finds the csv file containing metric values for each error
    csv_metrics = search_u.find_file(conf.root + "/" + patient + "/" + segmentation_set + "/" + conf.evaluation_folder_name  + "/" + conf.tree_metric_values,file=".csv", search="")

    # build for each metric a dataframe with metric values for each error and required steps for analysis
    df_statistics.build_metric_tables(csv_metrics, conf.all_metrics, conf.root + "/" + patient + "/" + segmentation_set + "/" + conf.evaluation_folder_name)

    create_empty_dataframe_for_visual_scores(csv_metrics, conf.root + "/" + patient + "/" + segmentation_set + "/" + conf.evaluation_folder_name)

# RUN CODE
# Note that this code can take up to 2 hours to generate a segmentation set depending on how strict the boundary conditions are.
all_possible_combinations_dict = get_all_possible_error_combinations()
for patient in conf.patient_list:
    for segmentation_set in conf.set_name_list:
        run(all_possible_combinations_dict, patient, segmentation_set)
