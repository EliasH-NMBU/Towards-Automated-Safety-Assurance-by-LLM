import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import os

# ----------------------------
# Wilson Score Confidence Interval
# ----------------------------
def wilson_ci(successes, n, confidence=0.95):
    if n == 0:
        return (0, 0)
    z = norm.ppf(1 - (1 - confidence) / 2)
    phat = successes / n
    denominator = 1 + z**2 / n
    center = (phat + z*z/(2*n)) / denominator
    margin = z*np.sqrt((phat*(1-phat) + z*z/(4*n)) / n) / denominator
    return center - margin, center + margin

# ----------------------------
# Load CSV
# ----------------------------
csv_file = "results/100+IterationResults/20251125163934_ptLTL_results_temp1.csv"

df = pd.read_csv(csv_file)
df['Equivalence Check'] = df['Equivalence Check'].astype(bool)

true_count = df['Equivalence Check'].sum()
false_count = len(df) - true_count
total = len(df)
accuracy = true_count / total
ci_low, ci_high = wilson_ci(true_count, total)

print("=== SUMMARY STATISTICS ===")
print(f"Total formulas: {total}")
print(f"Correct (True): {true_count}")
print(f"Incorrect (False): {false_count}")
print(f"Accuracy: {accuracy:.3f}")
print(f"95% CI: [{ci_low:.3f}, {ci_high:.3f}]\n")

# ----------------------------
# NMBU Color Palette
# ----------------------------
NMBU_GREEN = "#14A170"       # Primary green
NMBU_DARK_GREEN = "#087D54"  # For accuracy bar
NMBU_LIGHT_GREEN = "#8BC7B8"
NMBU_GREY_MED = "#DDA41F"     # False
NMBU_GREY_LIGHT = "#E6E6E6"
NMBU_GREY_DARK = "#4D4D4D"

# ----------------------------
# Publication Style
# ----------------------------
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
fig, ax = plt.subplots(figsize=(6, 6))

labels = ['Equivalent', 'Not Equivalent']
myexplode = [0, 0.1]
sizes = [true_count, false_count]
colors = [NMBU_GREEN, NMBU_GREY_MED]

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

ax.set_title("Equivalence Results, 100 iterations,\n rover use case, temperature = 1", pad=18)

plt.tight_layout()
plt.savefig(f"{out_dir}/equivalence_pie_chart.png", dpi=300)
plt.savefig(f"{out_dir}/equivalence_pie_chart.pdf", dpi=300)
plt.close()

# ----------------------------
# Bar Chart with Confidence Interval (NMBU Style)
# ----------------------------
fig, ax = plt.subplots(figsize=(6, 6))

ax.bar(['Accuracy'], [accuracy], color=NMBU_DARK_GREEN, edgecolor="black")
ax.errorbar(
    ['Accuracy'],
    [accuracy],
    yerr=[[accuracy - ci_low], [ci_high - accuracy]],
    fmt='o',
    color='black',
    capsize=6,
)

ax.set_ylim(0, 1)
ax.set_ylabel("Proportion")
ax.set_title("Model Accuracy with 95% Confidence Interval")

plt.tight_layout()
plt.savefig(f"{out_dir}/accuracy_ci.png", dpi=300)
plt.savefig(f"{out_dir}/accuracy_ci.pdf", dpi=300)
plt.close()

# ----------------------------
# Summary Table
# ----------------------------
fig, ax = plt.subplots(figsize=(7, 1.8))
ax.axis('off')

table_data = [
    ["Total", total],
    ["Correct", true_count],
    ["Incorrect", false_count],
    ["Accuracy", f"{accuracy:.3f}"],
    ["95% CI", f"[{ci_low:.3f}, {ci_high:.3f}]"]
]

table = ax.table(
    cellText=table_data,
    colLabels=["Metric", "Value"],
    loc="center",
    cellLoc="center",
)

table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1, 1.3)

plt.savefig(f"{out_dir}/summary_table.png", dpi=300, bbox_inches='tight')
plt.savefig(f"{out_dir}/summary_table.pdf", dpi=300, bbox_inches='tight')
plt.close()

print(f"📊 All NMBU-color scientific plots saved in: {out_dir}")
