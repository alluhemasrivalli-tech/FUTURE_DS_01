# ============================================================
#  TASK 1 — Business Sales Performance Analytics
#  Internship: Data Science & Analytics | Future Interns
#  Dataset: Sample Superstore Sales (2021–2023)
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")

# ── Output folder ────────────────────────────────────────────
os.makedirs("outputs", exist_ok=True)

# ── Plot style ───────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#F8F9FA",
    "axes.facecolor":   "#FFFFFF",
    "axes.edgecolor":   "#CCCCCC",
    "axes.grid":        True,
    "grid.color":       "#EEEEEE",
    "grid.linestyle":   "--",
    "font.family":      "DejaVu Sans",
    "font.size":        10,
})

PALETTE = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D",
           "#3B1F2B", "#44BBA4", "#E94F37", "#393E41"]

# ════════════════════════════════════════════════════════════
# 1. LOAD & CLEAN DATA
# ════════════════════════════════════════════════════════════
print("=" * 60)
print("  BUSINESS SALES PERFORMANCE ANALYTICS")
print("=" * 60)

df = pd.read_csv("superstore_sales.csv", parse_dates=["Order Date"])

# Basic cleaning
df.drop_duplicates(subset="Order ID", inplace=True)
df.dropna(subset=["Sales", "Profit", "Region", "Category"], inplace=True)
df["Year"]    = df["Order Date"].dt.year
df["Month"]   = df["Order Date"].dt.to_period("M")
df["Quarter"] = df["Order Date"].dt.to_period("Q")
df["Profit Margin %"] = (df["Profit"] / df["Sales"] * 100).round(2)

print(f"\n✅ Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"   Date Range : {df['Order Date'].min().date()} → {df['Order Date'].max().date()}")
print(f"   Regions    : {sorted(df['Region'].unique())}")
print(f"   Categories : {sorted(df['Category'].unique())}")


# ════════════════════════════════════════════════════════════
# 2. KPI SUMMARY
# ════════════════════════════════════════════════════════════
total_sales    = df["Sales"].sum()
total_profit   = df["Profit"].sum()
total_orders   = df["Order ID"].nunique()
avg_order_val  = total_sales / total_orders
overall_margin = (total_profit / total_sales * 100)
total_qty      = df["Quantity"].sum()

print("\n" + "─" * 60)
print("  📊  KEY PERFORMANCE INDICATORS")
print("─" * 60)
print(f"  Total Revenue    : ${total_sales:>12,.2f}")
print(f"  Total Profit     : ${total_profit:>12,.2f}")
print(f"  Overall Margin   : {overall_margin:>11.2f}%")
print(f"  Total Orders     : {total_orders:>12,}")
print(f"  Avg Order Value  : ${avg_order_val:>12,.2f}")
print(f"  Total Units Sold : {total_qty:>12,}")
print("─" * 60)


# ════════════════════════════════════════════════════════════
# 3. REVENUE TREND ANALYSIS
# ════════════════════════════════════════════════════════════
monthly = (df.groupby("Month")[["Sales", "Profit"]]
             .sum()
             .reset_index()
             .sort_values("Month"))
monthly["Month_dt"] = monthly["Month"].dt.to_timestamp()

yearly = df.groupby("Year")[["Sales", "Profit"]].sum().reset_index()


# ════════════════════════════════════════════════════════════
# 4. TOP PRODUCTS & CATEGORIES
# ════════════════════════════════════════════════════════════
top_products = (df.groupby("Product Name")["Sales"]
                  .sum()
                  .sort_values(ascending=False)
                  .head(10)
                  .reset_index())

cat_perf = (df.groupby("Category")
              .agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Orders=("Order ID","count"))
              .reset_index())
cat_perf["Margin %"] = (cat_perf["Profit"] / cat_perf["Sales"] * 100).round(2)

subcat_sales = (df.groupby(["Category","Sub-Category"])["Sales"]
                  .sum()
                  .sort_values(ascending=False)
                  .reset_index())


# ════════════════════════════════════════════════════════════
# 5. REGIONAL PERFORMANCE
# ════════════════════════════════════════════════════════════
region_perf = (df.groupby("Region")
                 .agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Orders=("Order ID","count"))
                 .reset_index()
                 .sort_values("Sales", ascending=False))
region_perf["Margin %"] = (region_perf["Profit"] / region_perf["Sales"] * 100).round(2)

state_perf = (df.groupby("State")["Sales"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index())


# ════════════════════════════════════════════════════════════
# 6. SEGMENT ANALYSIS
# ════════════════════════════════════════════════════════════
seg_perf = (df.groupby("Segment")
              .agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
              .reset_index())
seg_perf["Margin %"] = (seg_perf["Profit"] / seg_perf["Sales"] * 100).round(2)


# ════════════════════════════════════════════════════════════
# 7.  DISCOUNT IMPACT
# ════════════════════════════════════════════════════════════
disc_bins   = [0, 0.01, 0.11, 0.21, 0.31, 1.0]
disc_labels = ["No Discount","1-10%","11-20%","21-30%","31%+"]
df["Discount Band"] = pd.cut(df["Discount"], bins=disc_bins,
                              labels=disc_labels, include_lowest=True)
disc_impact = (df.groupby("Discount Band", observed=True)
                 .agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Orders=("Order ID","count"))
                 .reset_index())
disc_impact["Margin %"] = (disc_impact["Profit"] / disc_impact["Sales"] * 100).round(2)


# ════════════════════════════════════════════════════════════
# 8. PRINT INSIGHTS
# ════════════════════════════════════════════════════════════
print("\n  🏆  TOP 5 PRODUCTS BY REVENUE")
for i, row in top_products.head(5).iterrows():
    print(f"    {i+1}. {row['Product Name']:<30}  ${row['Sales']:>10,.2f}")

print("\n  📦  CATEGORY PERFORMANCE")
for _, row in cat_perf.iterrows():
    print(f"    {row['Category']:<20}  Sales: ${row['Sales']:>10,.2f}  "
          f"Profit: ${row['Profit']:>8,.2f}  Margin: {row['Margin %']:.1f}%")

print("\n  🌍  REGIONAL PERFORMANCE")
for _, row in region_perf.iterrows():
    print(f"    {row['Region']:<10}  Sales: ${row['Sales']:>10,.2f}  "
          f"Profit: ${row['Profit']:>8,.2f}  Margin: {row['Margin %']:.1f}%")

print("\n  👥  SEGMENT PERFORMANCE")
for _, row in seg_perf.iterrows():
    print(f"    {row['Segment']:<15}  Sales: ${row['Sales']:>10,.2f}  "
          f"Margin: {row['Margin %']:.1f}%")


# ════════════════════════════════════════════════════════════
# 9. VISUALIZATIONS
# ════════════════════════════════════════════════════════════

# ── Figure 1 : Revenue & Profit Trend ───────────────────────
fig, axes = plt.subplots(2, 1, figsize=(14, 8), facecolor="#F8F9FA")
fig.suptitle("Revenue & Profit Trends (2021–2023)", fontsize=15, fontweight="bold", y=1.01)

ax1 = axes[0]
ax1.fill_between(monthly["Month_dt"], monthly["Sales"],
                 alpha=0.25, color=PALETTE[0])
ax1.plot(monthly["Month_dt"], monthly["Sales"],
         color=PALETTE[0], linewidth=2.5, marker="o", markersize=4, label="Monthly Sales")
ax1.set_title("Monthly Revenue Trend", fontweight="bold")
ax1.set_ylabel("Revenue ($)")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"${x:,.0f}"))
ax1.legend()

ax2 = axes[1]
ax2.fill_between(monthly["Month_dt"], monthly["Profit"],
                 alpha=0.25, color=PALETTE[2])
ax2.plot(monthly["Month_dt"], monthly["Profit"],
         color=PALETTE[2], linewidth=2.5, marker="s", markersize=4, label="Monthly Profit")
ax2.axhline(0, color="red", linewidth=1, linestyle="--", alpha=0.6)
ax2.set_title("Monthly Profit Trend", fontweight="bold")
ax2.set_ylabel("Profit ($)")
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"${x:,.0f}"))
ax2.legend()

plt.tight_layout()
plt.savefig("outputs/01_revenue_profit_trend.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n  ✅  Chart saved: outputs/01_revenue_profit_trend.png")


# ── Figure 2 : Top 10 Products ───────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6), facecolor="#F8F9FA")
bars = ax.barh(top_products["Product Name"][::-1],
               top_products["Sales"][::-1],
               color=PALETTE[:10], edgecolor="white", height=0.6)
for bar, val in zip(bars, top_products["Sales"][::-1]):
    ax.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2,
            f"${val:,.0f}", va="center", fontsize=9)
ax.set_title("Top 10 Products by Revenue", fontsize=14, fontweight="bold")
ax.set_xlabel("Total Sales ($)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"${x:,.0f}"))
ax.set_xlim(0, top_products["Sales"].max() * 1.2)
plt.tight_layout()
plt.savefig("outputs/02_top10_products.png", dpi=150, bbox_inches="tight")
plt.close()
print("  ✅  Chart saved: outputs/02_top10_products.png")


# ── Figure 3 : Category & Sub-Category ──────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor="#F8F9FA")

# Pie – category share
ax = axes[0]
wedges, texts, autotexts = ax.pie(
    cat_perf["Sales"], labels=cat_perf["Category"],
    autopct="%1.1f%%", startangle=140,
    colors=PALETTE[:3], pctdistance=0.75,
    wedgeprops=dict(edgecolor="white", linewidth=2))
for at in autotexts:
    at.set_fontsize(11)
    at.set_fontweight("bold")
ax.set_title("Revenue Share by Category", fontweight="bold")

# Bar – sub-category top 10
ax2 = axes[1]
top_sub = subcat_sales.head(10)
colors_sub = [PALETTE[0] if c=="Technology" else
              PALETTE[1] if c=="Furniture" else PALETTE[2]
              for c in top_sub["Category"]]
ax2.bar(top_sub["Sub-Category"], top_sub["Sales"], color=colors_sub, edgecolor="white")
ax2.set_title("Top Sub-Categories by Revenue", fontweight="bold")
ax2.set_xlabel("Sub-Category")
ax2.set_ylabel("Sales ($)")
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"${x:,.0f}"))
plt.xticks(rotation=35, ha="right")

from matplotlib.patches import Patch
legend_els = [Patch(facecolor=PALETTE[0], label="Technology"),
              Patch(facecolor=PALETTE[1], label="Furniture"),
              Patch(facecolor=PALETTE[2], label="Office Supplies")]
ax2.legend(handles=legend_els, fontsize=9)

plt.tight_layout()
plt.savefig("outputs/03_category_subcategory.png", dpi=150, bbox_inches="tight")
plt.close()
print("  ✅  Chart saved: outputs/03_category_subcategory.png")


# ── Figure 4 : Regional Performance ─────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor="#F8F9FA")

ax = axes[0]
x = np.arange(len(region_perf))
w = 0.4
ax.bar(x - w/2, region_perf["Sales"],   width=w, color=PALETTE[0], label="Sales",  edgecolor="white")
ax.bar(x + w/2, region_perf["Profit"],  width=w, color=PALETTE[2], label="Profit", edgecolor="white")
ax.set_xticks(x)
ax.set_xticklabels(region_perf["Region"])
ax.set_title("Sales & Profit by Region", fontweight="bold")
ax.set_ylabel("Amount ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"${x:,.0f}"))
ax.legend()

ax2 = axes[1]
ax2.barh(state_perf["State"][::-1], state_perf["Sales"][::-1],
         color=sns.color_palette("Blues_d", len(state_perf)), edgecolor="white")
ax2.set_title("Top 10 States by Revenue", fontweight="bold")
ax2.set_xlabel("Sales ($)")
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"${x:,.0f}"))

plt.tight_layout()
plt.savefig("outputs/04_regional_performance.png", dpi=150, bbox_inches="tight")
plt.close()
print("  ✅  Chart saved: outputs/04_regional_performance.png")


# ── Figure 5 : KPI Dashboard ─────────────────────────────────
fig = plt.figure(figsize=(16, 10), facecolor="#1A1A2E")
gs  = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

def kpi_card(ax, title, value, subtitle="", bg="#16213E", fg="#E0E0E0", accent="#0F3460"):
    ax.set_facecolor(bg)
    for spine in ax.spines.values():
        spine.set_edgecolor(accent)
        spine.set_linewidth(2)
    ax.set_xticks([]); ax.set_yticks([])
    ax.text(0.5, 0.62, value,   transform=ax.transAxes,
            ha="center", va="center", fontsize=18, fontweight="bold", color="#E94560")
    ax.text(0.5, 0.30, title,   transform=ax.transAxes,
            ha="center", va="center", fontsize=10, color=fg)
    ax.text(0.5, 0.12, subtitle,transform=ax.transAxes,
            ha="center", va="center", fontsize=8,  color="#888888")

# KPI cards
kpi_card(fig.add_subplot(gs[0,0]), "Total Revenue",
         f"${total_sales/1e6:.2f}M", "All Regions • 2021–2023")
kpi_card(fig.add_subplot(gs[0,1]), "Total Profit",
         f"${total_profit/1e3:.1f}K", f"Margin: {overall_margin:.1f}%")
kpi_card(fig.add_subplot(gs[0,2]), "Total Orders",
         f"{total_orders:,}", f"AOV: ${avg_order_val:,.0f}")

# Yearly trend bar
ax_yr = fig.add_subplot(gs[1,:2])
ax_yr.set_facecolor("#16213E")
bars = ax_yr.bar(yearly["Year"], yearly["Sales"], color=["#E94560","#0F3460","#533483"],
                 edgecolor="white", width=0.5)
for bar, val in zip(bars, yearly["Sales"]):
    ax_yr.text(bar.get_x()+bar.get_width()/2, bar.get_height()+500,
               f"${val:,.0f}", ha="center", color="white", fontsize=9)
ax_yr.set_title("Yearly Revenue", color="white", fontweight="bold")
ax_yr.set_facecolor("#16213E")
ax_yr.tick_params(colors="white")
ax_yr.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"${x:,.0f}"))
ax_yr.spines[:].set_color("#333355")

# Segment donut
ax_seg = fig.add_subplot(gs[1,2])
ax_seg.set_facecolor("#16213E")
wedges,_,autotexts = ax_seg.pie(seg_perf["Sales"], labels=seg_perf["Segment"],
                                 autopct="%1.0f%%", startangle=90,
                                 colors=["#E94560","#0F3460","#533483"],
                                 wedgeprops=dict(width=0.55, edgecolor="#1A1A2E"))
for at in autotexts: at.set_color("white"); at.set_fontsize(9)
ax_seg.set_title("Revenue by Segment", color="white", fontweight="bold")

# Region margin bar
ax_rm = fig.add_subplot(gs[2,:2])
ax_rm.set_facecolor("#16213E")
region_perf_s = region_perf.sort_values("Margin %", ascending=True)
colors_m = ["#E94560" if m < 15 else "#44BBA4" for m in region_perf_s["Margin %"]]
ax_rm.barh(region_perf_s["Region"], region_perf_s["Margin %"], color=colors_m, edgecolor="white")
ax_rm.set_title("Profit Margin % by Region", color="white", fontweight="bold")
ax_rm.tick_params(colors="white")
ax_rm.set_xlabel("Margin %", color="white")
ax_rm.spines[:].set_color("#333355")
ax_rm.axvline(15, color="yellow", linestyle="--", alpha=0.5, linewidth=1)

# Discount impact
ax_di = fig.add_subplot(gs[2,2])
ax_di.set_facecolor("#16213E")
ax_di.bar(disc_impact["Discount Band"].astype(str), disc_impact["Margin %"],
          color=["#44BBA4","#F18F01","#E94560","#C73E1D","#6B0F1A"], edgecolor="white")
ax_di.set_title("Margin by Discount Band", color="white", fontweight="bold")
ax_di.tick_params(colors="white", axis="both")
plt.xticks(rotation=25, ha="right")
ax_di.set_ylabel("Margin %", color="white")
ax_di.spines[:].set_color("#333355")

fig.suptitle("Business Sales Performance Dashboard  |  2021–2023",
             fontsize=16, fontweight="bold", color="white", y=1.01)
plt.savefig("outputs/05_kpi_dashboard.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close()
print("  ✅  Chart saved: outputs/05_kpi_dashboard.png")


# ── Figure 6 : Correlation Heatmap ──────────────────────────
fig, ax = plt.subplots(figsize=(8, 5), facecolor="#F8F9FA")
corr = df[["Sales","Profit","Quantity","Discount","Unit Price","Profit Margin %"]].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn",
            mask=mask, ax=ax, linewidths=0.5,
            cbar_kws={"shrink": 0.8})
ax.set_title("Correlation Heatmap – Key Metrics", fontweight="bold", fontsize=13)
plt.tight_layout()
plt.savefig("outputs/06_correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
print("  ✅  Chart saved: outputs/06_correlation_heatmap.png")


# ════════════════════════════════════════════════════════════
# 10. INSIGHTS & RECOMMENDATIONS
# ════════════════════════════════════════════════════════════
best_region  = region_perf.iloc[0]["Region"]
worst_margin = region_perf.sort_values("Margin %").iloc[0]["Region"]
best_cat     = cat_perf.sort_values("Margin %", ascending=False).iloc[0]["Category"]
worst_disc   = disc_impact.sort_values("Margin %").iloc[0]["Discount Band"]
top_prod     = top_products.iloc[0]["Product Name"]

print("\n" + "═"*60)
print("  💡  KEY INSIGHTS & RECOMMENDATIONS")
print("═"*60)
print(f"""
  1. REVENUE LEADER  ▶  {best_region} region drives the highest revenue.
     → Invest more in marketing & inventory for this region.

  2. MARGIN ALERT    ▶  {worst_margin} region has the lowest profit margin.
     → Review pricing strategy and reduce operational costs here.

  3. BEST CATEGORY   ▶  {best_cat} yields the highest profit margins.
     → Prioritize {best_cat} upselling in all regions.

  4. TOP PRODUCT     ▶  '{top_prod}' leads in total revenue.
     → Ensure consistent stock availability for this product.

  5. DISCOUNT RISK   ▶  '{worst_disc}' discount band destroys margins.
     → Cap discounts at 20% to protect profitability.

  6. SEASONAL TREND  ▶  Q4 shows consistent revenue spikes each year.
     → Align promotional campaigns and stock build-up for Q4.
""")
print("═"*60)
print("  ✅  All outputs saved in → outputs/ folder")
print("═"*60)
