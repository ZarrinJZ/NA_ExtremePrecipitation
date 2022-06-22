import os


def get_observed_datapath(rootpath):
    res = []
    for dir2 in os.listdir(rootpath):
        path2 = rootpath + "/" + dir2
        if os.path.isdir(path2):
            for dir3 in os.listdir(path2):
                if "NARR" in dir3:
                    path3 = path2 + "/" + dir3
                    if os.path.isdir(path3):
                        for dir4 in os.listdir(path3):
                            if dir4.endswith("ANN_NARR_observed_r1i1p1f1_1981-2010.nc") and (not dir4.startswith("._")):
                                res.append(path3 + "/" + dir4)
    return res


if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Resampled"
    observed_datapath = get_observed_datapath(rootpath)
    for observed_data in observed_datapath:
        tag = "_".join(observed_data.split("/")[-1].split("_")[0:2])
        #print(tag)
        for dir2 in os.listdir(rootpath):
            path2 = rootpath + "/" + dir2
            if os.path.isdir(path2):
                for dir3 in os.listdir(path2):
                    if "NARR" not in dir3:
                        path3 = path2 + "/" + dir3
                        if os.path.isdir(path3):
                            for dir4 in os.listdir(path3):
                                if dir4.startswith(tag) and dir4.endswith(".nc") and (not dir4.startswith("._")):
                                    nc_in = path3 + "/" + dir4
                                    nc_out = path3 + "/" + "RMSE30_" + dir4
                                    #cmd = "cdo -sqrt -sqr -sub " + observed_data + " " + nc_in + " " + nc_out
                                    #cmd = "cdo -sqrt -fldmean  -sqr -sub " + observed_data + " " + nc_in + " " + nc_out
                                    cmd = "cdo -sqrt -divc,3003 -fldsum -sqr -sub " + observed_data + " " + nc_in + " " + nc_out
                                    print("当前执行命令为： " + cmd)
                                    print("开始执行命令")
                                    os.system(cmd)
                                    print("命令执行结束")
