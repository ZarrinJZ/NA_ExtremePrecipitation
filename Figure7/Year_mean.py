import os

if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Calculated_Indices_FutureAnalysis/14_significant_test/2041-2100"
    for dir2 in os.listdir(rootpath):
        path2 = rootpath + "/" + dir2
        if os.path.isdir(path2):
            for dir3 in os.listdir(path2):
                path3 = path2 + "/" + dir3
                path4 = path2 + "/" + dir3
                if os.path.isdir(path3):
                    for dir4 in os.listdir(path3):
                        if len(dir4) > 20 and dir4.endswith(".nc") and (not dir4.startswith("._")):
                            input_path = path3 + "/" + dir4
                            # output_path = path4 + "/" + "Crop_" + dir4
                            output_path1 = path4 + "/" + dir4.replace("2071-2100.nc", "2071-2100-mean.nc")

                            # output_path2 = path4 + "/" + dir4.replace("2071-2100.nc", "2071-2100-zonmean.nc")

                            cmd1 = "cdo timmean " + input_path + " " + output_path1
                            # cmd2 = "cdo zonmean " + output_path1 + " " + output_path2

                            print("cmd1:   " + cmd1)
                            # print("cmd2:   " + cmd2)
                            print("+++++++++++++++++++++++++++++")
                            os.system(cmd1)
                            # os.system(cmd2)
