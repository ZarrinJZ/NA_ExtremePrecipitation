# encoding:utf-8
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib as mpl
import matplotlib.colors as colors
import os
import netCDF4 as nc
import numpy as np
import geopandas as gpd


NAME_DICT = {"rx1day": "Rx1day", "r10mm": "R10mm", "r95p": "R95P", "cwd": "CWD", "prcptot": "PRCPTOT",
             "rx5day": "Rx5day", "r20mm": "R20mm", "r99p": "R99P", "cdd": "CDD", "sdii": "SDII"}

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        "trunc({n},{a:.2f},{b:.2f})".format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)),
    )
    return new_cmap

def plot(X, Y, values, lons, lats, key):
    year = key.split("#")[0]
    ssp = key.split("#")[1]
    zhishu = key.split("#")[2]
    title = ssp.upper()
    titleout = ssp.upper() + "-" + NAME_DICT[zhishu] + " (" + year + ")"
    fig, ax = plt.subplots(figsize=(20, 9),dpi=100)
    # 设置全局字体
    plt.rc('font',family='Times New Roman',size=30)
    plt.tight_layout()
    # 设置标题字体和大小
    ax.set_title(title, font={'family': 'Times New Roman', 'weight': 'normal', 'size': 30})
    cmap=plt.get_cmap('PiYG_r')
    trunc_cmap = truncate_colormap(cmap, 0.44, 1)
    ax.set_title(title, font={'family': 'Times New Roman', 'weight': 'normal', 'size': 30})
    if zhishu == "cdd":
        p = ax.contourf(X, Y, values, cmap='PiYG_r', levels=np.linspace(-5, 5, 11), extend='both')
    elif zhishu == "cwd":
        p = ax.contourf(X, Y, values, cmap='PiYG_r', levels=np.linspace(-5, 5, 11), extend='both')
    elif zhishu == "prcptot":
        p = ax.contourf(X, Y, values, cmap=trunc_cmap, levels=np.linspace(-5, 45, 11), extend='both')
    elif zhishu == "sdii":
        p = ax.contourf(X, Y, values, cmap=trunc_cmap, levels=np.linspace(-5, 45, 11), extend='both')
    elif zhishu == "r10mm":
        p = ax.contourf(X, Y, values, cmap='PiYG_r', levels=np.linspace(-5, 5, 11), extend='both')
    elif zhishu == "r20mm":
        p = ax.contourf(X, Y, values, cmap='PiYG_r', levels=np.linspace(-5, 5, 11), extend='both')
    elif zhishu == "r95p":
        p = ax.contourf(X, Y, values, cmap=trunc_cmap, levels=np.linspace(-10, 90, 11), extend='both')
    elif zhishu == "r99p":
        p = ax.contourf(X, Y, values, cmap=trunc_cmap, levels=np.linspace(-20, 180, 11), extend='both')
    elif zhishu == "rx1day":
        p = ax.contourf(X, Y, values, cmap=trunc_cmap, levels=np.linspace(-5, 45, 11), extend='both')
    elif zhishu == "rx5day":
        p = ax.contourf(X, Y, values, cmap=trunc_cmap, levels=np.linspace(-5, 45, 11), extend='both')
    # 设置colorbar

    plt.colorbar(p, format='%.1f', orientation="horizontal",  extend='both', aspect=70, fraction=0.03, pad=0.09)
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

    plt.scatter(lons, lats, color="black", s=0.2)
    plt.xticks(ticks=[-160, -140, -120, -100, -80, -60], labels=["160W", "140W", "120W", "100W", "80W", "60W"])
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%d N'))
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
        plt.ylabel(NAME_DICT[zhishu] +' (days)', font)
    else:
        plt.ylabel(NAME_DICT[zhishu] + ' (%)', font)
        # plt.ylabel('Relative Change (%)', fontdict={"size": 14})
    region_overlay = gpd.read_file("/Volumes/OneTouch/Calculated_Indices_FutureAnalysis/6_Spatial_remapbil/4_GraphDrawing_Data/4_NorthAmerica_overlay/NorthAmerica.shp")
    region_overlay.plot(ax=ax, color="none", edgecolor='black', zorder=100, alpha=0.8, linewidth=2)
    plt.tight_layout()
    plt.savefig("chapter4.3Bar_"+titleout + '.png', format='png', transparent=True, dpi=100, pad_inches=0.0)
    plt.show()


def get_snrfile_info(rootpath):
    res = {}
    for dir2 in os.listdir(rootpath):
        key1 = dir2
        path2 = rootpath + "/" + dir2
        if os.path.isdir(path2):
            for dir3 in os.listdir(path2):
                path3 = path2 + "/" + dir3
                if "_SNR_" in path3:
                    key2 = dir3.split("_")[3].lower()
                    if os.path.isdir(path3):
                        for dir4 in os.listdir(path3):
                            if dir4.endswith(".nc") and not dir4.startswith("._"):
                                key3 = dir4.split("_")[0]
                                key = "#".join([key1, key2, key3])
                                res[key] = path3 + "/" + dir4
    return res


def get_medianfile_info(rootpath):
    res = {}
    for dir2 in os.listdir(rootpath):
        key1 = dir2
        path2 = rootpath + "/" + dir2
        if os.path.isdir(path2):
            for dir3 in os.listdir(path2):
                path3 = path2 + "/" + dir3
                if "EnsembleMedian_" in path3:
                    key2 = dir3.split("_")[1]
                    if os.path.isdir(path3):
                        for dir4 in os.listdir(path3):
                            if dir4.endswith(".nc") and not dir4.startswith("._"):
                                key3 = dir4.split("_")[0]
                                key = "#".join([key1, key2, key3])
                                res[key] = path3 + "/" + dir4
    return res


if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Calculated_Indices_FutureAnalysis/6_Spatial_remapbil/4_GraphDrawing_Data/3_Year_mean"
    snrfile_info = get_snrfile_info(rootpath)
    medianfile_info = get_medianfile_info(rootpath)
    for key in snrfile_info.keys():
        zhishu = key.split("#")[2]
        if zhishu in ["rx1day", "rx5day", "r10mm", "r20mm", "r95p", "r99p", "cwd", "cdd", "prcptot", "sdii"]:
            ncdata_snr = nc.Dataset(snrfile_info[key])
            ncdata_median = nc.Dataset(medianfile_info[key])
            values = np.zeros(shape=(72, 121))
            lons = []
            lats = []
            for i in range(1):
                for j in range(72):
                    for k in range(121):
                        valuetype = str(type(ncdata_snr[zhishu][i, j, k]))
                        if zhishu in ["cdd", "cwd", "r10mm", "r20mm", "r30mm"]:
                            values[j, k] = float(ncdata_median[zhishu][i, j, k])
                        else:
                            values[j, k] = float(ncdata_median[zhishu][i, j, k]) * 100.0
                        if valuetype == "<class 'numpy.ma.core.MaskedArray'>":
                            if float(ncdata_snr[zhishu][i, j, k]) <= 1:
                                lons.append(ncdata_snr["lon"][k])
                                lats.append(ncdata_snr["lat"][j])
            plot(ncdata_median["lon"][:], ncdata_median["lat"][:], values, lons, lats, key)
