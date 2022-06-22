import os

if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Calculated_Indices_FutureAnalysis/15_Txx_Tnn"
    for dir2 in os.listdir(rootpath):
        path2 = rootpath + "/" + dir2
        if os.path.isdir(path2):
            for dir3 in os.listdir(path2):
                path3 = path2 + "/" + dir3
                path4 = path2 + "/" + dir3
                if os.path.isdir(path3):
                    for dir4 in os.listdir(path3):
                        if len(dir4) > 20 and dir4.endswith(".nc") and (not dir4.startswith("._")):
                            dir4 = dir4.replace("NA_", "")
                            input_path = path3 + "/" + "NA_"+ dir4
                            output_path = path4 + "/" + dir4
                            cmd1 = "cdo invertlat " + input_path + " " + output_path
                            print("cmd1:   " + cmd1)
                            # if "CMIP5_" in output_path:
                            #     cmd2 = "cdo -sellonlatbox,lonmin,lonmax,latmin,latmax " + output_path + " " + output_path
                            #     print("cmd2:   " + cmd2)
                            print("+++++++++++++++++++++++++++++")
                            os.system(cmd1)
                            # os.system(cmd2)