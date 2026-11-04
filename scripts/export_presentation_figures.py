"""Export presentation figures in high resolution for FH Kufstein Strategy Slides."""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Setup paths
output_dir = Path("docs/presentation_assets")
output_dir.mkdir(parents=True, exist_ok=True)

# Load data
df = pd.read_csv("data/interim/pump_clean.csv", parse_dates=["week_start"])

# Global style
sns.set_theme(style="white", font="Helvetica")
plt.rcParams["font.sans-serif"] = "Helvetica"
plt.rcParams["axes.edgecolor"] = "#cbd5e0"
plt.rcParams["axes.linewidth"] = 0.8

# Color palette inspired by FH Kufstein
FH_NAVY = "#1a365d"
FH_GREEN = "#7cb342"
FH_TEAL = "#00a3c4"
FH_RED = "#e53e3e"
FH_SLATE = "#4a5568"

# 1. Figure 1: Overall Class Imbalance
fig, ax = plt.subplots(figsize=(6, 3.8), dpi=300)
counts = df["failure_next_week"].value_counts().sort_index()
bars = ax.bar(["Healthy (0)", "Failure (1)"], counts, color=[FH_NAVY, FH_RED], edgecolor="black", width=0.45, linewidth=1)
ax.set_title("Operational Class Imbalance (24.4 : 1 Ratio)", fontsize=11, weight="bold", color=FH_NAVY, pad=12)
ax.set_ylabel("Pump-Weeks Count", fontsize=9, color=FH_SLATE)
ax.set_ylim(0, 11500)
for bar in bars:
    y = bar.get_height()
    pct = y / len(df) * 100
    ax.text(bar.get_x() + bar.get_width()/2, y + 250, f"{y:,}\n({pct:.2f}%)", ha="center", va="bottom", fontsize=9, weight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(output_dir / "fig1_imbalance.png", dpi=300)
plt.close()

# 2. Figure 2: Failure Rates by Site and Fluid
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.8), dpi=300)
site_rates = (df.groupby("site")["failure_next_week"].mean() * 100).reset_index()
sns.barplot(data=site_rates, x="site", y="failure_next_week", palette=[FH_NAVY, FH_TEAL, FH_SLATE], ax=ax1, edgecolor="black", width=0.5)
ax1.set_title("Failure Rate by Site (%)", fontsize=10, weight="bold", color=FH_NAVY)
ax1.set_ylabel("Rate (%)", fontsize=9)
ax1.set_ylim(0, 6)
for p in ax1.patches:
    ax1.annotate(f"{p.get_height():.2f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 0.15),
                 ha='center', va='bottom', fontsize=8.5, weight="bold")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

fluid_rates = (df.groupby("fluid")["failure_next_week"].mean() * 100).reset_index()
sns.barplot(data=fluid_rates, x="fluid", y="failure_next_week", palette=[FH_RED, FH_GREEN, FH_TEAL], ax=ax2, edgecolor="black", width=0.5)
ax2.set_title("Failure Rate by Fluid Type (%)", fontsize=10, weight="bold", color=FH_NAVY)
ax2.set_ylabel("Rate (%)", fontsize=9)
ax2.set_ylim(0, 6)
for p in ax2.patches:
    ax2.annotate(f"{p.get_height():.2f}%", (p.get_x() + p.get_width() / 2., p.get_height() + 0.15),
                 ha='center', va='bottom', fontsize=8.5, weight="bold")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(output_dir / "fig2_site_fluid.png", dpi=300)
plt.close()

# 3. Figure 3: Dominant Failure Mechanisms (Donut Chart)
fig, ax = plt.subplots(figsize=(6, 3.8), dpi=300)
mode_counts = df[df["failure_next_week"] == 1]["failure_mode"].value_counts()
colors = [FH_RED, FH_TEAL, FH_GREEN, "#ed8936", FH_SLATE]
wedges, texts, autotexts = ax.pie(
    mode_counts, labels=mode_counts.index, autopct="%1.1f%%", pctdistance=0.75,
    colors=colors, startangle=140, textprops=dict(color=FH_NAVY, weight="bold", size=8),
    wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2)
)
for at in autotexts:
    at.set_color("white")
    at.set_fontsize(8)
ax.set_title("Root Causes of 402 Failures (Bearings + Seals = 71.6%)", fontsize=10, weight="bold", color=FH_NAVY, pad=10)
plt.tight_layout()
plt.savefig(output_dir / "fig3_failure_modes.png", dpi=300)
plt.close()

# 4. Figure 4: Financial Disaster Matrix Comparison
fig, ax = plt.subplots(figsize=(6.5, 3.8), dpi=300)
models = ["Dummy Baseline\n(96.06% Acc)", "Realistic Model\n(80% Recall @ 12 Budget)", "Theoretical Oracle\n(100% Recall)"]
# Dummy: 402 * 18,000 = 7.236M
# Realistic: 80% of 402 = 321 caught (321 * 1200 + (52*12-321)*1200) + 81 missed * 18,000 = 0.748M + 1.458M = 2.206M
# Oracle: 402 * 1200 = 0.482M
costs = [7.236, 2.206, 0.482]
bars = ax.bar(models, costs, color=[FH_RED, FH_TEAL, FH_GREEN], edgecolor="black", width=0.45, linewidth=1)
ax.set_title("Annual Fleet Financial Impact (€ Millions)", fontsize=11, weight="bold", color=FH_NAVY, pad=12)
ax.set_ylabel("Total Operational Cost (€ Millions)", fontsize=9, color=FH_SLATE)
ax.set_ylim(0, 8.5)
for bar in bars:
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, y + 0.2, f"€{y:.2f}M", ha="center", va="bottom", fontsize=9, weight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(output_dir / "fig4_financial_impact.png", dpi=300)
plt.close()

print("All presentation figures generated successfully in docs/presentation_assets/")

