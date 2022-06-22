import os

if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Calculated_Indices_FutureAnalysis/15_Txx_Tnn"
    for dir2 in os.listdir(rootpath):
        path2 = rootpath + "/" + dir2
        if os.path.isdir(path2):
            for dir3 in os.listdir(path2):
                path3 = path2 + "/" + dir3
                path4 = path2 + "/resampled_" + dir3
                if not os.path.exists(path4) and not dir3.startswith("resampled_"):
                    os.makedirs(path4)
                if os.path.isdir(path3):

                    for dir4 in os.listdir(path3):
                        if len(dir4) > 20 and dir4.endswith(".nc") and (not dir4.startswith("._")):
                            input_path = path3 + "/" + dir4
                            #dir4 = dir4.replace("gr-gr", "2041-2100").replace("gr1-gr1", "2041-2100")
                            output_path = path4 + "/" + dir4
                            if "CMIP5_" in output_path:
                                cmd1 = "cdo -remapcon2,/Users/jinzhao/Desktop/CMIP5_template.nc " + input_path + " " + output_path
                                cmd2 = "cdo -sellonlatbox,190,350,5,85 " + output_path + " " + \
                                       output_path.replace(".nc", "-processed.nc")
                                print("cmd1:   " + cmd1)
                                # print("cmd2:   " + cmd2)
                                print("+++++++++++++++++++++++++++++")
                                os.system(cmd1)
                                # os.system(cmd2)
                            if "CMIP6_" in output_path:
                                cmd1 = "cdo -remapbil,/Volumes/OneTouch/Calculated_Indices_FutureAnalysis/14_significant_test/mean/ReferenceAverage_median_1981-2010/cdd_ANN_EnsembleMedian_historical_r1i1p1f1_ReferenceAverage.nc " + input_path + " " + output_path
                                print("cmd1:   " + cmd1)
                                print("+++++++++++++++++++++++++++++")
                                os.system(cmd1)
