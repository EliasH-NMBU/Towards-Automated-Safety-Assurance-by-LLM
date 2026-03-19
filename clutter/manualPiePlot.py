import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import os


plt.rcParams.update({
    "font.size": 13,
    "font.family": "serif",
    "axes.edgecolor": "black",
    "figure.dpi": 300,
    "axes.labelsize": 14,
    "axes.titlesize": 16,
    "legend.fontsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
})

out_dir = "analysis_plots"
os.makedirs(out_dir, exist_ok=True)


# ----------------------------
# Pie Chart (NMBU Colors)
# ----------------------------

TITLE = "Causes of Inaccuracy \n Rover Use Case"
value1 = 1
value2 = 1
value3 = 2
value4 = 1

NMBU_GREEN = "#07CA86"       # Primary green
NMBU_DARK_GREEN = "#087D54"  # For accuracy bar
NMBU_LIGHT_GREEN = "#8BC7B8"
NMBU_GREY_MED = "#FCBA06"     # False
NMBU_GREY_LIGHT = "#E6E6E6"
NMBU_GREY_DARK = "#4D4D4D"


fig, ax = plt.subplots(figsize=(6, 6))

labels = ['Generation', 'Description', 'Reference', 'Comparison']
myexplode = [0, 0, 0, 0]
sizes = [value1, value2, value3, value4]
colors = [NMBU_GREEN,NMBU_DARK_GREEN, NMBU_LIGHT_GREEN, NMBU_GREY_LIGHT]

wedges, texts, autotexts = ax.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    textprops={'color': 'black'},
    explode = myexplode
)

for text in texts + autotexts:
    text.set_fontsize(12)

ax.set_title(f"{TITLE}", pad=18)

plt.tight_layout()
plt.savefig(f"{out_dir}/falseReasoning.png", dpi=300)
plt.savefig(f"{out_dir}/falseReasoning.pdf", dpi=300)
plt.close()