# -- coding:utf-8 --
import os
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
from PIL import Image

NAME_DICT = {"rx1day": "Rx1day", "r10mm": "R10mm", "r95p": "R95P", "cwd": "CWD", "prcptot": "PRCPTOT",
             "rx5day": "Rx5day", "r20mm": "R20mm", "r99p": "R99P", "cdd": "CDD", "sdii": "SDII", "rx7day": "Rx7day",
             "r30mm": "R30mm", "r99ptot": "R99pTOT", "r95ptot": "R95pTOT", "EnsembleMedian": "CMIP-EnM"}


def get_areas(path):
    res = []
    for dir1 in os.listdir(path):
        if not dir1.startswith("."):
            path1 = path + "/" + dir1
            for dir2 in os.listdir(path1):
                if not dir2.startswith("."):
                    path2 = path1 + "/" + dir2
                    if os.path.isdir(path2):
                        for dir3 in os.listdir(path2):
                            if not dir3.startswith("."):
                                res.append(dir3)
    return list(set(res))


def get_zhishus(path):
    res = []
    for dir1 in os.listdir(path):
        if not dir1.startswith("."):
            path1 = path + "/" + dir1
            for dir2 in os.listdir(path1):
                if not dir2.startswith("."):
                    path2 = path1 + "/" + dir2
                    if os.path.isdir(path2):
                        for dir3 in os.listdir(path2):
                            if not dir3.startswith("."):
                                path3 = path2 + "/" + dir3
                                if os.path.isdir(path3):
                                    for dir4 in os.listdir(path3):
                                        if not dir4.startswith("."):
                                            path4 = path3 + "/" + dir4
                                            if os.path.isdir(path4):
                                                for dir5 in os.listdir(path4):
                                                    if dir5.endswith(".nc") and (not dir5.startswith(".")):
                                                        res.append(dir5.split("_")[1])
    return list(set(res))


def get_file_info(path):
    res = defaultdict(list)
    for dir1 in os.listdir(path):
        if not dir1.startswith("."):
            path1 = path + "/" + dir1
            key4 = dir1
            for dir2 in os.listdir(path1):
                if not dir2.startswith("."):
                    path2 = path1 + "/" + dir2
                    if os.path.isdir(path2):
                        for dir3 in os.listdir(path2):
                            if not dir3.startswith("."):
                                path3 = path2 + "/" + dir3
                                key3 = dir3
                                if os.path.isdir(path3):
                                    for dir4 in os.listdir(path3):
                                        if not dir4.startswith("."):
                                            path4 = path3 + "/" + dir4
                                            key2 = dir4.split("_")[2]
                                            if os.path.isdir(path4):
                                                for dir5 in os.listdir(path4):
                                                    if dir5.endswith(".nc") and (not dir5.startswith(".")):
                                                        key1 = dir5.split("_")[1]
                                                        key = key4 + "#" + key1 + "#" + key2 + "#" + key3
                                                        res[key].append(path4 + "/" + dir5)
    return res


def get_value(path):
    try:
        zhishu = path.split("/")[-1].split("_")[1]
        ncdata = nc.Dataset(path)
        if zhishu in ["cdd", "cwd", "r10mm", "r20mm", "r30mm"]:
            value = ncdata[zhishu][0][0][0]
        else:
            value = ncdata[zhishu][0][0][0] * 100
        return value
    except:
        print(path)


def get_png_info(rootpath):
    res = {}
    zhishus = []
    for dir1 in os.listdir(rootpath):
        if not dir1.startswith("A-") and dir1.endswith(".png"):
            path1 = rootpath + "/" + dir1
            key = dir1.split("_")[1].split(".")[0]
            res[key] = path1
            zhishus.append(dir1.split("_")[1].split("-")[1])
    return res, list(set(zhishus))


def he(path_126, path_245, path_585, outpath):
    img1, img2, img3 = Image.open(path_126), Image.open(path_245), Image.open(path_585)
    joint = Image.new('RGBA', (3200, 2000))
    joint.paste(img1, (-80, 0), mask=img1.split()[3])
    joint.paste(img2, (0, 0), mask=img2.split()[3])
    joint.paste(img3, (80, 0), mask=img3.split()[3])
    joint.save(outpath, format="png", quality=95)
    # joint.show()


if __name__ == '__main__':
    rootpath = "D:/zj/03.05"
    model_path = "D:/zj/03.05/Model_agreement/18models/ann"
    mean_path = "D:/zj/03.05/Model_agreement/CMIP6_EnM/ann"
    zhishus = get_zhishus(model_path)
    years = ["2041-2070", "2071-2100"]
    ssps = ["ssp126", "ssp245", "ssp585"]
    model_info = get_file_info(model_path)
    mean_info = get_file_info(mean_path)
    for zhishu in zhishus:
        for year in years:
            for ssp in ssps:
                plt.rc('font', family='Times New Roman', size=30)
                plt.figure(figsize=(16, 10), dpi=100)
                plt.title(NAME_DICT[zhishu], font={'family': 'Times New Roman', 'weight': 'bold', 'size': 32})
                temp_key = year + "#" + zhishu + "#" + ssp
                draw_data_zhifang = {}
                draw_data_temp_scatter = []
                for key in model_info.keys():
                    if key.startswith(temp_key):
                        for path in model_info[key]:
                            value = get_value(path)
                            area = key.split("#")[3].split("_")[1]
                            moxing = path.split("/")[-1].split("_")[3]
                            temp1 = pd.DataFrame({'values': [value], 'moxing': [moxing], 'area': [area], 'size': 1})
                            draw_data_temp_scatter.append(temp1)
                        for path in mean_info[key]:
                            value = get_value(path)
                            area = key.split("#")[3].split("_")[1]
                            draw_data_zhifang[area] = value
                draw_data_scatter = pd.concat(draw_data_temp_scatter)
                draw_data_scatter["area"] = draw_data_scatter["area"].astype("category")
                draw_data_scatter['area'] = draw_data_scatter['area'].cat.reorder_categories(["GIC", "NWN", "NEN", "WNA", "CNA", "ENA", "NCA", "SCA"])
                values = []
                for area in ["GIC", "NWN", "NEN", "WNA", "CNA", "ENA", "NCA", "SCA"]:
                    values.append(draw_data_zhifang[area])
                if ssp == "ssp126":
                    zhifang_tu = plt.bar(x=["GIC", "NWN", "NEN", "WNA", "CNA", "ENA", "NCA", "SCA"], width=0.25, height=values, facecolor="limegreen", linewidth=1.5)
                if ssp == "ssp245":
                    zhifang_tu = plt.bar(x=["GIC", "NWN", "NEN", "WNA", "CNA", "ENA", "NCA", "SCA"], width=0.25, height=values, facecolor="blue",  linewidth=1.5)
                if ssp == "ssp585":
                    zhifang_tu = plt.bar(x=["GIC", "NWN", "NEN", "WNA", "CNA", "ENA", "NCA", "SCA"], width=0.25, height=values, facecolor="red", linewidth=1.5)
                markers = {
                    "ACCESS-CM2": "o",
                    "ACCESS-ESM1-5": "v",
                    "BCC-CSM2-MR": "H",
                    "EC-Earth3": "*",
                    "FGOALS-g3": "p",
                    "GFDL-ESM4": "P",
                    "INM-CM4-8": ">",
                    "INM-CM5-0": "D",
                    "IPSL-CM6A-LR": "s",
                    "KACE-1-0-G": "o",
                    "MIROC6": "v",
                    "MPI-ESM1-2-HR": "H",
                    "MPI-ESM1-2-LR": "*",
                    "MRI-ESM2-0": "p",
                    "NESM3": "P",
                    "NorESM2-LM": ">",
                    "NorESM2-MM": "D",
                    "TaiESM1": "s"
                }

                hue_order = ["ACCESS-CM2",
                             "ACCESS-ESM1-5",
                             "BCC-CSM2-MR",
                             "EC-Earth3",
                             "FGOALS-g3",
                             "GFDL-ESM4",
                             "INM-CM4-8",
                             "INM-CM5-0",
                             "IPSL-CM6A-LR",
                             "KACE-1-0-G",
                             "MIROC6",
                             "MPI-ESM1-2-HR",
                             "MPI-ESM1-2-LR",
                             "MRI-ESM2-0",
                             "NESM3",
                             "NorESM2-LM",
                             "NorESM2-MM",
                             "TaiESM1"]
                palette = {
                    "ACCESS-CM2": "hotpink",
                    "ACCESS-ESM1-5": "violet",
                    "BCC-CSM2-MR": "mediumslateblue",
                    "EC-Earth3": "cornflowerblue",
                    "FGOALS-g3": "lightskyblue",
                    "GFDL-ESM4": "cyan",
                    "INM-CM4-8": "mediumseagreen",
                    "INM-CM5-0": "orange",
                    "IPSL-CM6A-LR": "dimgrey",
                    "KACE-1-0-G": "none",
                    "MIROC6": "none",
                    "MPI-ESM1-2-HR": "none",
                    "MPI-ESM1-2-LR": "none",
                    "MRI-ESM2-0": "none",
                    "NESM3": "none",
                    "NorESM2-LM": "none",
                    "NorESM2-MM": "none",
                    "TaiESM1": "none"
                }
                fc = {
                    "ACCESS-CM2": "hotpink",
                    "ACCESS-ESM1-5": "violet",
                    "BCC-CSM2-MR": "mediumslateblue",
                    "EC-Earth3": "cornflowerblue",
                    "FGOALS-g3": "lightskyblue",
                    "GFDL-ESM4": "cyan",
                    "INM-CM4-8": "mediumseagreen",
                    "INM-CM5-0": "orange",
                    "IPSL-CM6A-LR": "dimgrey",
                    "KACE-1-0-G": "none",
                    "MIROC6": "none",
                    "MPI-ESM1-2-HR": "none",
                    "MPI-ESM1-2-LR": "none",
                    "MRI-ESM2-0": "none",
                    "NESM3": "none",
                    "NorESM2-LM": "none",
                    "NorESM2-MM": "none",
                    "TaiESM1": "none"
                }
                ec = {
                    "ACCESS-CM2": "hotpink",
                    "ACCESS-ESM1-5": "violet",
                    "BCC-CSM2-MR": "mediumslateblue",
                    "EC-Earth3": "cornflowerblue",
                    "FGOALS-g3": "lightskyblue",
                    "GFDL-ESM4": "cyan",
                    "INM-CM4-8": "mediumseagreen",
                    "INM-CM5-0": "orange",
                    "IPSL-CM6A-LR": "dimgrey",
                    "KACE-1-0-G": "hotpink",
                    "MIROC6": "violet",
                    "MPI-ESM1-2-HR": "mediumslateblue",
                    "MPI-ESM1-2-LR": "cornflowerblue",
                    "MRI-ESM2-0": "lightskyblue",
                    "NESM3": "cyan",
                    "NorESM2-LM": "mediumseagreen",
                    "NorESM2-MM": "orange",
                    "TaiESM1": "dimgrey"
                }
                scatter = sns.scatterplot(x="area", y="values", data=draw_data_scatter, hue="moxing", style="moxing", style_order=hue_order, linewidth=1.5, s=100, markers=markers,
                                          hue_order=hue_order, zorder=100, palette=palette, legend=None,
                                          ec=['hotpink', 'violet', 'mediumslateblue', 'cornflowerblue', 'lightskyblue', 'cyan', 'mediumseagreen', 'orange', 'dimgrey',
                                              'hotpink', 'violet', 'mediumslateblue', 'cornflowerblue', 'lightskyblue', 'cyan', 'mediumseagreen', 'orange', 'dimgrey'])
                plt.tick_params(axis='x', which='minor', bottom=False)
                plt.tick_params(which="major", length=8)
                locs, labels = plt.xticks()
                plt.setp(labels, rotation=45)
                bwith = 2  # 边框宽度设置为2
                TK = plt.gca()  # 获取边框
                TK.spines['bottom'].set_linewidth(bwith)  # 图框下边
                TK.spines['left'].set_linewidth(bwith)  # 图框左边
                TK.spines['top'].set_linewidth(bwith)  # 图框上边
                TK.spines['right'].set_linewidth(bwith)  # 图框右边
                font = {'family': 'Times New Roman',
                        'weight': 'bold',
                        'size': 32
                        }
                if zhishu == "rx1day":
                    plt.ylim((-32, 105))
                if zhishu == "rx5day":
                    plt.ylim((-40, 120))
                if zhishu == "r10mm":
                    plt.ylim((-18, 10))
                if zhishu == "r20mm":
                    plt.ylim((-10, 6))
                if zhishu == "prcptot":
                    plt.ylim((-50, 210))
                if zhishu == "cdd":
                    plt.ylim((-33, 28))
                if zhishu == "cwd":
                    plt.ylim((-39, 7))
                if zhishu == "r95p":
                    plt.ylim((-80, 690))
                if zhishu == "r99p":
                    plt.ylim((-100, 1430))
                if zhishu == "sdii":
                    plt.ylim((-19, 42))
                if zhishu == "r30mm":
                    plt.ylim((-4, 3))
                if zhishu == "rx7day":
                    plt.ylim((-20, 60))
                if zhishu == "r95ptot":
                    plt.ylim((-30, 90))
                if zhishu == "r99ptot":
                    plt.ylim((-50, 200))
                if zhishu in ["cdd", "cwd", "r10mm", "r20mm", "r30mm"]:
                    plt.ylabel("Relative Change (days)", font)
                else:
                    plt.ylabel("Relative Change (%)" + ' (%)', font)
                plt.xlabel("")
                if ssp in ["ssp126", "ssp585"]:
                    bwith = 0  # 边框宽度设置为2
                    TK = plt.gca()  # 获取边框
                    TK.spines['bottom'].set_linewidth(bwith)  # 图框下边
                    TK.spines['left'].set_linewidth(bwith)  # 图框左边
                    TK.spines['top'].set_linewidth(bwith)  # 图框上边
                    TK.spines['right'].set_linewidth(bwith)  # 图框右边
                    plt.xticks([])
                    plt.yticks([])
                    plt.ylabel("")
                    plt.title("")
                else:
                    plt.axhline(y=0, color='grey', lw=2, alpha=1, linestyle='--')
                plt.savefig("chapter4.7_" + ssp + "-" + NAME_DICT[zhishu] + "-" + year + '.png', format='png', transparent=True, dpi=200,
                            pad_inches=0.1, bbox_inches=None)
                # plt.show()
    res, zhishus_he = get_png_info(rootpath)
    outpath = ""
    for zhishu in zhishus_he:
        for year in years:
            outpath = "A-" + zhishu + "-" + year + ".png"
            path_126 = res["ssp126-" + zhishu + "-" + year]
            path_245 = res["ssp245-" + zhishu + "-" + year]
            path_585 = res["ssp585-" + zhishu + "-" + year]
            he(path_126, path_245, path_585, outpath)
