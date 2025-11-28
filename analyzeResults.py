import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import os

USECASE = "UV Robot Use Case"
TEMP = "0"
csv_file = "results/100+IterationResults/20251128192047_ptLTL_results.csv"
ITERAITIONS = "1000"

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

NMBU_GREEN = "#07CA86"       # Primary green
NMBU_DARK_GREEN = "#087D54"  # For accuracy bar
NMBU_LIGHT_GREEN = "#8BC7B8"
NMBU_GREY_MED = "#FCBA06"     # False
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

labels = ['True', 'False']
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

ax.set_title(f"Equivalence Results\n {USECASE}, temperature = {TEMP}", pad=18)

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


# ----------------------------
# Horizontal Bar Plot per Requirement (Counts, not proportions)
# ----------------------------

if "ID" not in df.columns:
    print("⚠️ No 'ID' column found in CSV. Skipping per-requirement bar plot.")
else:
    # Count True/False per requirement
    grouped = df.groupby("ID")["Equivalence Check"].agg(
        true_count=lambda x: x.sum(),
        false_count=lambda x: (~x).sum(),
        total=lambda x: len(x)
    ).reset_index()

    # Total number of iterations per requirement (assumed same for all)
    iterations = int(grouped["total"].iloc[0])

    # Reverse order for better visualization
    grouped = grouped.iloc[::-1]

    fig, ax = plt.subplots(figsize=(9, max(4, len(grouped) * 0.35)))

    y_positions = np.arange(len(grouped))

    # True counts
    ax.barh(
        y_positions,
        grouped["true_count"],
        color=NMBU_GREEN,
        edgecolor="black",
        label="True"
    )

    """"
    # False counts stacked to the right of True counts
    ax.barh(
        y_positions,
        grouped["false_count"],
        left=grouped["true_count"],
        color=NMBU_GREY_MED,
        edgecolor="black",
        label="False"
    )
    """

    # Requirement ID on Y-axis
    ax.set_yticks(y_positions)
    ax.set_yticklabels(grouped["ID"], fontsize=11)
    ax.set_ylabel("ID", fontsize=13, rotation=0)

    ax.set_xlabel("Iterations", fontsize=13)
    ax.set_title(f"Equivalence Results \n {USECASE}, temperature = {TEMP}", fontsize=15, pad=30)

    # X-axis shows total iterations
    ax.set_xlim(0, iterations)

    # Add light grid
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    # Legend
    ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, 1.12),
    ncol=2,
    frameon=False
    )


    # Leave 8% of the figure height free at the top for the legend
    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.savefig(f"{out_dir}/per_requirement_horizontal_bars_counts.png", dpi=300)
    plt.savefig(f"{out_dir}/per_requirement_horizontal_bars_counts.pdf", dpi=300)
    plt.close()

    print(f"📘 Per-requirement horizontal count bar chart generated. (Iterations = {iterations})")
