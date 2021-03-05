from utils import search_utils as search_u
import AVE_config as conf
from utils import directory_utils as dir_u
import statistics
import pandas as pd
import statistics as stats

#SUBANALYSIS INDEX OF DISPERSION AND MEDIAN VALUES CORRESPONDING TO VISUAL SCORES

# ANALYSIS OF MEDIAN VALUES CORRESPONDING TO VISUAL SCORES
# This analysis calculates the median performance measure value corresponding to visual scores 1 to 10.

#create a directory within results_folder called folder_name_of_analysis
dir_u.create_a_directory(conf.results_folder, conf.folder_name_of_analysis_IoD)

all_patient_median_metric_value_dict = {}

for metric_name in conf.all_usable_metrics:
    # initialize a list with possible visual scores as keys
    dict_of_median_metric_value_per_score = dict.fromkeys(conf.visual_scores)
    for score in conf.visual_scores:
        filtered_metric_values_list = []
        for patient in conf.patient_list:
            for set_name in conf.set_name_list:
                # the csv file containing the visual scores assigned to the simulated segmentations is located under the path "visual_score_df_path"
                visual_score_df_path = conf.root + "/" + patient + "/" + set_name + "/" + conf.evaluation_folder_name+ "/" + conf.metric_dataframes+ "/" + "visual_scores.csv"
                visual_score_df = pd.read_csv(visual_score_df_path)
                visual_score_df.set_index("Segmentation", inplace=True)

                # saves the identifiers(names) of segmentations with the given visual score
                # to the list segmentation_string_list_with_a_score
                segmentation_string_list_with_a_score = visual_score_df.index[visual_score_df["Score"] == score].tolist()
                # the csv file containing the metric values for segmentations is located under the path "metric_df_path"
                metric_df_path = conf.root + "/" + patient + "/" + set_name + "/" + conf.evaluation_folder_name + "/" + conf.metric_dataframes + "/" + metric_name + ".csv"

                metric_df = pd.read_csv(metric_df_path)
                metric_df.rename(columns={"Unnamed: 0" : "Segmentation"}, inplace=True)
                metric_df.set_index("Segmentation" , inplace=True)

                # filters the dataframe using the indentifiers(names) of segmentations receving the given visual score
                metric_df_filtered_based_on_score = metric_df.filter(items=segmentation_string_list_with_a_score, axis=0)
                #gets the metric values segmentations in the filtered dataframe
                filtered_metric_values_for_visual_score = list(metric_df_filtered_based_on_score[metric_name])
                # adds all filtered values to the "filtered_metric_values_list"
                for metric_value in filtered_metric_values_for_visual_score:
                    filtered_metric_values_list.append(metric_value)
        #updates the dictonary with the median metric value of segmentations receiving current visual score in the loop.
        dict_of_median_metric_value_per_score[score] = statistics.median(filtered_metric_values_list)

    # For all patients,the median metric values corresponding to all 10 visual scores are filtered and saved in dict_of_median_metric_value_per_score
    # the metric name is mapped with the median values by updating the "all_patient_median_metric_value_dict"
    print(metric_name)
    print(dict_of_median_metric_value_per_score)
    all_patient_median_metric_value_dict[metric_name] = dict_of_median_metric_value_per_score

median_value_visual_score_df = pd.DataFrame.from_dict(all_patient_median_metric_value_dict)
# the dataframe is transposed for better visualization
median_value_visual_score_df = median_value_visual_score_df.transpose()

print(median_value_visual_score_df)

median_value_visual_score_df.to_csv(conf.results_folder + "/" + conf.folder_name_of_analysis_IoD + "/" + conf.csv_file_name_to_save_median)

#
# INDEX OF DISPERSION ANALYSIS
# This analysis calculates the index of dispersion of performance measure (PM) values.
# Each segmentation (total= 2984) receives a PM value. There are a total of 22 PMs used in this study.
# For each PM, all 2984 values corresponding to 2984 different segmentations are used
# to calculate the index of dispersion.

def get_metric_values(metric):
    """
    Description: Takes a metric name as input and finds all values
    corresponding to that metric within the root directory.

    Args: metric: metric name as string, for example "DICE".
    Returns: a list of all values of the metric calculated in the run.
    """
    metric_values = []
    for patient in conf.patient_list:
        for set_name in conf.set_name_list:
            #csv file containing the metric values are located in the frollowing path "metric_df_path"
            metric_df_path = conf.root + "/" + patient + "/" + set_name + "/" + conf.evaluation_folder_name + "/" + conf.metric_dataframes + "/" + metric + ".csv"
            metric_df = pd.read_csv(metric_df_path)
            #the column name with the metric name contains the values
            metric_value_list_of_patient = list(metric_df[metric])
            #add all the values to the empty list "metric_values"
            for metric_value in metric_value_list_of_patient:
                metric_values.append(metric_value)
    return metric_values

#define empty dictionary for dispersion values
dict_of_dispersions = {}

for metric in conf.all_usable_metrics:
    #get all metric values to calculate the index of dispersion from
    metric_values_of_all_segmentations = get_metric_values(metric)

    # metric values of Conformity(CFM) and Sensibility(SENSBIL) are calculated as percentages
    # and therefore are divided by 100 for better comparison with other overlap based metrics which usually a range from 1-0.
    if metric == "CFM":
        d_int = 100
        metric_values_of_all_segmentations = [x / d_int for x in metric_values_of_all_segmentations]

    if metric == "SENSBIL":
        d_int = 100
        metric_values_of_all_segmentations = [x / d_int for x in metric_values_of_all_segmentations]
    #calculate the variance of metric values
    variance_of_metric_values =  stats.variance(metric_values_of_all_segmentations)
    #calculate the mean of metric values
    mean_of_metric_values = stats.mean(metric_values_of_all_segmentations)
    #calculate index of dispersion of metric values
    index_of_dispersion_of_metric_values = variance_of_metric_values / mean_of_metric_values
    #add calculated index of dispersion value to the dictionary "dict_of_dispersions"
    dict_of_dispersions[metric] = index_of_dispersion_of_metric_values
    #print(len(metric_values_of_all_segmentations))

#create a dataframe from the dictionary of dispersion values
df_of_dispersion = pd.DataFrame.from_dict(dict_of_dispersions, orient="index")

df_of_dispersion = df_of_dispersion.rename(columns= {0: "index_of_dispersion"})

#sort metrics based on their index of dispersion values from high to low
df_of_dispersion.sort_values(by="index_of_dispersion", ascending = False, inplace=True)

print(df_of_dispersion)
df_of_dispersion.to_csv(conf.results_folder + "/" + conf.folder_name_of_analysis_IoD + "/" + conf.csv_file_name_to_save_IoD )


