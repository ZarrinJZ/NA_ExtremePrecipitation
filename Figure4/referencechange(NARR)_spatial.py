# encoding:utf-8
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os
import netCDF4 as nc
import numpy as np
import geopandas as gpd
import matplotlib.colors as col

NAME_DICT = {"rx1day": "Rx1day", "r10mm": "R10mm", "r95p": "R95P", "r95ptot": "R95Ptot","cwd": "CWD", "prcptot": "PRCPTOT",
             "rx5day": "Rx5day", "r20mm": "R20mm", "r99p": "R99P", "r99ptot": "R99Ptot","cdd": "CDD", "sdii": "SDII"}


def plot(X, Y, values, lons, lats, key):
    year = key.split("#")[0]
    historical = key.split("#")[1]
    print(historical)
    zhishu = key.split("#")[2]
    # if zhishu in ["cdd", "cwd", "r10mm", "r20mm", "r30mm"]:
    #     title = NAME_DICT[zhishu] + ' (days)'
    # elif zhishu in ["r95ptot", "r99ptot"]:
    #     title = NAME_DICT[zhishu] + ' (%)'
    # else:
    #     title = NAME_DICT[zhishu] + ' (mm)'
    title = r"$\bf{" + 'NARR' + "}$"
    titleout = historical.upper() + "-" + NAME_DICT[zhishu] + " (" + year + ")"
    fig, ax = plt.subplots(figsize=(10, 9),dpi=100)
    # 设置全局字体
    plt.rc('font',family='Times New Roman',size=30)
    plt.tight_layout()
    # 设置标题字体和大小
    ax.set_title(title, font={'family': 'Times New Roman', 'weight': 'normal', 'size': 30})
    color = 'Blues'
    # cpool8 = ['#FFFAF0', '#E0FFFF', '#BFEFFF', '#87CEFF', '#EEAEEE', '#DA70D6', '#8B4789', '#4B0082']
    # cmap8 = col.ListedColormap(cpool8, 'indexed')
    # cpool6 = ['#FFFAF0', '#BFEFFF', '#87CEFF', '#EEAEEE', '#DA70D6', '#8B4789']
    # cmap6 = col.ListedColormap(cpool6, 'indexed')
    # cpool5 = ['#FFFAF0', '#BFEFFF', '#87CEFF', '#EEAEEE', '#8B4789']
    # cmap5 = col.ListedColormap(cpool5, 'indexed')
    # if zhishu == "cdd":
    #     p = plt.pcolormesh(X, Y, values, cmap=cmap6, vmin=0, vmax=60)
    # elif zhishu == "cwd":
    #     p = plt.pcolormesh(X, Y, values, cmap=cmap8, vmin=0, vmax=20)
    # elif zhishu == "prcptot":
    #     p = plt.pcolormesh(X, Y, values, cmap=cmap6, vmin=0, vmax=1500)
    # elif zhishu == "sdii":
    #     p = plt.pcolormesh(X, Y, values, cmap=cmap6, vmin=0, vmax=15)
    # elif zhishu == "r10mm":
    #     p = plt.pcolormesh(X, Y, values, cmap=cmap8, vmin=0, vmax=40)
    # elif zhishu == "r20mm":
    #     p = plt.pcolormesh(X, Y, values, cmap=cmap8, vmin=0, vmax=20)
    # elif zhishu == "r95p":
    #     p = plt.pcolormesh(X, Y, values, cmap=cmap8, vmin=0, vmax=400)
    # elif zhishu == "r99p":
    #     p = plt.pcolormesh(X, Y, values, cmap=cmap5, vmin=0, vmax=100)
    # elif zhishu == "r95ptot":
    #     p = plt.pcolormesh(X, Y, values, cmap=cmap8, vmin=10, vmax=30)
    # elif zhishu == "r99ptot":
    #     p = plt.pcolormesh(X, Y, values, cmap=cmap5, vmin=0, vmax=10)
    # elif zhishu == "rx1day":
    #     p = plt.pcolormesh(X, Y, values, cmap=cmap6, vmin=0, vmax=60)
    # elif zhishu == "rx5day":
    #     p = plt.pcolormesh(X, Y, values, cmap=cmap6, vmin=0, vmax=120)

    if zhishu == "cdd":
        p = plt.pcolormesh(X, Y, values, cmap="BrBG", vmin=0, vmax=60)
    elif zhishu == "cwd":
        p = plt.pcolormesh(X, Y, values, cmap="BrBG", vmin=0, vmax=20)
    elif zhishu == "prcptot":
        p = plt.pcolormesh(X, Y, values, cmap="BrBG", vmin=0, vmax=1500)
    elif zhishu == "sdii":
        p = plt.pcolormesh(X, Y, values, cmap="BrBG", vmin=0, vmax=15)
    elif zhishu == "r10mm":
        p = plt.pcolormesh(X, Y, values, cmap="BrBG", vmin=0, vmax=40)
    elif zhishu == "r20mm":
        p = plt.pcolormesh(X, Y, values, cmap="BrBG", vmin=0, vmax=20)
    elif zhishu == "r95p":
        p = plt.pcolormesh(X, Y, values, cmap="BrBG", vmin=0, vmax=400)
    elif zhishu == "r99p":
        p = plt.pcolormesh(X, Y, values, cmap="BrBG", vmin=0, vmax=100)
    elif zhishu == "r95ptot":
        p = plt.pcolormesh(X, Y, values, cmap="BrBG", vmin=10, vmax=30)
    elif zhishu == "r99ptot":
        p = plt.pcolormesh(X, Y, values, cmap="BrBG", vmin=0, vmax=10)
    elif zhishu == "rx1day":
        p = plt.pcolormesh(X, Y, values, cmap="BrBG", vmin=0, vmax=60)
    elif zhishu == "rx5day":
        p = plt.pcolormesh(X, Y, values, cmap="BrBG", vmin=0, vmax=120)
    # 设置colorbar
    plt.colorbar(p, format='%.0f', orientation="horizontal",  extend='both', aspect=29, fraction=0.03, pad=0.09)
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 30

    plt.tick_params(top=False, bottom=True, left=True, right=False)
    plt.tick_params(which='both', direction='out')
    plt.tick_params(which="major", length=8, width=2)
    plt.tick_params(which="minor", length=3, width=0.5)

    bwith = 2  # 边框宽度设置为2
    TK = plt.gca()  # 获取边框
    TK.spines['bottom'].set_linewidth(bwith)  # 图框下边
    TK.spines['left'].set_linewidth(bwith)  # 图框左边
    TK.spines['top'].set_linewidth(bwith)  # 图框上边
    TK.spines['right'].set_linewidth(bwith)  # 图框右边

    # plt.scatter(lons, lats, color="black", s=0.2)
    plt.xticks(ticks=[-160, -140, -120, -100, -80, -60], labels=["160W", "140W", "120W", "100W", "80W", "60W"])
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%dN'))
    # colorbar字体
    # cb = plt.colorbar(mappable=im, cax=None, ax=None)
    # for l in cb.ax.yaxis.get_ticklabels():
    #     l.set_family('Times New Roman')
    # 设置坐标刻度值的大小以及刻度值的字体
    plt.tick_params(labelsize=30)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    # 设置横纵坐标名称和大小
    font = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 30
            }
    if zhishu in ["cdd", "cwd", "r10mm", "r20mm", "r30mm"]:
        plt.ylabel(r"$\bf{" + NAME_DICT[zhishu] +' (days)' + "}$", font)
    elif zhishu in ["r95ptot", "r99ptot"]:
        plt.ylabel(r"$\bf{" + NAME_DICT[zhishu] + ' (%)' + "}$", font)
        # plt.ylabel(NAME_DICT[zhishu] +' (%)', font)
    else:
        plt.ylabel(r"$\bf{" + NAME_DICT[zhishu] + ' (mm)' + "}$", font)
        # plt.ylabel(NAME_DICT[zhishu] + ' (mm)', font)
    region_overlay = gpd.read_file("/Volumes/OneTouch/Calculated_Indices_FutureAnalysis/6_Spatial_remapbil/4_GraphDrawing_Data/4_NorthAmerica_overlay/NorthAmerica.shp")
    region_overlay.plot(ax=ax, color="none", edgecolor='black', zorder=100, alpha=0.8, linewidth=2)
    plt.tight_layout()
    plt.savefig("chapter4.3_NARR_"+titleout + '.png', format='png', transparent=True, dpi=100, pad_inches=0.1, bbox_inches='tight')
    plt.show()



def get_medianfile_info(rootpath):
    res = {}
    for dir2 in os.listdir(rootpath):
        print(dir2)
        key1 = dir2
        path2 = rootpath + "/" + dir2
        if os.path.isdir(path2):
            for dir3 in os.listdir(path2):
                path3 = path2 + "/" + dir3
                print(path3)
                if "NARR_" in path3:
                    key2 = dir3.split("_")[1]
                    print(key2)
                    if os.path.isdir(path3):
                        for dir4 in os.listdir(path3):
                            if dir4.endswith(".nc") and not dir4.startswith("._"):
                                key3 = dir4.split("_")[0]
                                key = "#".join([key1, key2, key3])
                                res[key] = path3 + "/" + dir4
    return res


if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Crop_CMIP6_Historical"
    medianfile_info = get_medianfile_info(rootpath)
    for key in medianfile_info.keys():
        zhishu = key.split("#")[2]
        if zhishu in ["rx1day", "rx5day", "r10mm", "r20mm", "r95p", "r99p", "r95ptot", "r99ptot","cwd", "cdd", "prcptot", "sdii"]:
        # if zhishu in ["r95ptot", "r99ptot"]:
            ncdata_median = nc.Dataset(medianfile_info[key])
            values = np.zeros(shape=(72, 121))
            lons = []
            lats = []
            for i in range(1):
                for j in range(72):
                    for k in range(121):
                        valuetype = str(type(ncdata_median[zhishu][i, j, k]))
                        if zhishu in ["cdd", "cwd", "r10mm", "r20mm", "r30mm"]:
                            values[j, k] = float(ncdata_median[zhishu][i, j, k])
                        else:
                            values[j, k] = float(ncdata_median[zhishu][i, j, k])
                        if valuetype == "<class 'numpy.ma.core.MaskedArray'>":
                            if float(ncdata_median[zhishu][i, j, k]) > 1:
                                lons.append(ncdata_median["lon"][k])
                                lats.append(ncdata_median["lat"][j])
            plot(ncdata_median["lon"][:], ncdata_median["lat"][:], values, lons, lats, key)
