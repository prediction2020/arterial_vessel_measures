from utils import search_utils as search_u
import pandas as pd
import AVE_config as conf


# create dataframes containing metric values for segmentations and rank segmentations from highest quality to lowest
def build_metric_tables(csv_metrics, all_metrics, evaluation_folder):
    print("....Creating dataframes and saving results for each metric")
    for metric_name in all_metrics:
        dictionary_of_a_metric = search_u.find_metric_to_dict(csv_metrics, metric_name)
        df = pd.DataFrame.from_dict(dictionary_of_a_metric, orient="index")
        df.rename(columns={0: metric_name}, inplace=True)
        # rank segmentations using metric values
        # note that similarity based metrics have high values
        # for segmentations of high quality (Dice, Volumetric similarity)
        # distance based metrics have low values
        # for segmentations of high quality (Hausdorff distance, average Hausdorff distance)
        # based on this the ranking is done separately for both metric families
        if metric_name in conf.similarity_based_metrics:
            df["rank"] = df[metric_name].rank(ascending=False, method="min")
        if metric_name in conf.distance_based_metrics:
            df["rank"] = df[metric_name].rank(ascending=True, method="min")

        df.to_csv(evaluation_folder + "/" + conf.metric_dataframes + "/" + metric_name + ".csv")


