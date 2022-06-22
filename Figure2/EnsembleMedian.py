import os


def getzhishu(path3):
    zhishu = []
    for dir4 in os.listdir(path3):
        if dir4.endswith(".nc") and (not dir4.startswith("._")):
            zhishu.append(dir4.split("_")[0])
    return list(set(zhishu))


def gethouzhui(zhishu, dir4):
    if dir4.startswith(zhishu):
        return "_".join(dir4.split("_")[3:])


def get_mean(lastpath, zhishu, dir4):
    for y in zhishu:
        houzhui = gethouzhui(y, dir4)
        output1 = lastpath + "/processed/" + y + "_output50.nc"
        output2 = lastpath + "/processed/" + y + "_output53.nc"
        output3 = lastpath + "/processed/" + y + "_MON_EnsembleMedian_" + houzhui
        output4 = lastpath + "/processed/" + y + "_MON_25_" + houzhui
        output5 = lastpath + "/processed/" + y + "_MON_75_" + houzhui
        cmd1 = "cdo enspctl,50 " + lastpath + "/" + y + "_MON" + "_*.nc " + output1
        cmd2 = "cdo enspctl,53 " + lastpath + "/" + y + "_MON" + "_*.nc " + output2
        cmd3 = "cdo ensavg " + output1 + " " + output2 + " " + output3
        cmd4 = "cdo enspctl,25 " + lastpath + "/" + y + "_MON" + "_*.nc " + output4
        cmd5 = "cdo enspctl,75 " + lastpath + "/" + y + "_MON" + "_*.nc " + output5
        print("++++++++++++++开始执行+++++++++++++")
        print(cmd1)
        print(cmd2)
        print(cmd3)
        print(cmd4)
        print(cmd5)
        # os.system(cmd1)
        # os.system(cmd2)
        # os.system(cmd3)
        # os.system(cmd4)
        # os.system(cmd5)
        print("++++++++++++++结束执行++++++++++++++")


if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Resampled"
    for dir2 in os.listdir(rootpath):
        path2 = rootpath + "/" + dir2
        if os.path.isdir(path2):
            for dir3 in os.listdir(path2):
                path3 = path2 + "/" + dir3
                if os.path.isdir(path3):
                    zhishu = getzhishu(path3)
                    for dir4 in os.listdir(path3):
                        if dir4.endswith(".nc") and (not dir4.startswith("._")):
                            filepath = path3 + "/" + dir4
                            get_mean(filepath, zhishu, dir4)
