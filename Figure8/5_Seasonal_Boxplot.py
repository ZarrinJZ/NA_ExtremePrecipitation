import os
from collections import defaultdict
import pandas as pd
import netCDF4 as nc
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import colorsys
from matplotlib.ticker import MultipleLocator

NAME_DICT = {"rx1day": "Rx1day", "r10mm": "R10mm", "r95p": "R95P", "cwd": "CWD", "prcptot": "PRCPTOT",
             "rx5day": "Rx5day", "r20mm": "R20mm", "r99p": "R99P", "cdd": "CDD", "sdii": "SDII", "rx7day": "Rx7day",
             "r30mm": "R30mm", "r99ptot": "R99pTOT", "r95ptot": "R95pTOT"}


def get_zhishus(rootpath):
    res = []
    for dir2 in os.listdir(rootpath):
        if not dir2.startswith("."):
            path2 = rootpath + "/" + dir2
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


def get_file_info(rootpath):
    res = defaultdict(list)
    for dir2 in os.listdir(rootpath):
        if not dir2.startswith("."):
            path2 = rootpath + "/" + dir2
            key4 = dir2
            if os.path.isdir(path2):
                for dir3 in os.listdir(path2):
                    if not dir3.startswith("."):
                        path3 = path2 + "/" + dir3
                        key3 = dir3
                        if os.path.isdir(path3):
                            for dir4 in os.listdir(path3):
                                if not dir4.startswith("."):
                                    print(dir4)
                                    path4 = path3 + "/" + dir4
                                    key2 = dir4.split("_")[2]
                                    if os.path.isdir(path4):
                                        for dir5 in os.listdir(path4):
                                            if dir5.endswith(".nc") and (not dir5.startswith(".")):
                                                key1 = dir5.split("_")[1]
                                                key = key4 + "#" + key1 + "#" + key2 + "#" + key3
                                                res[key].append(path4 + "/" + dir5)
    return res


def get_values(paths):
    try:
        res = []
        zhishu = paths[0].split("/")[-1].split("_")[1]
        for path in paths:
            ncdata = nc.Dataset(path)
            if zhishu in ["cdd", "cwd", "r10mm", "r20mm", "r30mm"]:
                value = ncdata[zhishu][0][0][0]
            else:
                value = ncdata[zhishu][0][0][0] * 100
            res.append(value)
        return np.array(res)
    except:
        print(paths)


if __name__ == '__main__':
    rootpath = "/Volumes/OneTouch/Calculated_Indices_FutureAnalysis/12_Boxplot_Ready/18models/seasonal/2071-2100"
    enm_path = "/Volumes/OneTouch/Calculated_Indices_FutureAnalysis/12_Boxplot_Ready/CMIP6_EnM/seasonal/2071-2100"
    zhishus = get_zhishus(rootpath)
    file_info = get_file_info(rootpath)
    enm_info = get_file_info(enm_path)
    for dir2 in os.listdir(rootpath):
        if not dir2.startswith("."):
            for zhishu in zhishus:
                draw_data_temp = []
                draw_data_temp_enm = []
                for key in file_info.keys():
                    if (dir2 + "#") in key and (zhishu + "#") in key:
                        values = get_values(file_info[key])
                        values_enm = get_values(enm_info[key])
                        ssp = key.split("#")[2]
                        area = key.split("#")[3].split("_")[1]
                        temp = pd.DataFrame({'values': values, 'ssp': ssp, 'area': area})
                        temp_enm = pd.DataFrame({'values': values_enm, 'ssp': ssp, 'area': area})
                        draw_data_temp.append(temp)
                        draw_data_temp_enm.append(temp_enm)
                draw_data = pd.concat(draw_data_temp)
                draw_data_enm = pd.concat(draw_data_temp_enm)
                # First, we'll pick some nicer colors for the healthy and disease.
                # I got these colors by tweaking some colors from the Set1 palette
                # in powerpoint, and then grabbing the hex code from Powerpoint.
                # light1 = 'lightgreen'
                # light2 = 'lightskyblue'
                # light3 = 'lightsalmon'

                light1 = 'lightgreen'
                light2 = 'lightskyblue'
                light3 = 'lightsalmon'

                pal = {"ssp126": light1, "ssp245": light2, "ssp585": light3}

                dark1 = 'green'
                dark2 = 'blue'
                dark3 = 'red'

                # Here, we set up some properties for the boxplot parts. I definitely
                # stole this from Stack Overflow, but I can't find the original post
                # right now.
                boxprops = {'edgecolor': 'k', 'linewidth': 2}
                lineprops = {'color': 'k', 'linewidth': 2}
                boxprops_enm = {'edgecolor': 'k', 'linewidth': 0}
                lineprops_enm = {'color': 'k', 'linewidth': 0}
                # The boxplot kwargs get passed to matplotlib's boxplot function.
                # Note how we can re-use our lineprops dict to make sure all the lines
                # match. You could also edit each line type (e.g. whiskers, caps, etc)
                # separately.
                hue_order = ['ssp126', 'ssp245', 'ssp585']
                boxplot_kwargs = {'boxprops': boxprops, 'medianprops': lineprops,
                                  'capprops': lineprops,
                                  'width': 0.75,
                                  'palette': pal,
                                  'hue_order': hue_order}
                boxplot_kwargs_enm = {'boxprops': boxprops_enm, 'medianprops': lineprops_enm,
                                      'capprops': lineprops_enm,
                                      'width': 0.75,
                                      'palette': pal,
                                      'hue_order': hue_order}
                # When you start digging into the parameters, it's a good idea to explicitly
                # initialize the figure and get the figure and axes handles

                # plt.rcParams['ytick.right'] = plt.rcParams['ytick.labelright'] = True
                # 设置全局字体
                plt.rc('font', family='Times New Roman', size=30)
                # plt.minorticks_on()

                fig, ax = plt.subplots(figsize=(9, 12), dpi=100)
                ax.tick_params(axis='x', which='minor', bottom=False)
                # 设置标题字体和大小
                if dir2 == 'summer':
                    title = NAME_DICT[zhishu] + " (" + rootpath.split("/")[-1] + ")" + "\n" + "JJA"
                elif dir2 == 'winter':
                    title = NAME_DICT[zhishu] + " (" + rootpath.split("/")[-1] + ")" + "\n" + "DJF"
                else:
                    title = NAME_DICT[zhishu] + " (" + rootpath.split("/")[-1] + ")" + "\n" + "ANN"

                if dir2 == 'summer':
                    title1 = "JJA"
                elif dir2 == 'winter':
                    title1 = "DJF"
                else:
                    title1 = "ANN"  + " (" + rootpath.split("/")[-1] + ")"
                ax.set_title(NAME_DICT[zhishu]+' ('+ title1 +')', font={'family': 'Times New Roman', 'weight': 'bold', 'size': 32})

                # And we can plot just like last time
                sns.boxplot(x="area", y="values", data=draw_data, hue="ssp",
                            whis=1000, saturation=1,
                            whiskerprops={'linestyle': '--', 'linewidth': 2},
                            fliersize=0, **boxplot_kwargs,
                            order=["GIC", "NWN", "NEN", "WNA", "CNA", "ENA", "NCA", "SCA"]
                            )
                plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
                handles, labels = ax.get_legend_handles_labels()
                temp_label = []
                for label in labels:
                    temp_label.append(label.upper())
                for i, artist in enumerate(ax.artists):
                    if i % 3 == 0:
                        col = dark1
                    elif i % 3 == 1:
                        col = dark2
                    else:
                        col = dark3
                    # This sets the color for the main box
                    artist.set_edgecolor(col)
                    # Each box has 6 associated Line2D objects (to make the whiskers, fliers, etc.)
                    # Loop over them here, and use the same colour as above
                    for j in range(i * 6, i * 6 + 6):
                        line = ax.lines[j]
                        line.set_color(col)
                        line.set_mfc(col)
                        line.set_mec(col)
                ax = sns.boxplot(x="area", y="values", data=draw_data_enm, hue="ssp",
                                 # whis=0, saturation=1,
                                 # whiskerprops={'linestyle': '--', 'linewidth': 1},
                                 # fliersize=0,
                                 **boxplot_kwargs_enm,
                                 order=["GIC", "NWN", "NEN", "WNA", "CNA", "ENA", "NCA", "SCA"],
                                 showmeans=True,
                                 meanprops = {"marker": "s",
                                              "markerfacecolor": 'white',
                                              "markeredgecolor": 'black',
                                              "markersize":4}
                                 )

                legend_elements = [Patch(facecolor=light1, edgecolor=dark1,
                                         label='SSP126', linewidth=2),
                                   Patch(facecolor=light2, edgecolor=dark2,
                                         label='SSP245', linewidth=2),
                                   Patch(facecolor=light3, edgecolor=dark3,
                                         label='SSP585', linewidth=2)
                                   # Line2D([0], [0], marker='o', color='w', label='CMIP6-EnM',
                                   #        markerfacecolor='w',markeredgecolor='b', markersize=10),
                                   ]
                bwith = 2  # 边框宽度设置为2
                TK = plt.gca()  # 获取边框
                TK.spines['bottom'].set_linewidth(bwith)  # 图框下边
                TK.spines['left'].set_linewidth(bwith)  # 图框左边
                TK.spines['top'].set_linewidth(bwith)  # 图框上边
                TK.spines['right'].set_linewidth(bwith)  # 图框右边

                # plt.minorticks_on()
                plt.tick_params(top=False, bottom=True, left=True, right=False)
                plt.tick_params(which='both', direction='out')
                plt.tick_params(which="major", length=10, width=2)
                plt.tick_params(which="minor", length=5, width=1.5)

                plt.axhline(y=0, color='grey', lw=2, alpha=0.8, linestyle='-')
                plt.legend(loc="best", frameon=False, handles = legend_elements)
                plt.tight_layout()
                font = {'family': 'Times New Roman',
                        'weight': 'bold',
                        'size': 32
                        }
                if zhishu == "rx1day":
                     plt.ylim((-52, 165))
                if zhishu == "rx5day":
                     plt.ylim((-55, 215))
                     # y_ticks = np.linspace(-20, 80, 11)  # 产生区间在-5至4间的10个均匀数值
                if zhishu == "r10mm":
                     plt.ylim((-18.5, 4))
                if zhishu == "r20mm":
                     plt.ylim((-10, 6))
                if zhishu == "prcptot":
                    plt.ylim((-70, 480))
                if zhishu == "cdd":
                     plt.ylim((-33, 28))
                     # y_ticks = np.linspace(-20, 80, 11)  # 产生区间在-5至4间的10个均匀数值
                if zhishu == "cwd":
                    plt.ylim((-39, 7))
                    # y_ticks = np.linspace(-20, 80, 11)  # 产生区间在-5至4间的10个均匀数值
                if zhishu == "r95p":
                     plt.ylim((-80, 690))
                if zhishu == "r99p":
                     plt.ylim((-100, 1430))
                     # y_ticks = np.linspace(-20, 80, 11)  # 产生区间在-5至4间的10个均匀数值
                if zhishu == "sdii":
                     plt.ylim((-19, 42))
                if zhishu in ["cdd", "cwd", "r10mm", "r20mm", "r30mm"]:
                    plt.ylabel("Relative Change" + ' (days)', font)
                    # plt.ylabel('Relative Change (days)', font)
                    plt.xlabel("")
                else:
                    plt.ylabel("Relative Change" + ' (%)', font)
                    # plt.ylabel('Relative Change (%)', font)
                    plt.xlabel("")

                # if zhishu in ["cdd", "cwd", "r10mm", "r20mm", "r30mm"]:
                #     plt.ylabel(r"$\bf{" + NAME_DICT[zhishu] + ' (days)' + "}$", font)
                #     plt.xlabel("")
                # elif zhishu in ["prcptot", "sdii", "rx1day", "rx1day", "r95p", "r99p","r95ptot","r99ptot"]:
                #     plt.ylabel(r"$\bf{" + NAME_DICT[zhishu] + ' (%)' + "}$", font)
                #     plt.xlabel("")

                plt.savefig("chapter4.4_" + title.replace("\n", "_") + '.png', format='png', transparent=True, dpi=200,
                            pad_inches=0.1, bbox_inches='tight')
                plt.tight_layout()
                plt.show()
