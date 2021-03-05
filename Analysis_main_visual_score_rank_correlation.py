import AVE_config as conf
import pandas as pd
from scipy.stats import spearmanr, kendalltau
from utils import directory_utils as dir_u
from utils import search_utils as search_u

# DESCRIPTION
# This analysis calculates the spearman rank correlation coefficient of the following:
# 1. Visual scores assigned to simulated segmentations
# with
# 2. Metric rankings of these simulated segmentations

# The metric that produces the ranking with the highest correlation with the visual scores is the most suitable metric
# for performance assesment for the chosen segmentation task(cerebral vessel segmentation).
#
# The analysis can be performed on subgroups of segmentations
# for example only with simulated segmentations that received a score of 1-5 (see Subanalyis_subgroup_good_bad_quality.py).

# FUNCTIONS
def visual_score_correlation(metric_df_path, visual_score_df):
    """
    # the function calculates the correlation between the visual scores and
    # the ranking of segmentations resulting from metric values.

    Args:
        metric_df_path: csv file path where the segmentations are ranked based
        on the metric values they received from most similar to the ground truth
        to least similar to ground truth.

        visual_score_df: visual score dataframe that contains the visual scores
        assigned to the segmentations.

    Returns: the spearman correlation coefficient rho between the metric rankings and visual scores

    """
    # get the dataframe containing the metric values for the simulated segmentations
    metric_df = pd.read_csv(metric_df_path)
    # save the "rank" column of the metric_df in a list called metric_rank_list
    metric_rank_list = list(metric_df["rank"])
    # if the stirng "filtered" is in the dataframe path this means the analysis will be performed on a subgroup
    # which is selected based on visual scores (see Subanalysis_subgroup_good_bad_quality.py).
    # For this the updated rank_after_filter column is taken for calculation.
    if "filtered" in metric_df_path:
        metric_rank_list = list(metric_df["rank_after_filter"])

    # convert the "Score" column of the visual score dataframe to a list
    visual_score_rank_list = list(visual_score_df["Score"])
    # calculate the spearmans correlation coefficient of the two lists mentioned above and store the correlation value in rho.
    rho, p_val = spearmanr(visual_score_rank_list, metric_rank_list)
    # return the correlation(rho) of the metric ranking with visual scores
    return rho

def create_overview_correlation_dataframe(visual_score_df, patient, set_name, analysis_folder_name_to_save):
    """
    For a given patient this function calls the "visual_score_correlation" function
    and saves the correlation results for each metric in a dataframe.

    Args:
        visual_score_df: visual score dataframe that contains the visual scores
        assigned to the segmentations.
        patient: patient identifier for example "37"
        set_name: name of the segmentation set folder within the patient folder, for example "segmentation_set"
        analysis_folder_name_to_save: name of the folder where the results should be saved

    Returns: -

    """
    # create an empty dictionary with all metric names as keys
    correlation_values_dict_spearman = dict.fromkeys(conf.all_usable_metrics, None)
    # repeats the steps for each metric to be analyzed
    for metric_name in conf.all_usable_metrics:
        # path for the dataframe containing the metric values and ranking for the simulated segmentations
        metric_dataframe_path = conf.root + "/" + patient + "/" + set_name + "/" + conf.evaluation_folder_name + "/" + dataframes_folder_name + "/" + metric_name + ".csv"
        #calculate correlation between visual scores and metric rankings
        correlation_of_metric_spearman = visual_score_correlation(metric_dataframe_path, visual_score_df)
        # store the resulting correlation value of a metric in the dictionary "correlation_values_dict_spearman" with metric name as key and correlation value as value
        correlation_values_dict_spearman[metric_name] = correlation_of_metric_spearman
    #create a dataframe from the above dictionary which stores all the spearman correlation values for each metric for the given patient
    correlation_with_visual_rankings_overview_spearman = pd.DataFrame.from_dict(correlation_values_dict_spearman, orient='index')

    # 0 is the column name of the dataframe correlation_with_visual_rankings_overview
    correlation_with_visual_rankings_overview_spearman.sort_values(ascending=False, by=0, inplace=True)
    # rename the first column of the dataframe
    correlation_with_visual_rankings_overview_spearman.rename(columns={correlation_with_visual_rankings_overview_spearman.columns[0]: "Correlation with visual ranking"}, inplace=True)
    # save the dataframe with the patient name within the csv file name in the conf.results_folder
    correlation_with_visual_rankings_overview_spearman.to_csv(conf.results_folder + "/" + conf.visual_correlation_analysis_folder_name + "/" + analysis_folder_name_to_save + "/" + patient + "correlation_with_visual_ranking_df_spearman.csv")

def get_metric_correlations_and_create_median_df(path_list_of_dfs_to_calculate_median):
    """
    Calculates the median value of spearman correlation coefficients from dataframes saved in the conf.results_folder

    Args:
             path_list_of_dfs_to_calculate_median: the paths of dataframes of each patient with stored spearman correlation coefficients for each  metric

    Returns:
             overview_df: an overview dataframe of all spearman correlation coefficients of all patients and metrics.
             median_correlation_df : the final dataframe with median spearman correlation coefficients of all patients.

    """
    # create two empty dataframes
    overview_df = pd.DataFrame()
    median_correlation_df = pd.DataFrame()

    for df_path in path_list_of_dfs_to_calculate_median:
        #the df_to_add of each patient will be concataneted to the overview dataframe
        df_to_add = pd.read_csv(df_path)
        df_to_add = df_to_add.rename(columns={"Unnamed: 0": "metric_name"})
        # sets the index of the sample dataframe to ERROR
        df_to_add = df_to_add.set_index("metric_name")
        overview_df = pd.concat([overview_df, df_to_add], axis=1)
        #the median of spearman rank correlation values is calculated and stored in a dataframe
        median_correlation_df = overview_df.median(axis=1)
    return overview_df, median_correlation_df


# CODE
# create necessary directories
dir_u.create_a_directory(conf.results_folder, conf.visual_correlation_analysis_folder_name)

#conf.run dictionary contains the strings for segmentation groups 1. main analysis group(all segmentations) 2. subgroup good quality segmentations(visual scores 1-5) 3. subgroup bad quality (visual scores 6-10)

for key, value in conf.run_dictionary.items():
    dataframes_folder_name = key
    analysis_folder_name_to_save = value

    # create necessary directories
    dir_u.create_a_directory(conf.results_folder + "/" + conf.visual_correlation_analysis_folder_name, analysis_folder_name_to_save)

    for patient in conf.patient_list:
        for set_name in conf.set_name_list:
            # the path for the csv file where the visual scores of segmentations are stored
            scoring_sheet_path = conf.root + "/" + patient + "/" + set_name + "/"+ conf.evaluation_folder_name + "/" + dataframes_folder_name + "/visual_scores.csv"
            scoring_df = pd.read_csv(scoring_sheet_path)

            create_overview_correlation_dataframe(scoring_df, patient, set_name, analysis_folder_name_to_save)
    # finds all csv files containing the string "correlation_with_visual_ranking_df_spearman" within the directory of analysis_folder_name_to_save, these csv files contain the spearman correlation coefficients
    all_spearman_metric_correlations = search_u.find_file(conf.results_folder + "/" + conf.visual_correlation_analysis_folder_name + "/" + analysis_folder_name_to_save, ".csv", "correlation_with_visual_ranking_df_spearman")
    # calculate median spearman rank correlation coefficient
    spearman_correlation_df, median_spearman_correlation_df = get_metric_correlations_and_create_median_df(all_spearman_metric_correlations)

    spearman_correlation_df.to_csv(conf.results_folder + "/" + conf.visual_correlation_analysis_folder_name + "/" +
                                   analysis_folder_name_to_save + "/" + "spearman_correlation.csv")
    # sort the metrics by correlation values from highest to lowest
    median_spearman_correlation_df.sort_values(ascending=False, inplace=True)

    median_spearman_correlation_df = pd.DataFrame(median_spearman_correlation_df)

    median_spearman_correlation_df.columns = ["Spearman correlation"]

    # results are rounded after the third decimal
    median_spearman_correlation_df = median_spearman_correlation_df.round(3)

    median_spearman_correlation_df.to_csv(conf.results_folder + "/" + conf.visual_correlation_analysis_folder_name + "/" +  analysis_folder_name_to_save + "/" + "median_spearman_correlation.csv")