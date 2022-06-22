import os

if __name__ == '__main__':
    rootpath = "/Users/jinzhao/Desktop/NARR_1981-2020/NARR_1981-2010"
    for dir2 in os.listdir(rootpath):
        path2 = rootpath + "/" + dir2
        print(path2)
        if os.path.isdir(path2):
            for dir3 in os.listdir(path2):
                path3 = path2 + "/" + dir3
                print(path3)
                if os.path.isdir(path3):
                    for dir4 in os.listdir(path3):
                        print(dir4)
                        if dir4.startswith("acpcp") and dir4.endswith(".nc") and (not dir4.startswith("._")):
                            nc_in = path3 + "/" + dir4
                            nc_out = path3 + "/processed_" + dir4
                            cmd = "cdo -remapbil,global_0.3 " + nc_in + " " + nc_out
                            print("当前执行命令为： "+cmd)
                            print("开始执行命令")
                            os.system(cmd)
                            print("命令执行结束")

