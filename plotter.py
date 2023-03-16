import locale
import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

locale.setlocale(locale.LC_ALL, "el_GR.utf8")


def get_station_name(file):
    base_name = os.path.basename(file)[:-4]
    time_range, station_name = base_name.split("_")
    return station_name


def yaxis_color_aqi(ax):
    ymin, ymax = ax.get_ylim()
    ax.margins(y=0)
    ax.axhspan(0, 10, color="#43dbff")
    ax.axhspan(10, 20, color="#96cd4f")
    ax.axhspan(20, 25, color="#ffff00")
    ax.axhspan(25, 50, color="#fc3903")
    ax.axhspan(50, ymax, color="#990100")


def format_date(df, ax):
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    if df.index[-1] - df.index[0] <= pd.Timedelta(days=1):
        fmt_date = mdates.DayLocator()
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        sec_xaxis = ax.secondary_xaxis(-0.08)
        sec_xaxis.xaxis.set_major_locator(fmt_date)
        sec_xaxis.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
        sec_xaxis.spines["bottom"].set_visible(False)
        sec_xaxis.tick_params(bottom=False)


def add_logos(ax, img_path="lapup_aether_logo.png"):
    pic = plt.imread(img_path)
    ax.imshow(pic)
    ax.axis("off")


def pm_to_aqi_color(pm_value):
    if type(pm_value) is str:
        return "#43dbff"
    if pm_value < 10:
        return "#43dbff"
    elif pm_value >= 10 and pm_value < 20:
        return "#96cd4f"
    elif pm_value >= 20 and pm_value < 25:
        return "#ffff00"
    elif pm_value >= 25 and pm_value < 50:
        return "#fc3903"
    elif pm_value >= 50:
        return "#990100"


def add_last_value(df, ax, station_name=""):
    last_dt = df.notna()[::-1].idxmax()
    last_pm_measurement = df.loc[last_dt]
    try:
        last_pm_value = int(last_pm_measurement["pm2.5"])
    except ValueError as e:
        last_pm_value = "No Data"
    last_dt_fmt = last_dt["pm2.5"].strftime("%d %b %H:%M")
    ax.set_facecolor(pm_to_aqi_color(last_pm_value))
    center_text = f"{last_pm_value} $\mu g/m^3$"
    ax.text(
        0.5,
        0.5,
        center_text,
        fontsize=28,
        weight="bold",
        ha="center",
        va="center",
    )
    ax.text(
        0.5,
        0.9,
        last_dt_fmt,
        fontsize=12,
        weight="bold",
        ha="center",
        va="center",
    )
    for axis in ["top", "bottom", "left", "right"]:
        ax.spines[axis].set_linewidth(2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(
        0.5,
        0.1,
        station_name,
        fontsize=12,
        weight="bold",
        ha="center",
        va="center",
    )


def plot_all(df_7d, df_24h, station_name="station_a"):
    fig, axes = plt.subplots(
        2, 2, figsize=(10, 7), gridspec_kw={"width_ratios": [1, 2]}
    )
    ax_top_left = axes[0][0]
    ax_top_right = axes[0][1]
    ax_lower_left = axes[1][0]
    ax_lower_right = axes[1][1]

    if df_7d.count().values[0] == 0:
        print("ALL NAN")
    print("-------")
    print(df_24h.count())
    ax_top_right.plot(df_7d.index, df_7d["pm2.5"], color="black")
    ax_lower_right.plot(df_24h.index, df_24h["pm2.5"], color="black")
    # yaxis_color_aqi(ax_top_right)
    # yaxis_color_aqi(ax_lower_right)
    # format_date(df_7d, ax_top_right)
    # format_date(df_24h, ax_lower_right)
    # add_logos(ax_lower_left)
    # add_last_value(df_24h, ax_top_left, station_name=station_name)
    # fig.subplots_adjust(hspace=0.3)
    # plt.savefig(f"img/{station_name}.png")
    plt.show()


import glob

files_24h = glob.glob("*/*/24h*.csv")
files_7d = glob.glob("*/*/7d*.csv")

# for file_24h, file_7d in zip(files_24h, files_7d):
# print(file_24h, file_7d)

file_24h = "site-data/Germanou/24h_Germanou.csv"
file_7d = "site-data/Germanou/7d_Germanou.csv"

df_24h = pd.read_csv(file_24h, parse_dates=True, index_col="time_stamp")
df_24h.index = df_24h.index.tz_convert("Europe/Athens")
station_name = get_station_name(file_24h)

df_7d = pd.read_csv(file_7d, parse_dates=True, index_col="time_stamp")
df_7d.index = df_7d.index.tz_convert("Europe/Athens")
plot_all(df_7d, df_24h, station_name=station_name)