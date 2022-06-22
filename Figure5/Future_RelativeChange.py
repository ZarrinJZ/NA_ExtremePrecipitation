import os
from collections import defaultdict


def get_reference_datapath(rootpath):
    res = defaultdict(list)
    for dir2 in os.listdir(rootpath):
        if "Reference" in dir2 and not dir2.startswith("."):
            key = "_".join(dir2.split("_")[0:3])
            path2 = rootpath + "/" + dir2
            if os.path.isdir(path2):
                for dir3 in os.listdir(path2):
                    if dir3.endswith(".nc") and (not dir3.startswith("._")):
                        res[key].append(path2 + "/" + dir3)
    return res


if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Resampled"
    reference = get_reference_datapath(rootpath)
    replace_tag = ""
    for key in reference.keys():
        for reference_data in reference[key]:
            tag = "_".join(reference_data.split("/")[-1].split("_")[0:3])
            for dir2 in os.listdir(rootpath):
                if "Reference" not in dir2 and dir2.startswith(key):
                    replace_tag = dir2.split("_")[-2]
                    path2 = rootpath + "/" + dir2
                    if os.path.isdir(path2):
                        for dir3 in os.listdir(path2):
                            if dir3.startswith(tag) and dir3.endswith(".nc") and (not dir3.startswith("._")):
                                nc_in = path2 + "/" + dir3
                                nc_out1 = "/Volumes/OneTouch/REsult/Sub/" + dir2 + "/" + dir3.replace(replace_tag, replace_tag + "-Sub")
                                nc_out11 = "/Volumes/OneTouch/REsult/SubMean/" + dir2 + "/" + dir3.replace(replace_tag, replace_tag + "-SubMean")
                                nc_out2 = "/Volumes/OneTouch/REsult/DivSub/" + dir2 + "/" + dir3.replace(replace_tag, replace_tag + "-DivSub")
                                nc_out22 = "/Volumes/OneTouch/REsult/DivSubMean/" + dir2 + "/" + dir3.replace(replace_tag, replace_tag + "-DivSubMean")
                                cmd1 = "cdo sub " + nc_in + " " + reference_data + " " + nc_out1
                                cmd2 = "cdo div " + nc_out1 + " " + reference_data + " " + nc_out2
                                cmd3 = "cdo divc,3003 -fldsum " + nc_out1 + " " + nc_out11
                                cmd4 = "cdo divc,3003 -fldsum " + nc_out2 + " " + nc_out22
                                print("开始执行命令")
                                print(cmd1)
                                print(cmd2)
                                print(cmd3)
                                print(cmd4)
                                # os.system(cmd1)
                                # os.system(cmd2)
                                # os.system(cmd3)
                                # os.system(cmd4)
                                print("命令执行结束")