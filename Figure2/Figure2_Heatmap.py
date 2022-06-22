# encoding:utf-8
import netCDF4 as nc
import os
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib import ticker


def generate_txt(rootpath, outpath):
    f = open(outpath, 'w', newline='')
    for dir2 in os.listdir(rootpath):
        if dir2.endswith(".nc") and (not dir2.startswith("._")):
            path2 = rootpath + "/" + dir2
            ncdata = nc.Dataset(path2)
            if "CMIP6-EnM" in dir2:
                zhishu = dir2.split("_")[1]
                moxing = dir2.split("_")[2].replace(".nc", "")
            else:
                zhishu = dir2.split("_")[1]
                moxing = dir2.split("_")[3]
            value = str(float(ncdata[zhishu][:][0][0][0]))
            f.writelines(zhishu + "," + moxing + "," + value)
            f.writelines("\n")


def transfer2map(x_zhou, filepath):
    dictb = calc_mean(x_zhou, filepath)
    dicta = {}
    with open(filepath) as f:
        lines = f.readlines()
        for line in lines:
            if line:
                new_line = line.strip()
                dicta["#".join(new_line.split(",")[0:2])] = float(new_line.split(",")[2])
    dicta.update(dictb)
    return dicta


def calc_mean(x_zhou, filepath):
    dicta = defaultdict(list)
    dictb = {}
    with open(filepath) as f:
        lines = f.readlines()
        for line in lines:
            if line:
                new_line = line.strip()
                dicta[new_line.split(",")[1]].append(float(new_line.split(",")[2]))
    for x in x_zhou:
        dictb["rmseall#" + x] = sum(dicta[x]) / len(dicta[x])
        print(x , dictb["rmseall#" + x])
    return dictb


def draw(rawdata, rawdata2, x_zhou, y_zhou):
    a = []
    for y in y_zhou:
        b = []
        for x in x_zhou:
            key = y.lower() + "#" + x
            # 小数点保留1位
            b.append(round(rawdata[key], 3))
        a.append(b)
    harvest = np.array(a)

    a1 = []
    for y in y_zhou:
        b1 = []
        for x in x_zhou:
            key = y.lower() + "#" + x
            # 小数点保留1位
            b1.append(round(rawdata2[key], 3))
        a1.append(b1)
    harvest1 = np.array(a1)
    # 这里是创建一个画布

    fig, (ax, ax1) = plt.subplots(dpi=150, figsize=(15, 6.4), nrows=1, ncols=2)
    # 设置全局字体
    plt.rc('font', family='Times New Roman', size=14)
    # im = ax.imshow(harvest, cmap="RdBu_r", vmin=-0.5, vmax=0.5)
    im = ax.imshow(harvest, cmap="RdBu_r", vmin=-0.5, vmax=0.5)
    # 修改标签
    ax.set_title("Relative RMSE (Daymet)", font='Times New Roman', fontsize=16)
    ax.set_xticks(np.arange(len(x_zhou)))
    ax.set_yticks(np.arange(len(y_zhou)))
    ax.set_xticklabels(x_zhou, font='Times New Roman', fontsize=14)
    ax.set_yticklabels(y_zhou, font='Times New Roman', fontsize=14)
    ax.tick_params(top=False, bottom=True, left=True, right=False)
    ax.tick_params(which='both', direction='out')
    ax.tick_params(which="major", length=4, width=0.7)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    # cb = plt.colorbar(mappable=im, shrink=1,
    #                   orientation='horizontal',
    #                   aspect=23, fraction=0.02, pad=0.02,
    #                   extend='both', ax=ax)
    # cb.set_ticks(np.arange(-0.5, 0.6, 0.1))
    # cb.ax.tick_params(labelsize=5)

    im1 = ax1.imshow(harvest1, cmap='RdBu_r', vmin=-0.5, vmax=0.5)
    ax1.set_title("Relative RMSE (NARR)", font='Times New Roman', fontsize=16)
    ax1.set_xticks(np.arange(len(x_zhou)))
    ax1.set_yticks(np.arange(len(y_zhou)))
    ax1.set_xticklabels(x_zhou, font='Times New Roman', fontsize=14)
    ax1.set_yticklabels(y_zhou, font='Times New Roman', fontsize=14)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    plt.subplots_adjust(bottom=0.3, wspace=0.1, hspace=0.3)
    plt.tight_layout()
    plt.tick_params(top=False, bottom=True, left=True, right=False)
    plt.tick_params(which='both', direction='out')
    plt.tick_params(which="major", length=5, width=1)
    # cb1 = plt.colorbar(mappable=im1, shrink=1,
    #                    orientation='horizontal',
    #                    aspect=23, fraction=0.02, pad=0.02,
    #                    extend='both', ax=ax1)
    # cb1.set_ticks(np.arange(-0.5, 0.6, 0.1))
    # cb1.ax.tick_params(labelsize=5)
    l = 0.27
    b = 0.07
    w = 0.5
    h = 0.03
    # 对应 l,b,w,h；设置colorbar位置；
    rect = [l, b, w, h]
    cbar_ax = fig.add_axes(rect)
    cb = plt.colorbar(im1, cax=cbar_ax, extend='both', orientation='horizontal')
    # 设置colorbar标签字体等
    cb.ax.tick_params(labelsize=14)  # 设置色标刻度字体大小。
    font = {'family': 'Times New Roman',
            #       'color'  : 'darkred',
            'color': 'black',
            'weight': 'normal',
            'size': 14,
            }
    cb.set_ticks(np.arange(-0.5, 0.6, 0.1))
    # tick_locator = ticker.MaxNLocator(nbins=9)
    # cb.locator = tick_locator
    # cb.update_ticks()
    plt.savefig('chapter4.1_Portrait diagram of reltive RMSEs (daymet&NARR).png', format='png', transparent=True, dpi=150,
                pad_inches=0.0)
    plt.show()


if __name__ == '__main__':
    x_zhou = ["ACCESS-CM2", "ACCESS-ESM1-5", "BCC-CSM2-MR", "EC-Earth3", "FGOALS-g3", "GFDL-ESM4", "INM-CM4-8",
              "INM-CM5-0", "IPSL-CM6A-LR", "KACE-1-0-G", "MIROC6", "MPI-ESM1-2-HR", "MPI-ESM1-2-LR", "MRI-ESM2-0",
              "NESM3", "NorESM2-LM", "NorESM2-MM", "TaiESM1", "CMIP6-EnM"]

    # y_zhou = ["cdd", "cwd", "prcptot", "r10mm", "r20mm", "r30mm", "r95p", "r95ptot", "r99p", "r99ptot", "rx1day",
    #           "rx5day", "rx7day", "sdii"]
    y_zhou = ["RMSEall", "CDD", "CWD", "PRCPTOT", "R10mm", "R20mm", "R95p", "R99p", "RX1day", "RX5day", "SDII"]

    # outpath = "8_NARR-CMIP6_RMSE_YearAverage_draw.txt"
    outpath1 = "8_daymet-CMIP6_RMSE_YearAverage_draw.txt"
    rawdata1 = transfer2map(x_zhou, outpath1)

    outpath2 = "8_NARR-CMIP6_RMSE_YearAverage_draw.txt"
    rawdata2 = transfer2map(x_zhou, outpath2)

    draw(rawdata1, rawdata2, x_zhou, y_zhou)
