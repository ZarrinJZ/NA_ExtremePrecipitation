
import os

if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Calculated_Indices_FutureAnalysis/15_Txx_Tnn"
    for dir2 in os.listdir(rootpath):
        path2 = rootpath + "/" + dir2
        if os.path.isdir(path2):
            for dir3 in os.listdir(path2):
                path3 = path2 + "/" + dir3
                if os.path.isdir(path3):
                    for dir4 in os.listdir(path3):
                        if len(dir4) > 20 and dir4.endswith(".nc") and (not dir4.startswith("._")):
                            temp_filepath = path3 + "/" + dir4
                            new_temp_filepath = path2 + "/" + dir4.replace("crop_", "")
                            cmd1 = "ncks -C -O -x -v crs " + temp_filepath + " " + new_temp_filepath
                            #cmd2 = "ncatted -O -a bounds,,d,, " + new_temp_filepath
                            print(cmd1)
                            #print(cmd2)
                            print("+++++++++++++++++++++++++++++")
                            os.system(cmd1)
                            #os.system(cmd2)
