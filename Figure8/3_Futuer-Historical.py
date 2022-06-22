import os
from collections import defaultdict


def get_reference_datapath(rootpath):
    res = defaultdict(list)
    for dir2 in os.listdir(rootpath):
        if "Reference" in dir2:
            key = dir2.split("_")[1]
            path2 = rootpath + "/" + dir2
            if os.path.isdir(path2):
                for dir3 in os.listdir(path2):
                    if dir3.endswith(".nc") and (not dir3.startswith("._")):
                        res[key].append(path2 + "/" + dir3)
    return res


if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Resampled"
    reference = get_reference_datapath(rootpath)
    replace_tag = ""
    for key in reference.keys():
        for reference_data in reference[key]:
            tag = "_".join(reference_data.split("/")[-1].split("_")[0:2])
            for dir2 in os.listdir(rootpath):
                if "Reference" not in dir2 and key in dir2:
                    if "median" in dir2:
                        replace_tag = "EnsembleMedian"
                    elif "quarter-25" in dir2:
                        replace_tag = "Quarter-25"
                    else:
                        replace_tag = "Quarter-75"
                    path2 = rootpath + "/" + dir2
                    if os.path.isdir(path2):
                        for dir3 in os.listdir(path2):
                            if dir3.startswith(tag) and dir3.endswith(".nc") and (not dir3.startswith("._")):
                                nc_in = path2 + "/" + dir3
                                nc_out1 = "/Volumes/OneTouch/Calculated_Indices_FutureAnalysis/10_Temporal+Spatial/Sub/" + "_".join(dir3.replace(replace_tag, replace_tag + "-Sub").split("_")[2:4]) + "/" + dir3.replace(replace_tag, replace_tag + "-Sub")
                                nc_out11 = "/Volumes/OneTouch/Calculated_Indices_FutureAnalysis/10_Temporal+Spatial/SubMean/" + "_".join(dir3.replace(replace_tag, replace_tag + "-SubMean").split("_")[2:4]) + "/" + dir3.replace(replace_tag, replace_tag + "-SubMean")
                                nc_out2 = "/Volumes/OneTouch/Calculated_Indices_FutureAnalysis/10_Temporal+Spatial/DivSub/" + "_".join(dir3.replace(replace_tag, replace_tag + "-DivSub").split("_")[2:4]) + "/" + dir3.replace(replace_tag, replace_tag + "-DivSub")
                                nc_out22 = "/Volumes/OneTouch/Calculated_Indices_FutureAnalysis/10_Temporal+Spatial/DivSubMean/"+ "_".join(dir3.replace(replace_tag, replace_tag + "-DivSubMean").split("_")[2:4]) + "/" + dir3.replace(replace_tag, replace_tag + "-DivSubMean")
                                cmd1 = "cdo sub " + nc_in + " " + reference_data + " " + nc_out1
                                cmd2 = "cdo div " + nc_out1 + " " + reference_data + " " + nc_out2
                                cmd3 = "cdo divc,3003 -fldsum " + nc_out1 + " " + nc_out11
                                cmd4 = "cdo divc,3003 -fldsum " + nc_out2 + " " + nc_out22
                                print("开始执行命令")
                                print(cmd1)
                                print(cmd2)
                                print(cmd3)
                                print(cmd4)
                                os.system(cmd1)
                                os.system(cmd2)
                                os.system(cmd3)
                                os.system(cmd4)
                                print("命令执行结束")
