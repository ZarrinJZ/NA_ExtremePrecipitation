# -- coding:utf-8 --
import matplotlib.pyplot as plt
import os
import netCDF4 as nc
import numpy as np
from collections import defaultdict
import matplotlib.ticker as mticker
from matplotlib.ticker import MultipleLocator

NAME_DICT = {"rx1day": "Rx1day", "r10mm": "R10mm", "r95p": "R95P", "cwd": "CWD", "prcptot": "PRCPTOT",
             "rx5day": "Rx5day", "r20mm": "R20mm", "r99p": "R99P", "cdd": "CDD", "sdii": "SDII"}


def get_file_info(rootpath):
    res = defaultdict(list)
    for dir2 in os.listdir(rootpath):
        key1 = dir2
        path2 = rootpath + "/" + dir2
        if os.path.isdir(path2):
            for dir3 in os.listdir(path2):
                path3 = path2 + "/" + dir3
                if os.path.isdir(path3):
                    for dir4 in os.listdir(path3):
                        if dir4.endswith(".nc") and not dir4.startswith("._"):
                            key3 = dir4.split("_")[0]
                            key4 = dir4.split("_")[2]
                            key = "#".join([key1, key3])
                            res[key].append(key4 + "#" + path3 + "/" + dir4)
    return res


def get_float(zhishu, file_path):
    data = []
    ncdata_median = nc.Dataset(file_path)
    for i in range(72):
        if not np.isnan(float(ncdata_median[zhishu][0, i, 0])):
            if zhishu.lower() in ["cdd", "cwd", "r10mm", "r20mm", "r30mm"]:
                data.append(float(ncdata_median[zhishu][0, i, 0]))
            else:
                data.append(float(ncdata_median[zhishu][0, i, 0]) * 100)
    return data


def get_drwa_data(zhishu, infos):
    data_126 = []
    data_126_25 = []
    data_126_75 = []
    data_245 = []
    data_245_25 = []
    data_245_75 = []
    data_585 = []
    data_585_25 = []
    data_585_75 = []
    for info in infos:
        tag = info.split("#")[0]
        file_path = info.split("#")[1]
        if "ssp126" in file_path:
            if "25" in tag:
                data_126_25 = get_float(zhishu, file_path)
            elif "75" in tag:
                data_126_75 = get_float(zhishu, file_path)
            else:
                data_126 = get_float(zhishu, file_path)
        if "ssp245" in file_path:
            if "25" in tag:
                data_245_25 = get_float(zhishu, file_path)
            elif "75" in tag:
                data_245_75 = get_float(zhishu, file_path)
            else:
                data_245 = get_float(zhishu, file_path)
        if "ssp585" in file_path:
            if "25" in tag:
                data_585_25 = get_float(zhishu, file_path)
            elif "75" in tag:
                data_585_75 = get_float(zhishu, file_path)
            else:
                data_585 = get_float(zhishu, file_path)
    return data_126, data_126_25, data_126_75, data_245, data_245_25, data_245_75, data_585, data_585_25, data_585_75


def plot(key, data_126, data_126_25, data_126_75, data_245, data_245_25, data_245_75, data_585, data_585_25, data_585_75, y_zhou):
    plt.figure(figsize=(10, 9), dpi=100)
    # 设置全局字体
    plt.rc('font', family='Times New Roman', size=30)
    plt.tight_layout()
    plt.tick_params(top=False, bottom=True, left=True, right=False)
    plt.tick_params(which='both', direction='out')
    plt.tick_params(which="major", length=8, width=2)
    plt.tick_params(which="minor", length=3, width=0.5)

    # if zhishu.lower() in ["prcptot", "sdii"]:
    #     plt.xlim((-27, 145))
    # if zhishu.lower() in ["rx1day", "rx5day"]:
    #     plt.xlim((-12, 78))
    # if zhishu.lower() in ["r95p", "r99p"]:
    #     plt.xlim((-50, 900))
    # if zhishu.lower() in ["r10mm", "r20mm"]:
    #     plt.xlim((-14, 9))
    # if zhishu.lower() in ["cdd", "cwd"]:
    #      plt.xlim((-24, 18))
    if zhishu.lower() in ["prcptot", "sdii"]:
        plt.xlim((-27, 145))
    if zhishu.lower() in ["rx1day", "rx5day"]:
        plt.xlim((-27, 145))
    if zhishu.lower() in ["r95p"]:
        plt.xlim((-50, 400))
    if zhishu.lower() in ["r99p"]:
        plt.xlim((-50, 900))
    if zhishu.lower() in ["r10mm", "r20mm"]:
        plt.xlim((-24, 18))
    if zhishu.lower() in ["cdd", "cwd"]:
         plt.xlim((-24, 18))
    bwith = 2  # 边框宽度设置为2
    TK = plt.gca()  # 获取边框
    TK.spines['bottom'].set_linewidth(bwith)  # 图框下边
    TK.spines['left'].set_linewidth(bwith)  # 图框左边
    TK.spines['top'].set_linewidth(bwith)  # 图框上边
    TK.spines['right'].set_linewidth(bwith)  # 图框右边

    ax = plt.gca()
    ax.yaxis.set_ticks_position('right')

    # title = key.split("#")[1].upper() + "(" + key.split("#")[0] + ")"

    title = NAME_DICT[zhishu] + " (" + key.split("#")[0] + ")"
    # plt.title(key.split("#")[1].upper() + "(" + key.split("#")[0] + ")")
    # 设置标题字体和大小
    ax.set_title(title, font={'family': 'Times New Roman', 'weight': 'normal', 'size': 30})
    plt.plot(data_126, y_zhou, color="mediumseagreen", label='SSP126', zorder=100, linewidth=3.0)
    plt.plot(data_126_25, y_zhou, alpha=0)
    plt.plot(data_126_75, y_zhou, alpha=0)
    plt.fill_betweenx(y_zhou, data_126_25, data_126_75, facecolor='mediumseagreen', alpha=0.2, zorder=50)
    plt.plot(data_245, y_zhou, color="orange", label='SSP245', zorder=100, linewidth=3.0)
    plt.plot(data_245_25, y_zhou, alpha=0)
    plt.plot(data_245_75, y_zhou, alpha=0)
    plt.fill_betweenx(y_zhou, data_245_25, data_245_75, facecolor='orange', alpha=0.2, zorder=50)
    plt.plot(data_585, y_zhou, color="deeppink", label='SSP585', zorder=100, linewidth=3)
    plt.plot(data_585_25, y_zhou, alpha=0)
    plt.plot(data_585_75, y_zhou, alpha=0)
    plt.fill_betweenx(y_zhou, data_585_25, data_585_75, facecolor='deeppink', alpha=0.2, zorder=50)
    plt.legend(loc="best", ncol=1, frameon=False, prop={'size': 30, "family": "Times New Roman"})
    ax.yaxis.set_major_locator(MultipleLocator(10))
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%d N'))
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 30
    plt.tick_params(labelsize=30)
    ax.axvline(x=0, color='grey', ls="--", lw=2, alpha=1)
    plt.savefig("chapter4.4_" + title + '.png', format='png', transparent=True, dpi=100, pad_inches=0.0)
    plt.show()


if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Calculated_Indices_FutureAnalysis/6_Spatial_remapbil/4_GraphDrawing_Data/5_zonmean_ready"
    file_info = get_file_info(rootpath)
    y_zhou = list(np.linspace(15.5, 82.5, 68))
    for key in file_info.keys():
        zhishu = key.split("#")[1]
        if zhishu in ["rx1day", "rx5day", "r10mm", "r20mm", "r95p", "r99p", "cwd", "cdd", "prcptot", "sdii"]:
            data_126, data_126_25, data_126_75, data_245, data_245_25, data_245_75, data_585, data_585_25, data_585_75 = get_drwa_data(zhishu, file_info[key])
            plot(key, data_126, data_126_25, data_126_75, data_245, data_245_25, data_245_75, data_585, data_585_25, data_585_75, y_zhou)
