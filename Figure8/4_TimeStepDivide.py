import os

if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Resampled"
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
                            output_path1 = path4 + "/" + dir4.replace(".nc", "-29Year.nc")

                            cmd1 = "cdo seltimestep,1/29 " + input_path + " " + output_path1

                            print("cmd1:   " + cmd1)

                            print("+++++++++++++++++++++++++++++")
                            os.system(cmd1)
