import os
from nco import Nco


# 获取nco操作所需参数
def get_nco_params(path2, path3):
    res = []
    time = []
    temp_filepath = ""
    for dir4 in os.listdir(path3):
        if len(dir4) > 20 and dir4.endswith(".nc") and (not dir4.startswith("._")):
            res.append(path3 + "/" + dir4)
            temp_filepath = dir4[0:len(dir4) - 20]
            time_0 = int(dir4[-20:-3].split("-")[0])
            time_1 = int(dir4[-20:-3].split("-")[1])
            time.append(time_0)
            time.append(time_1)
    output_path = path2 + "/" + temp_filepath + str(min(time)) + "-" + str(max(time)) + ".nc"
    res.sort()
    return res, output_path


if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Crop_CMIP6_Historical"
    for dir2 in os.listdir(rootpath):
        path2 = rootpath + "/" + dir2
        if os.path.isdir(path2):
            for dir3 in os.listdir(path2):
                path3 = path2 + "/" + dir3
                temp_filepath = ""
                if os.path.isdir(path3):
                    nco_params, output_path = get_nco_params(path2, path3)
                    print(nco_params, output_path)
                    print("++++++++++++++++++++++++++++++++++")
                    os.system("cdo cat " + " ".join(nco_params) + " " + output_path)
                    print("********************************************")
