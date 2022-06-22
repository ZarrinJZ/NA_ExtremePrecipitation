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
                            output_path = path2 + "/" + dir4.replace("_MON_", "_JJA_")
                            print("********"+path4)
                            # cmd1 = "cdo selmon,1,2,12 " + input_path + " " + output_path
                            if "prcptot_" in dir4 or "r10mm_" in dir4 or "r20mm_" in dir4 or "r30mm_" in dir4:
                                cmd1 = "cdo timselsum,3,5,9 " + input_path + " " + output_path
                                print("cmd1:   " + cmd1)
                                os.system(cmd1)
                            else:
                                cmd2 = "cdo timselmax,3,5,9 " + input_path + " " + output_path
                                print("cmd2:   " + cmd2)
                                os.system(cmd2)
                            print("+++++++++++++++++++++++++++++")

