# -- coding:utf-8 --
import os
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import seaborn as sns

NAME_DICT = {"rx1day": "Rx1day", "r10mm": "R10mm", "r95p": "R95P", "cwd": "CWD", "prcptot": "PRCPTOT",
             "rx5day": "Rx5day", "r20mm": "R20mm", "r99p": "R99P", "cdd": "CDD", "sdii": "SDII",
             "rx7day": "Rx7day", "r30mm": "R30mm", "r95ptot": "R95Ptot", "r99ptot": "R99Ptot"}


def get_file_info(rootpath):
    models = []
    zhishus = []
    res = {}
    for dir2 in os.listdir(rootpath):
        if not dir2.startswith("."):
            print(dir2)
            key1 = dir2.split("_")[1]
            models.append(key1)
            key2 = dir2.split("_")[2]
            path2 = rootpath + "/" + dir2
            if os.path.isdir(path2):
                for dir3 in os.listdir(path2):
                    if dir3.endswith(".nc") and not dir3.startswith("._"):
                        key3 = dir3.split("_")[0]
                        zhishus.append(key3)
                        path3 = path2 + "/" + dir3
                        res[key1 + "#" + key2 + "#" + key3] = path3
    zhishus = list(set(zhishus))
    models = list(set(models))
    return models, zhishus, res


def get_data(path, zhishu):
    res = []
    data = nc.Dataset(path)
    for i in range(1):
        for j in range(72):
            for k in range(121):
                if not np.isnan(float(data[zhishu][i, j, k])):
                    if zhishu in ["cdd", "cwd", "r10mm", "r20mm", "r30mm"]:
                        res.append(float(data[zhishu][i, j, k]))
                    else:
                        res.append(float(data[zhishu][i, j, k]) * 100)

    return res



def huatu(model, zhishu, data1, data2):
    plt.rc('font', family ='Times New Roman', size=28)
    fig, ax = plt.subplots(figsize=(12, 4), dpi=100)
    # 设置全局字体
    # 设置标题字体和大小
    if zhishu in ["cdd", "cwd", "r10mm", "r20mm", "r30mm"]:
        title = NAME_DICT[zhishu]
    else:
        title = NAME_DICT[zhishu]
    ax.set_title(title, font={'family': 'Times New Roman', 'weight': 'bold', 'size': 30})
    bwith = 2  # 边框宽度设置为2
    TK = plt.gca()  # 获取边框
    TK.spines['bottom'].set_linewidth(bwith)  # 图框下边
    TK.spines['left'].set_linewidth(bwith)  # 图框左边
    TK.spines['top'].set_linewidth(bwith)  # 图框上边
    TK.spines['right'].set_linewidth(bwith)  # 图框右边

    plt.minorticks_on()
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 28
    plt.tick_params(top=False, bottom=True, left=True, right=False)
    plt.tick_params(which='both', direction='out')

    plt.tick_params(which="major", length=8, width=2)
    plt.tick_params(which="minor", length=4, width=1)

    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 28
    plt.tick_params(labelsize=28)
    # 设置横纵坐标名称和大小
    kwargs = dict()
    if zhishu == "rx1day":
        plt.xlim(-40, 120)

        plt.ylim(-0.011, 0.11)
    if zhishu == "rx5day":
        plt.xlim(-40, 120)

        plt.ylim(-0.011, 0.11)
        # y_ticks = np.linspace(-20, 80, 11)  # 产生区间在-5至4间的10个均匀数值
    if zhishu == "rx7day":
        plt.xlim(-40, 120)

        plt.ylim(-0.011, 0.11)
    if zhishu == "cdd":
        plt.xlim(-26, 26)

        plt.ylim(-0.031, 0.31)
    if zhishu == "cwd":
        plt.xlim(-26, 26)

        plt.ylim(-0.14, 1.4)
    if zhishu == "r10mm":
        plt.xlim(-26, 26)

        plt.ylim(-0.048, 0.48)
    if zhishu == "r20mm":
        plt.xlim(-26, 26)

        plt.ylim(-0.12, 1.2)
    if zhishu == "r30mm":
        plt.xlim(-26, 26)

        plt.ylim(-0.21, 2.1)
    if zhishu == "r95p":
        plt.xlim((-50, 320))

        plt.ylim(-0.0033, 0.033)
    if zhishu == "r95ptot":
        plt.xlim((-20, 120))

        plt.ylim(-0.006, 0.06)
    if zhishu == "r99p":
        plt.xlim((-100, 1100))

        plt.ylim(-0.0018, 0.018)
    if zhishu == "r99ptot":
        plt.xlim((-100, 600))

        plt.ylim(-0.0026, 0.026)
    if zhishu == "prcptot":
        plt.xlim((-40, 130))

        plt.ylim(-0.0074, 0.074)
    if zhishu == "sdii":
        plt.xlim(-40, 120)

        plt.ylim(-0.023, 0.23)
    plt.ylabel("Density", font={'family': 'Times New Roman', 'weight': 'bold', 'size': 30})
    # legend_elements = [Patch(facecolor="paleturquoise", edgecolor="darkturquoise",
    #                          label='2041-2070', linewidth=2),
    #                    Patch(facecolor="lightpink", edgecolor="deeppink",
    #                          label='2071-2100', linewidth=2),
    #                    Line2D([0], [0], color='darkturquoise', lw=2.5, label="Mean=" + str(round(np.mean(data1), 2))),
    #                    Line2D([0], [0], color='deeppink', lw=2.5, label="Mean=" + str(round(np.mean(data2), 2)))
    #                    ]
    legend_elements = [Line2D([0], [0], color='darkturquoise', lw=2.5, label="Mean=" + str(round(np.mean(data1), 2))),
                       Line2D([0], [0], color='deeppink', lw=2.5, label="Mean=" + str(round(np.mean(data2), 2)))
                       ]
    # drawing Hist
    weights1 = np.ones_like(data1) / len(data1)
    weights = np.ones_like(data2) / len(data2)
    # plt.hist(data1, **kwargs, density=True, zorder=50, label="2041-2070", color="paleturquoise", edgecolor="darkturquoise", linewidth=2)
    sns.kdeplot(data1, linewidth=2, zorder=100, shade=True, color="darkturquoise", alpha=0.2)
    # plt.hist(data2, **kwargs, density=True, zorder=50, label="2071-2100", color="lightpink", edgecolor="deeppink", linewidth=2)
    sns.kdeplot(data2,  linewidth=2, zorder=90, shade=True, color="deeppink", alpha=0.2)
    ax.text(0.02, 0.8, model.upper(), transform=ax.transAxes, fontdict={'size': '26', 'color': 'black', 'weight': 'bold'})
    # plt.axvline(np.mean(data1), zorder=100, color="darkturquoise", linewidth=2, label='{:5.0f}'.format(np.mean(data1)))
    # plt.axvline(np.mean(data2), zorder=100, color="deeppink", linewidth=2, label='{:5.0f}'.format(np.mean(data2)))
    plt.scatter(np.mean(data1), 0, s=50, color="darkturquoise", zorder=100, marker="x")
    plt.scatter(np.mean(data2), 0, s=50, color="deeppink", zorder=100, marker="x")
    # plt.axvline(x=0, color='grey', ls="--", lw=2, alpha=1)

    # plt.legend(loc="best", frameon=False, handles=legend_elements)
    # plt.axis('off')  # 关闭坐标轴

    plt.savefig("chapter4.6_" + model.upper() + "_" + title.replace("\n", "_") + '.png', format='png', transparent=True, dpi=100,
                pad_inches=0.0)
    plt.show()


if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Calculated_Indices_FutureAnalysis/13_Histogram"
    models, zhishus, res = get_file_info(rootpath)
    for model in models:
        for zhishu in zhishus:
            # if zhishu in ["cdd"]:
            data1 = get_data(res[model + "#2041-2070#" + zhishu], zhishu)
            data2 = get_data(res[model + "#2071-2100#" + zhishu], zhishu)
            huatu(model, zhishu, data1, data2)
