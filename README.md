# 📊 Task 1 — Business Sales Performance Analytics
**Internship:** Data Science & Analytics | Future Interns  
**Track Code:** DS &nbsp;|&nbsp; **Repository:** FUTURE_DS_01

---

## 📌 Objective
Analyze business sales data to identify:
- Revenue trends over time (monthly, quarterly, yearly)
- Top-selling products and high-value categories
- Regional performance comparison
- Customer segment insights
- Discount impact on profitability

---

## 🗂️ Dataset
**Name:** Sample Superstore Sales Dataset  
**Period:** January 2021 – December 2023  
**Records:** 1,000 orders  
**Source:** Synthetically generated based on the classic Superstore schema (Kaggle)

| Column | Description |
|---|---|
| Order ID | Unique order identifier |
| Order Date | Date of purchase |
| Ship Mode | Shipping method |
| Customer ID / Name | Customer details |
| Segment | Consumer / Corporate / Home Office |
| City, State, Region | Geographic data |
| Category / Sub-Category | Product hierarchy |
| Product Name | Item sold |
| Unit Price, Quantity | Pricing details |
| Discount | Discount applied |
| Sales | Final revenue |
| Profit | Net profit |

---

## 🛠️ Tools & Libraries
- **Python 3.x**
- `pandas` — data manipulation
- `numpy` — numerical operations
- `matplotlib` — core visualizations
- `seaborn` — statistical plots

---

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/FUTURE_DS_01.git
cd FUTURE_DS_01

# 2. Install dependencies
pip install pandas numpy matplotlib seaborn openpyxl

# 3. Run the analysis
python sales_analysis.py
```

All charts will be saved automatically in the `outputs/` folder.

---

## 📊 Key Performance Indicators

| KPI | Value |
|---|---|
| Total Revenue | $2,648,423.82 |
| Total Profit | $432,887.66 |
| Overall Profit Margin | 16.35% |
| Total Orders | 1,000 |
| Avg Order Value | $2,648.42 |
| Total Units Sold | 5,078 |

---

## 📈 Visualizations Generated

| File | Description |
|---|---|
| `01_revenue_profit_trend.png` | Monthly revenue & profit trend lines |
| `02_top10_products.png` | Top 10 products by revenue |
| `03_category_subcategory.png` | Category share pie + sub-category bar chart |
| `04_regional_performance.png` | Region-wise sales & profit + top 10 states |
| `05_kpi_dashboard.png` | Dark-theme executive KPI dashboard |
| `06_correlation_heatmap.png` | Correlation heatmap of key metrics |

---

## 💡 Key Insights & Recommendations

1. **West region** leads in total revenue — increase marketing investment here.
2. **East region** has the lowest profit margin (15.5%) — review pricing and costs.
3. **Technology** category delivers the highest margins (20.6%) — prioritize upselling.
4. **Nokia G50** is the top revenue-generating product — maintain stock availability.
5. **Discounts above 20%** severely erode profit margins — implement a 20% cap policy.
6. **Q4 seasonal spike** is consistent across all years — align inventory and promotions.

---

## 📁 Repository Structure

```
FUTURE_DS_01/
│
├── sales_analysis.py          ← Main analysis script
├── superstore_sales.csv       ← Dataset
├── README.md                  ← Project documentation
│
└── outputs/
    ├── 01_revenue_profit_trend.png
    ├── 02_top10_products.png
    ├── 03_category_subcategory.png
    ├── 04_regional_performance.png
    ├── 05_kpi_dashboard.png
    └── 06_correlation_heatmap.png
```

---

## 👤 Author
**Internship Program:** Future Interns  
**Domain:** Data Science & Analytics  
**LinkedIn:** [Future Interns](https://www.linkedin.com/company/future-interns/)
