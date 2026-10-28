"""
BUSINESS INTELLIGENCE ANALYTICS PROJECT

NAME   : Shikhar Agrawal

Topic  : Retail Sales Performance Analysis (Descriptive Analytics)
Course : BBA - IBM - 3rd sem (2025-2028)

Output: 6 charts saved in a folder called "charts"
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("charts", exist_ok=True)

# STEP 1: LOAD THE DATASET
df = pd.read_csv("retail_sales.csv", parse_dates=["Order Date"])

print("First 5 rows:")
print(df.head())
print("\nRows and columns:", df.shape)


# STEP 2: CLEAN THE DATA
print("\nMissing values in each column:")
print(df.isnull().sum())
print("Duplicate rows:", df.duplicated().sum())

df = df.drop_duplicates()                    # remove duplicate rows
df["Discount"] = df["Discount"].fillna(0)    # missing discount = no discount
print("Rows after cleaning:", len(df))


# STEP 3: KEY NUMBERS
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()

print("\n--- KPIs ---")
print("Total Sales   : Rs", round(total_sales / 100000, 1), "Lakh")
print("Total Profit  : Rs", round(total_profit / 100000, 1), "Lakh")
print("Profit Margin :", round(total_profit / total_sales * 100, 1), "%")
print("Total Orders  :", total_orders)

# STEP 4: ANALYSIS
# By region
region = df.groupby("Region")[["Sales", "Profit"]].sum()
region["Margin %"] = region["Profit"] / region["Sales"] * 100
print("\n--- By Region ---")
print(region.round(1))

# By category
category = df.groupby("Category")[["Sales", "Profit"]].sum()
category["Margin %"] = category["Profit"] / category["Sales"] * 100
print("\n--- By Category ---")
print(category.round(1))

# By sub-category
subcat = df.groupby("Sub-Category")[["Sales", "Profit"]].sum()
subcat["Margin %"] = subcat["Profit"] / subcat["Sales"] * 100
print("\n--- By Sub-Category ---")
print(subcat.round(1))

# Monthly sales
df["Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
monthly = df.groupby("Month")["Sales"].sum()

# Discount vs profit
discount = df.groupby("Discount")[["Sales", "Profit"]].sum()
discount["Margin %"] = discount["Profit"] / discount["Sales"] * 100
print("\n--- Profit Margin by Discount ---")
print(discount.round(1))

# Top 10 customers
top_customers = df.groupby("Customer ID")["Sales"].sum().sort_values(ascending=False).head(10)
print("\n--- Top 10 Customers ---")
print(top_customers.round(0))

# STEP 5: CHARTS
# Chart 1: Monthly sales trend
plt.figure(figsize=(9, 4.5))
plt.plot(monthly.index, monthly.values / 100000, marker="o", color="blue")
plt.title("Monthly Sales Trend (2024-2025)")
plt.ylabel("Sales (Rs Lakh)")
plt.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/1_monthly_sales_trend.png", dpi=150)
plt.close()

# Chart 2: Sales and profit by region
region[["Sales", "Profit"]].div(100000).plot(kind="bar", figsize=(8, 4.5), color=["blue", "green"])
plt.title("Sales and Profit by Region")
plt.ylabel("Rs Lakh")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/2_sales_profit_by_region.png", dpi=150)
plt.close()

# Chart 3: Profit by sub-category (red = loss)
subcat_sorted = subcat.sort_values("Profit")
colors = ["red" if p < 0 else "blue" for p in subcat_sorted["Profit"]]
plt.figure(figsize=(8, 5))
plt.barh(subcat_sorted.index, subcat_sorted["Profit"] / 100000, color=colors)
plt.axvline(0, color="black", linewidth=0.8)
plt.title("Profit by Sub-Category (red = loss)")
plt.xlabel("Profit (Rs Lakh)")
plt.tight_layout()
plt.savefig("charts/3_profit_by_subcategory.png", dpi=150)
plt.close()

# Chart 4: Profit margin by discount level
labels = [str(int(round(d * 100))) + "%" for d in discount.index]
colors = ["red" if m < 0 else "green" for m in discount["Margin %"]]
plt.figure(figsize=(8, 4.5))
plt.bar(labels, discount["Margin %"], color=colors)
plt.axhline(0, color="black", linewidth=0.8)
plt.title("Profit Margin by Discount Level")
plt.xlabel("Discount given")
plt.ylabel("Profit margin (%)")
plt.tight_layout()
plt.savefig("charts/4_margin_vs_discount.png", dpi=150)
plt.close()

# Chart 5: Share of sales by category
plt.figure(figsize=(6, 6))
plt.pie(category["Sales"], labels=category.index, autopct="%1.1f%%", startangle=90)
plt.title("Share of Sales by Category")
plt.tight_layout()
plt.savefig("charts/5_sales_share_by_category.png", dpi=150)
plt.close()

# Chart 6: Top 10 customers
plt.figure(figsize=(8, 5))
plt.barh(top_customers.index[::-1], top_customers.values[::-1] / 100000, color="blue")
plt.title("Top 10 Customers by Sales")
plt.xlabel("Sales (Rs Lakh)")
plt.tight_layout()
plt.savefig("charts/6_top_10_customers.png", dpi=150)
plt.close()

# STEP 6: KEY FINDINGS
print("\n--- KEY FINDINGS ---")
print("1. Overall profit margin:", round(total_profit / total_sales * 100, 1), "%")
print("2. Top region by sales:", region["Sales"].idxmax())
print("3. Top category by sales:", category["Sales"].idxmax())
print("4. Peak sales month:", monthly.idxmax().strftime("%B %Y"))
print("5. Loss-making sub-categories:", list(subcat[subcat["Profit"] < 0].index))
print("6. Margin with no discount:", round(discount["Margin %"].iloc[0], 1), "%",
      "| with 40% discount:", round(discount["Margin %"].iloc[-1], 1), "%")

print("\nDone! 6 charts saved in the 'charts' folder.")
