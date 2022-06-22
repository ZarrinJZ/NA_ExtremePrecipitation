# encoding:utf-8
import netCDF4 as nc
import os

def generate_txt(rootpath, outpath):
    f = open(outpath, 'w', newline='')
    for dir2 in os.listdir(rootpath):
        if dir2.endswith(".nc") and (not dir2.startswith("._")):
            path2 = rootpath + "/" + dir2
            ncdata = nc.Dataset(path2)
            #if "output50" in dir2:
            if "RESE30_Mean" in dir2:
                Indices = dir2.split("_")[1]
                Models = dir2.split("_")[2].replace(".nc", "")
                print(Indices)
            else:
                Indices = dir2.split("_")[1]
                Models = dir2.split("_")[3]
            value = str(float(ncdata[Indices][:][0][0][0]))
            #f.writelines(Indices + "," + Models + "," + value)
            #f.writelines("\n")


if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Resampled/NA_ReadyToAnalysis/8_daymet-CMIP6_RMSE_YearAverage"
    #rootpath = "/Volumes/OneTouch/Resampled/NA_ReadyToAnalysis/6_RMES_NAMean_NARR-Simulation"
    outpath = rootpath + "/A_rmes_result.txt"
    generate_txt(rootpath, outpath)
