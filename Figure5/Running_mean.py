import netCDF4 as nc
import os
import pandas as pd

if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Resampled/csv"
    for dir2 in os.listdir(rootpath):
        if dir2.endswith(".nc") and (not dir2.startswith("._")):
            with open("/Volumes/OneTouch/Resampled/res/" + dir2.replace(".nc", ".txt"), 'w') as f:
                zhishu = dir2.split("_")[0]
                path2 = rootpath + "/" + dir2
                ncdata = nc.Dataset(path2)
                index = list(range(1981, 2101))
                data = []
                for i in range(120):
                    data.append(ncdata[zhishu][i, 0, 0])
                ser_data = pd.Series(data, index=index)
                res = ser_data.rolling(20).mean()
                for i in range(120):
                    result = str(res[index[i]])
                    if result != "nan":
                        f.writelines(str(index[i]) + "," + result)
                        f.writelines("\n")