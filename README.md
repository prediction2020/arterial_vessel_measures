# arterial_vessel_measures
## Overview 
This repository contains the code for our performance measure selection framework based on manual visual scoring of simulated segmentations to find the optimal performance measures for arterial cerebral vessel segmentation.

## Publication
## Data
We used imaging data from 10 patients from the 1000Plus study that enrolled patients with steno-occlusive cerebrovascular disease. At the current time-point the imaging data cannot be made publicly accessible due to data protection.

## How to use
### Dependencies
#### EvaluateSegmentation tool
- Executable file for ubuntu: 

https://github.com/Visceral-Project/EvaluateSegmentation/blob/master/builds/Ubuntu/EvaluateSegmentation-2020.08.28-Ubuntu.zip 

#### Python and packages
- Nibabel 
- Pandas
- Scipy
- Matplotlib
- Scikit learn
- Python version 3.8.5

An environment.yml file can be found in the repository. 

### Directories and Paths
#### Before Run
```
-root
 |
 ---- patient_1
 |    |
 |    ---- errors
 |    |     |
 |    |     ---- errors_to_add
 |    |     |
 |    |     ---- errrors_to_subtract
 |    |     |
 |    |     ---- segments
 |    |     |
 |    |     ---- segment_radius_errors
 |    |     |
 |    |     ---- already_error_trees
 |    |
 |    |
 |    ---- ground_truth
 |    |   |
 |        ---- annotated_vessel_tree.nii.gz
 |    |
 |    |
 |    ---- patient_images
 |    |   |
 |    |   ---- patient_TOF.nii.gz
 |     
 ---- patient_2
 |
 ---- ...
 |
 ---- patient_10
 |
 ---- ES
     |
     ---- EvaluateSegmentation
```

#### After the Run
```
-root
 |
 ----patient_1
 |    |
 |    ---- errors
 |    |    |
 |    |    ---- errors_to_add
 |    |    |
 |    |    ---- errrors_to_subtract
 |    |    |
 |    |    ---- segments
 |    |    |
 |    |    ---- segment_radius_errors
 |    |    |
 |    |    ---- already_error_trees
 |    |
 |    |
 |    ---- ground_truth
 |    |    |
 |    |    ---- annotated_vessel_tree.nii.gz
 |    |
 |    |
 |    ---- patient_images
 |    |    |
 |    |    ---- patient_TOF.nii.gz
 |    | 
 |    ---- segmentation_set
 |    |    |
 |    |    ---- Error_Simulations
 |    |    |
 |    |    ---- ES_results 
 |    |    |
 |    |    ---- Evaluation
 |    |    |    |
 |    |    |    ---- metric_dfs
 |    |    |    |    |
 |    |    |    |    ---- DICE.csv
 |    |    |    |    |
 |    |    |    |    ---- ...
 |    |    |    |    |
 |    |    |    |    ---- AVD.csv
 |    |    |    |    | 
 |    |    |    |    ---- visual_scores.csv
 |    |    |    | 
 |    |    |    |  
 |    |    |    ---- metric_dfs_filtered_high_quality_1_5
 |    |    |    | 
 |    |    |    ---- metric_dfs_filtered_low_quality_6_10 
 |    |    |    |
 |    |    |    ---- tree_metric_values 
 |    |    |      
 |    |    ---- information.txt
 | 
 |  
 ---- patient_2
 |
 ---- ...
 |
 ---- patient_10
 |
 ---- Results
 |    |    |
 |    |    ---- Subanalysis_index_of_dispersion_and_median_values
 |    |    |    |
 |    |    |    ---- all_patient_median_metric_values_of_visual_scores.csv
 |    |    |    |
 |    |    |    ---- index_of_dispersion_dataframe.csv
 |    |    |     
 |    |    |
 |    |    ---- Visual_score_correlation_analysis
 |    |    |    |
 |    |    |    ---- correlation_analysis
 |    |    |    |
 |    |    |    ---- correlation_analysis_filtered_high_quality_1_5
 |    |    |    | 
 |    |    |    ---- correlation_analysis_filtered_low_quality_6_10
 |
 |
 ----ES
     |
     ----EvaluateSegmentation

```
### File and folder descriptions

**errors_to_add** : contains error niftis that can be added to the ground truth directly to simulate false positive segmentation errors.

**errors_to_subtract** : contains error niftis that can be subtracted from the ground truth directly to simulate false positive segmentation errors.

**segments** : contains binary vessel segments extracted from the  annotated_vessel_tree.nii.gz. These can be used to manually create errors.

**segment_radius_errors** : contains errors that are ready to be subtracted or added to the ground truth that manipulate vessel segments like Pcom, M1 or ICA. 

**already_error_trees** : contains error nifty that are created by manipulating the ground truth directly. These need to be processed with error_creation_and_preperation.py before they can be freely combined with other errors.

**annotated_vessel_tree.nii.gz** : An annotated version created from the ground_truth.nii.gz where vessel segments Pcom M1 and ICA are labeled with different colors(different vessel IDs) in ITK-SNAP.  The identifiers for the vessels can be found in the Vessel_IDs.txt file which can be directly imported to ITK-SNAP. 

**patient_TOF.nii.gz** : The original TOF MRI of the patient. Used for the creation of  random_voxels_error 

**Error_simulations** : contains folders with the following structure. The simulated segmentation variations are stored in this folder.
 
```
 ---- “C0_H2_E1”
 |    |
 |    ---- segmentation.nii.gz  
 |     
 ---- “C92_M91_R2_V3_G1”
 |    |
 |    ---- segmentation.nii.gz  
 |     
 ---- ...

```
**ES_results** : contains the performance measure values for each of the simulated segmentation variations. Has the following structure:
“Folder_name_indicating_time_of_the_run” like “20210303-215158”
```
---- “20210303-215158” (“Folder_name_indicating_time_of_the_run”)
     |
     ---- “C0_H2_E1”
     |    |
     |    ---- all_metrics.csv
     |     
     ---- “C92_M91_R2_V3_G1”
     |    |
     |    ---- all_metrics.csv  
     |     
     ---- ...

```
**Evaluation** : “metric_dfs” contains a csv for each metric with metric values and rankings from highest quality to lowest. It also contains a file visual_scores.csv which contains the visual scores assigned to the segmentations in the given segmentation set.

**information.txt**  : Contains information about properties of the segmentation set so that the user can make sure the segmentation set is within defined boundary conditions. See below Step 3. 

**Subanalysis_index_of_dispersion_and_median_values** : See Table 5 in the publication.

**All_patient_median_metric_values_of_visual_scores.csv** : Median performance measure values in the run corresponding to different visual scores are provided.

**Index_of_dispersion_dataframe.csv** : Index of dispersion for each metric is calculated.

**Visual_score_correlation_analysis** : This is the main analysis of the performance measure selection framework. The segmentations are ranked from highest to lowest quality as assessed by 22 different metrics. This ranking is called the metric ranking. Also a visual score is assigned to each segmentation. The metric providing the metric ranking with the highest correlation with the visual scores should be chosen an is the most suitable metric for the task at hand.  

**EvaluateSegmentation**:  The EvaluateSegmentation tool executable file. This path should be defined in the AVE_config.py 

 
## Code Files

Environment yml file:
- environment.yml
 
Config file:
- AVE_config.py

Utils:
- directory_utils.py
- image_manipulation.py
- search_utils.py
- dataframe_build.py 
- AVE_ES_functions_.py 

Execution files:
- MAIN_segmentation_simulation_and_evaluation.py
- Analysis_main_visual_score_rank_correlation.py
- Subanalysis_index_of_dispersion_and_mean_values.py
- Subanalysis_subgroup_good_bad_quality_preparation.py

Optional:
- error_creation_and_preperation.py
- segmentations_with_one_error_run.py

Text files:
- Vessel_IDs.txt

Contents

**utils**: helper functions for the whole framework can be found here.

**optional**: files not essential for the performance measure selection framework.


## PERFORMANCE MEASURE SELECTION FRAMEWORK

Instructions on how to use the performance measure selection framework can be found in the manual.md file.

**Notes:** 

Terms metric and performance measure are used interchangeably in the comments and variable names within the code, although mathematically they are different. 





