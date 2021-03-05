import os
import re
import xml.etree.cElementTree as ET
import pandas as pd
import time
from AVE_config import *
from pathlib import Path


#this function finds the relevant paths defined according to the unique strings in config.py for goldstandards and segmentations
def find_paths(rootdir, goldstandard_string, segmentation_string):
    goldstandard_paths = []
    segmentation_paths = []
    subdirectories = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            path = (os.path.join(subdir, file))
            print(path)
            if re.search(goldstandard_string, path):
                goldstandard_paths.append(path)
                subdirectories.append(subdir)
            if re.search(segmentation_string, path):
                #adds path to segmentation paths only if the the folder has the same name with segmentation string
                cut = Path(path).parent
                folder_name = os.path.basename(cut)
                if folder_name == segmentation_string:
                    segmentation_paths.append(path)
    return(goldstandard_paths, segmentation_paths, subdirectories)

#extract the patient ID according to the defined strings
def extract_patient_id(path, index_string, end_string):
    index = path.find(index_string)
    index_end = path.find(end_string, index)
    patient = path[index + len(index_string): index_end]
    return patient


#compare segmentations based on the EvaluateSegmentation software of Taha et al
def segment_comparison(goldstandard_paths, segmentation_paths, executable_path, results_folder_path, string_prior, string_after):
    indx = 0
    for path in goldstandard_paths:
        os.chdir(executable_path)
        patient = extract_patient_id(path, string_prior, string_after)
        gold_path = "\ ".join(goldstandard_paths[indx].split(" "))
        segment_path = "\ ".join(segmentation_paths[indx].split(" "))
        #mm string
        #command_string = r"./EvaluateSegmentation" + " " + gold_path + " " + segment_path + " " + "-unit" + " " + "millimeter" + " " + "-use" + " "+ evaluation_string + " " + "-xml" + " " + "\ ".join(results_folder_path.split(" ")) +  "/" + patient + "_" + "Evaluation.xml"
        #voxel_string
        command_string = r"./EvaluateSegmentation" + " " + gold_path + " " + segment_path + " " + "-use" + " "+ evaluation_string + " " + "-xml" + " " + "\ ".join(results_folder_path.split(" ")) +  "/" + patient + "_" + "Evaluation.xml"

        os.system(command_string)
        print(command_string)
        indx += 1


#a function that returns a list of all relevant paths of our xml_files

def find_xml_paths(results_folder_path, Evaluation_xml_string = "Evaluation.xml"):
    Evaluations_xmls = []
    for subdir, dirs, files in os.walk(results_folder_path):
        for file in files:
            path = (os.path.join(subdir, file))
            if re.search(Evaluation_xml_string, path):
                Evaluations_xmls.append(path)
    return(Evaluations_xmls)

#parse the xml file and create dataframes for the relevant metric data. Also, save the dataframe data into csvs
def parse_xml(results_folder_path):
    #get the paths of all xmls
    Evaluations_xmls = find_xml_paths(results_folder_path)


    #get all the metrics as a list
    list_of_measures = []

    for path in Evaluations_xmls[:1]:
        tree = ET.parse(path)
        root = tree.getroot()
        for child in root.findall(".//metrics/*"):
            list_of_measures.append(child.attrib["symbol"])
            # get the data for each patient corresponding to header>

    #save the header into a list. First entry of a list of lists that will later be converted into a pandas dataframe
    header_and_patients = []

    header_and_patients.append(list_of_measures)

    # find patient number + patient values for the metrics
    indices = []

    for path in Evaluations_xmls:
        patient_values = []
        tree = ET.parse(path)
        root = tree.getroot()

        # find patient name and add to indices that are saved
        for path in root.findall("fixed-image"):
            string = (path.attrib["filename"])
            ind_string = "patients/"
            end_string = "/TOF_Source"
            index = string.find(ind_string)
            index_end = string.find(end_string, index)
            patient = string[index + len(ind_string):index_end]

            indices.append(patient)

        # find all values for the metrics and add them to the values
        for child in root.findall(".//metrics/*"):
            value = child.attrib["value"]
            patient_values.append(value)


        # append the values of the current patient to the list of lists
        header_and_patients.append(patient_values)


    # import list of lists as pandas dataframe
    df = pd.DataFrame(header_and_patients[1:], index=indices, columns=header_and_patients[0])

    #change metric values to int/float

    for measure in list_of_measures:
        df[measure] = df[measure].apply(pd.to_numeric)

    #save final dataframe

    df.to_csv(results_folder_path + "/" + "02_all_metrics.csv")

    # gather stat_values

    stat_list = []
    for measure in list_of_measures:
        description = df[measure].describe()
        stat_list.append(description)

    stat_df = pd.DataFrame()
    for entry in stat_list:
        stat_df = pd.concat([stat_df, entry], axis=1,sort=True)

    # save stats
    stat_df.to_csv(results_folder_path + "/" + "03_descriptive_stats.csv")
    return(stat_df)



#save a report with all relevant information
def save_report(results_folder_path, rootdir, executable_path, goldstandard_string, list_of_segmentation_strings, string_prior, string_after, comment, goldstandard_paths, segmentation_paths, subdirectories):
    a = locals()
    args = []
    for key,value in sorted(a.items()):
        if isinstance(key, str):
            row = [key] + [str(value)]
            args.append(",".join(row))
        else:
            for lst in value:
                row = [key] + [str(lst)]
                args.append(",".join(row))

    reportpath = os.path.join(results_folder_path + r"/" + r"01_report.txt")
    report = open(reportpath, "w")

    report.write("\n".join(args))
    report.close()

#create dictionary of 4 confusion matrix values
def create_dict_from_xml(xml_path, metrics_list=["TP", "FP", "TN", "FN"]):
    value_metrics_dic = []
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for child in root.findall(".//metrics/*"):
        if child.tag in metrics_list:
            value_metrics_dic.append(child.attrib["value"])
    metrics_dic = dict(zip(metrics_list, value_metrics_dic))
    return metrics_dic


#calculate_sensibility
def calculate_sensibility(metrics_dic):
    fp = int(metrics_dic["FP"])
    fn = int(metrics_dic["FN"])
    tp = int(metrics_dic["TP"])

    valsensibility = (1-fp/(tp+fn))*100

    return valsensibility

#calculate_conformity
def calculate_conformity(metrics_dic):
    fp = int(metrics_dic["FP"])
    fn = int(metrics_dic["FN"])
    tp = int(metrics_dic["TP"])

    valconformity = ((1-(fp + fn)/tp))*100

    return valconformity


#include Sensibility and Conformity into our Evaluation xmls

def sensibility_conformity_to_xml(results_folder_path):

    Evaluations_xmls = find_xml_paths(results_folder_path)
    for xml_path in Evaluations_xmls:

        tree = ET.parse(xml_path)
        root = tree.getroot()

        metrics_dic = create_dict_from_xml(xml_path)

        valsensibility = calculate_sensibility(metrics_dic)
        valconformity =  calculate_conformity(metrics_dic)

        sensibility_attributes= {"name": "sensibility","value":str(valsensibility),"symbol":"SENSBIL","type":"similarity","unit":"voxel" }
        SENSBIL = ET.Element("SENSBIL", attrib = sensibility_attributes)
        conformity_attributes= {"name": "conformity","value":str(valconformity),"symbol":"CFM","type":"similarity","unit":"voxel" }
        CFM = ET.Element("CFM",attrib = conformity_attributes)
        root[2].insert(2, SENSBIL)
        root[2].insert(3, CFM)

        tree.write(xml_path)


# main function
def evaluate_segmentation(rootdir, executable_path, goldstandard_string, list_of_segmentation_strings, string_prior, string_after,comment, name_of_results_folder="/Results"):
    #create Resultsfolder that is unique for each run
    time_string = time.strftime("%Y%m%d-%H%M%S")
    resultspath = os.path.join(os.path.dirname(rootdir) + name_of_results_folder + "/" + time_string)
    if not os.path.exists(resultspath):
        os.makedirs(resultspath)
    #loop over each segmentation type that is defined in the "run" document
    for segmentation_string in list_of_segmentation_strings:
        #get all paths within the patient directory using the find_paths function
        goldstandard_paths, segmentation_paths, subdirectories = find_paths(rootdir, goldstandard_string, segmentation_string)
        print(segmentation_string)
        print(goldstandard_paths)
        print(segmentation_paths)
        print(subdirectories)
        #make a folder for the segmentation results
        results_folder_path = os.path.join(resultspath + "/" + segmentation_string)
        os.makedirs(results_folder_path)
        #compare the segmentation with the segment_comparison function and save the xml files in the results folder
        segment_comparison(goldstandard_paths, segmentation_paths, executable_path, results_folder_path, string_prior, string_after)
        #parse the generated xmls and insert two more metrics: Sensibility and Conformity
        sensibility_conformity_to_xml(results_folder_path)
        #parse the xml files in each folder, do stats and save the dataframes as csvs with the parse_xml function
        stat_df = parse_xml(results_folder_path)
        #save a report with all relevant information
        save_report(results_folder_path, rootdir, executable_path, goldstandard_string, list_of_segmentation_strings, string_prior, string_after, comment, goldstandard_paths, segmentation_paths, subdirectories)
