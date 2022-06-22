import os
from cdo import *

# 获取cdo操作所需参数
def get_cdo_params(rootpath, secpath, filename, begintime, endtime):
    cdo_input = secpath + "/"+filename
    cdo_out_path = rootpath + "/"
    dateparams = ""
    if len(filename) > 20 and filename.endswith(".nc") and (not filename.startswith("._")):
        temp_filepath = dir4[0:len(filename) - 20]
        time_0 = int(filename[-20:-3].split("-")[0])
        time_1 = int(filename[-20:-3].split("-")[1])
        # Satiation1: 1950-1970
        if begintime <= time_0 <= endtime <= time_1:
            cdo_out_path += temp_filepath + str(time_0) + "-" + str(endtime) + ".nc"
            dateparams = str(time_0) + "," + str(endtime)
        # Satiation2: 1950-2000
        elif begintime <= time_0 and endtime >= time_1:
            cdo_out_path += temp_filepath + str(time_0) + "-" + str(time_1) + ".nc"
            dateparams = str(time_0) + "," + str(time_1)
        # Satiation3: 1970-1980
        elif begintime >= time_0 and endtime <= time_1:
            cdo_out_path += temp_filepath + str(begintime) + "-" + str(endtime) + ".nc"
            dateparams = str(begintime) + "," + str(endtime)
        # Satiation4: 1970-2000
        elif begintime >= time_0 and endtime >= time_1:
            cdo_out_path += temp_filepath + str(begintime) + "-" + str(time_1) + ".nc"
            dateparams = str(begintime) + "," + str(time_1)
    return cdo_input, cdo_out_path, dateparams


if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Crop_CMIP6_Historical"
    date1 = int("20110101")
    date2 = int("20141231")
    for dir2 in os.listdir(rootpath):
        path2 = rootpath + "/" + dir2
        if os.path.isdir(path2):
            for dir3 in os.listdir(path2):
                path3 = path2 + "/" + dir3
                temp_filepath = ""
                if os.path.isdir(path3):
                    for dir4 in os.listdir(path3):
                        if len(dir4) > 20 and dir4.endswith(".nc") and (not dir4.startswith("._")):
                            cdo_input, cdo_out_path, dateparams = get_cdo_params(path2, path3, dir4, 20110101, 20141231)
                            # cdo 相关操作写在这里
                            print("input="+cdo_input, "output="+cdo_out_path, "date="+dateparams)
                            cdo = Cdo()
                            cdo.debug = True
                            bbox_str = '190,350,5,85'
                            # crop time dimension to range:
                            cdo.seldate(dateparams, input=cdo_input, output=cdo_out_path, options='-f nc')
                            # crop to target bbox
                            cdo.sellonlatbox(bbox_str, input=cdo_input, output=cdo_out_path, options='-f nc')
                            # chaining multiple operations:
                            cdo.seldate(dateparams, input=' -sellonlatbox,' + bbox_str + ' ' + cdo_input,
                                        output=cdo_out_path, options='-f nc')
                            # cdo.seldate(date1+','+date2, input = in_file, output = out_file, options =  '-f nc')
                            print ("Zarrin_end")