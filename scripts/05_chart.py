# Forest plot of the size adjusted for-profit gap for each condition

import pandas as pd
import matplotlib.pyplot as plt

FONT = ["Avenir Next", "Helvetica Neue", "Arial"]
INK = "#1f2a36"
MUTED = "#7d8794"
ACCENT = "#b5432c"
LIGHT = "#c9ced4"
GRID = "#e6e8eb"
SOURCE = "Source: CMS Hospital Readmissions Reduction Program, FY 2026. Adjusted for hospital size (discharges)."

plt.rcParams["font.family"] = FONT
plt.rcParams["text.color"] = INK
plt.rcParams["axes.labelcolor"] = MUTED
plt.rcParams["xtick.color"] = MUTED
plt.rcParams["ytick.color"] = INK

names = {
    "READM-30-PN-HRRP": "Pneumonia",
    "READM-30-AMI-HRRP": "Heart attack",
    "READM-30-HF-HRRP": "Heart failure",
    "READM-30-COPD-HRRP": "COPD",
    "READM-30-CABG-HRRP": "Bypass surgery",
    "READM-30-HIP-KNEE-HRRP": "Hip/knee replacement",
}

df = pd.read_csv("data/clean/gaps_by_condition.csv")
df = df[df["group"] == "For-profit"].copy()
df["label"] = df["condition"].map(names) + "  (" + df["hospitals"].astype(str) + " hospitals)"

# fewest hospitals at the bottom, most at the top
df = df.sort_values("hospitals")

fig, ax = plt.subplots(figsize=(9, 5.5))
fig.subplots_adjust(top=0.80, bottom=0.16, left=0.33, right=0.96)

for i, row in enumerate(df.itertuples()):
    color = ACCENT if row.significant else LIGHT
    ax.plot([row.ci_low, row.ci_high], [i, i], color=color, linewidth=2.5, solid_capstyle="round")
    ax.scatter(row.gap_vs_nonprofit, i, s=70, color=color, edgecolor="white", linewidth=1, zorder=3)

ax.axvline(0, color=MUTED, linewidth=1)
ax.text(0.001, len(df) - 0.45, "Same as nonprofit", fontsize=8.5, color=MUTED, ha="left")

ax.set_yticks(range(len(df)))
ax.set_yticklabels(df["label"], fontsize=10)
ax.set_xlabel("Difference in excess readmission ratio, for-profit minus nonprofit")
ax.tick_params(length=0)
for side in ["top", "right", "left"]:
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(LIGHT)
ax.xaxis.grid(True, color=GRID, linewidth=1)
ax.set_axisbelow(True)

fig.text(0.04, 0.94, "For-profit hospitals have higher readmission ratios than nonprofits",
         fontsize=15, fontweight="bold", ha="left")
fig.text(0.04, 0.895, "Dot is the gap, line is the 95% confidence interval. Gray means the line crosses zero.",
         fontsize=10.5, color=MUTED, ha="left")
fig.text(0.04, 0.03, SOURCE, fontsize=8, color=MUTED, ha="left")

plt.savefig("charts/for_profit_gap_by_condition.png", dpi=200)
plt.close()
print("Saved charts/for_profit_gap_by_condition.png")