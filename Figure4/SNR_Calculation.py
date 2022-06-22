import os
from collections import defaultdict

def get_EnsembleMedian_info(rootpath):
    res = defaultdict(list)
    for dir2 in os.listdir(rootpath):
        if dir2.endswith("_EnsembleMedian"):
            path2 = rootpath + "/" + dir2
            if os.path.isdir(path2):
                for dir3 in os.listdir(path2):
                    if dir3.endswith(".nc") and (not dir3.startswith("._")):
                        path3 = path2 + "/" + dir3
                        key = dir2.split("_")[3] + "-" + dir3.split("_")[0]
                        res[key].append(path3)
    return res


def get_Median_Individal_info(rootpath):
    res = defaultdict(list)
    for dir2 in os.listdir(rootpath):
        if dir2.endswith("_Median-Individal"):
            path2 = rootpath + "/" + dir2
            key = dir2.split("_")[3]
            res[key].append(path2)
    return res


def get_Median_Individal_tag(rootpath):
    res = defaultdict(list)
    for dir2 in os.listdir(rootpath):
        if dir2.endswith("_Median-Individal"):
            path2 = rootpath + "/" + dir2
            key = dir2.split("_")[3] + "#" + path2
            if os.path.isdir(path2):
                temp = []
                for dir3 in os.listdir(path2):
                    temp.append(dir3)
                res[key] = list(set(temp))
    return res


if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Calculated_Indices_FutureAnalysis/1_RMSE_Evaluation/SNR_Calculation"
    EnsembleMedian_res = get_EnsembleMedian_info(rootpath)
    for dir2 in os.listdir(rootpath):
        if dir2.endswith("_1981-2010"):
            path2 = rootpath + "/" + dir2
            if os.path.isdir(path2):
                print("开始执行命令1")
                for dir3 in os.listdir(path2):
                    if dir3.endswith(".nc") and (not dir3.startswith("._")):
                        key = dir2.split("_")[3] + "-" + dir3.split("_")[0]
                        ensemble_nc = EnsembleMedian_res[key][0]
                        nc_in1 = path2 + "/" + dir3
                        nc_out1 = get_Median_Individal_info(rootpath)[dir2.split("_")[3]][0] + "/" + dir3.replace(
                            dir3.split("_")[2], dir3.split("_")[2] + "-Median-Individal")
                        cmd1 = "cdo -sqr -sub " + ensemble_nc + " " + nc_in1 + " " + nc_out1
                        print(cmd1)
                        os.system(cmd1)
                print("命令1执行结束")
    Median_Individal_tag = get_Median_Individal_tag(rootpath)
    for key in Median_Individal_tag.keys():
        for value in Median_Individal_tag[key]:
            nc_in2 = key.split("#")[1] + "/" + value.split("_")[0] + "_ANN*.nc"
            nc_out2 = key.split("#")[1].replace("Median-Individal", "Noise") + "/" + value.replace(value.split("_")[2],
                                                                                                   "Noise")
            cmd2 = "cdo sqrt -ensmean " + nc_in2 + " " + nc_out2
            print("开始执行命令2")
            print(cmd2)
            os.system(cmd2)
            print("命令2执行结束")
            print("开始执行命令3")
            cmd3key = key.split("#")[0] + "-" + value.split("_")[0]
            nc_in3left = EnsembleMedian_res[cmd3key][0]
            nc_in3right = nc_out2
            nc_out3 = key.split("#")[1].replace("Median-Individal", "SNR") + "/" + value.replace(value.split("_")[2], "SNR")
            cmd3 = "cdo abs -div " + nc_in3left + " " + nc_in3right + " " + nc_out3
            print(cmd3)
            os.system(cmd3)
            print("命令3执行结束")
