import pandas as pd
import AVE_config as conf
from utils import directory_utils as dir_u

# SUB_ANALYSIS BASED ON SUBGROUPS OF SEGMENTATIONS WITH GOOD(visual scores 1-5) AND BAD QUALITY(visual scores 6-10)
# This code divides the segmentations into 2 subgroups based on visual scores as described above.
# This code must be executed prior to continuing with ......ANALYSIS_PYTHON_SCRIPT......

# different subgroups and the scores defining these subgroups are given in the subgroup_dictionary.
for key, value in conf.subgroup_dictionary.items():
    # the string that describes the subgroup is "filtered_segmentation_description_string"
    filtered_segmentation_description_string = key
    # lower and upper visual scores are defined in the list which is the value of the "subgroup_dictionary"
    score_lower_limit = value[0]
    score_upper_limit = value[1]

    for patient in conf.patient_list:
        for set_name in conf.set_name_list:
            # the visual scores assigned to the segmentations are found in the csv file under the following path.
            scoring_sheet_csv_path = conf.root + "/" + patient + "/" + set_name + "/" + conf.evaluation_folder_name + "/" + conf.metric_dataframes + "/" + conf.visual_scoring_csv_file_name

            # read csv into s dataframe, rename column and set index
            visual_score_df = pd.read_csv(scoring_sheet_csv_path)
            visual_score_df.rename(columns={"Unnamed: 0": "Segmentation"}, inplace=True)
            visual_score_df.set_index("Segmentation", inplace=True)

            # get names(identifiers) of segmentations which received the a visual score within the visual score upper and lower limit
            above_lower_limit = visual_score_df["Score"] >= score_lower_limit
            below_upper_limit = score_upper_limit >= visual_score_df["Score"]
            segmentation_string_list_within_a_visual_score_range = visual_score_df.index[above_lower_limit & below_upper_limit].tolist()

            # filter the dataframe based on segmentation identifiers
            filtered_visual_scores_df = visual_score_df.filter(
                items=segmentation_string_list_within_a_visual_score_range, axis=0)

            print(filtered_visual_scores_df)

            #create a folder with the name of the "filtered_segmentation_description_string" to store the filtered visual score dataframe
            dir_u.create_a_directory(conf.root + "/" + patient + "/" + set_name + "/" + conf.evaluation_folder_name , filtered_segmentation_description_string)

            save_filtered_visual_scores_df_path = conf.root + "/" + patient + "/" + set_name + "/" + conf.evaluation_folder_name + "/" + filtered_segmentation_description_string + "/" + conf.visual_scoring_csv_file_name

            # save filtered_visual_scores_df
            filtered_visual_scores_df.to_csv(save_filtered_visual_scores_df_path)

            # the following for loop filters the metric values of segmentations with the above defined visual score ranges and saves the filtered dataframes to
            for metric_name in conf.all_usable_metrics:
                #csv file containing the metric values is located under the following path in each patient directory
                metric_df_path = conf.root + "/" + patient + "/" + set_name + "/" + conf.evaluation_folder_name + "/" + conf.metric_dataframes + "/" + metric_name + ".csv"

                metric_df = pd.read_csv(metric_df_path)
                metric_df.rename(columns={"Unnamed: 0": "Segmentation"}, inplace=True)
                metric_df.set_index("Segmentation", inplace=True)

                #metric dataframe is filtered based on the identifers/names of segmentations receiving visual scores within the range defined for teh subgroup.
                filtered_metric_df = metric_df.filter(items=segmentation_string_list_within_a_visual_score_range, axis=0)

                # Segmentations are re ranked from most similar to ground truth to least similar to the ground truth as reflected by the metric value
                # (the rank of each segmentation was previously calculated so the ranking is done using the prior ranking:
                # Example: 1-2-3-4-5-6-7 after filtering becomes 1-4-6-7 and this is re ranked as 1-2-3-4).
                filtered_metric_df["rank_after_filter"] = filtered_metric_df["rank"].rank(method="min")

                save_filtered_metric_df_path = conf.root + "/" + patient + "/" + set_name + "/" + conf.evaluation_folder_name + "/" + filtered_segmentation_description_string + "/" + metric_name + ".csv"
                filtered_metric_df.to_csv(save_filtered_metric_df_path)

