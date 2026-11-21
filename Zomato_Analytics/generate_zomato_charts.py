import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setup output folder & Zomato color theme
OUTPUT_DIR = "eda_charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)
PRIMARY = "#E23744"    # Zomato Red
SECONDARY = "#2D2D2D"  # Dark Slate
ACCENT = "#FF7E8B"     # Soft Coral
sns.set_theme(style="whitegrid", font_scale=1.05)

print("Loading Excel files (this may take 15-30 seconds for large files)...")
orders = pd.read_excel("orders.xlsx")
restaurants = pd.read_excel("restaurant.xlsx")
users = pd.read_excel("users.xlsx")
food = pd.read_excel("food.xlsx")
order_types = pd.read_excel("orders_Type.xlsx")

# Clean numeric & date columns safely
orders["sales_amount"] = pd.to_numeric(orders["sales_amount"], errors="coerce")
orders["sales_qty"] = pd.to_numeric(orders["sales_qty"], errors="coerce")
orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
restaurants["rating"] = pd.to_numeric(restaurants["rating"], errors="coerce")
users["Age"] = pd.to_numeric(users["Age"], errors="coerce")

# Merge orders with restaurants and users
df = orders.merge(restaurants, left_on="r_id", right_on="id", how="left", suffixes=("", "_rest"))
df = df.merge(users, on="user_id", how="left", suffixes=("", "_user"))

# --- Figure A1: Monthly Revenue Trend ---
monthly = df.dropna(subset=["order_date"]).groupby(df["order_date"].dt.to_period("M"))["sales_amount"].sum()
monthly.index = monthly.index.astype(str)
plt.figure(figsize=(10, 4.8))
plt.plot(monthly.index, monthly.values / 1e6, marker="o", color=PRIMARY, linewidth=2.5)
plt.fill_between(monthly.index, monthly.values / 1e6, color=ACCENT, alpha=0.2)
plt.title("Figure A1: Monthly Revenue Trend (in Millions)", fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Revenue (Millions)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/A1_monthly_revenue_trend.png", dpi=300)
plt.close()

# --- Figure A2: Top 10 Cities by Total Revenue ---
top_cities = df.groupby("city")["sales_amount"].sum().nlargest(10).sort_values()
plt.figure(figsize=(9, 5))
bars = plt.barh(top_cities.index, top_cities.values / 1e6, color=PRIMARY)
plt.title("Figure A2: Top 10 Cities by Total Revenue", fontweight="bold")
plt.xlabel("Total Revenue (Millions)")
for bar in bars:
    plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f" {bar.get_width():.1f}M", va="center", fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/A2_top10_cities_revenue.png", dpi=300)
plt.close()

# --- Figure A3: Top 10 Restaurants by Total Revenue ---
top_rest = df.dropna(subset=["name"]).assign(name=lambda x: x["name"].astype(str)).groupby("name")["sales_amount"].sum().nlargest(10).sort_values()
plt.figure(figsize=(10, 5))
bars = plt.barh(top_rest.index, top_rest.values / 1e6, color=SECONDARY)
plt.title("Figure A3: Top 10 Restaurants by Total Revenue", fontweight="bold")
plt.xlabel("Total Revenue (Millions)")
for bar in bars:
    plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f" {bar.get_width():.2f}M", va="center", fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/A3_top10_restaurants.png", dpi=300)
plt.close()

# --- Figure A4: Customer Demographics (Gender & Age Distribution) ---
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
gender_counts = df["Gender"].value_counts()
axes[0].pie(gender_counts.values, labels=gender_counts.index, autopct="%1.1f%%",
            colors=[PRIMARY, SECONDARY, ACCENT], startangle=90, wedgeprops=dict(width=0.45))
axes[0].set_title("Orders by Gender", fontweight="bold")

sns.histplot(users["Age"].dropna(), bins=20, kde=True, color=PRIMARY, ax=axes[1])
axes[1].axvline(users["Age"].mean(), color=SECONDARY, linestyle="--", label=f"Mean: {users['Age'].mean():.1f}")
axes[1].set_title("Customer Age Distribution", fontweight="bold")
axes[1].set_xlabel("Age")
axes[1].legend()

plt.suptitle("Figure A4: Customer Demographics Analysis", fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/A4_customer_demographics.png", dpi=300, bbox_inches="tight")
plt.close()

# --- Figure A5: Heatmap - Revenue by Occupation x Marital Status ---
pivot = df.pivot_table(index="Occupation", columns="Marital Status", values="sales_amount", aggfunc="sum") / 1e6
plt.figure(figsize=(8, 5))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="Reds", linewidths=0.5)
plt.title("Figure A5: Total Revenue (Millions) — Occupation vs Marital Status", fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/A5_occupation_marital_heatmap.png", dpi=300)
plt.close()

# --- Figure A6: Veg vs Non-Veg Split & Order Type Distribution ---
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
veg_counts = food["veg_or_non_veg"].value_counts()
axes[0].pie(veg_counts.values, labels=veg_counts.index, autopct="%1.1f%%",
            colors=["#2ECC71", PRIMARY, "#95A5A6"], startangle=90, wedgeprops=dict(width=0.45))
axes[0].set_title("Menu Items: Veg vs Non-Veg", fontweight="bold")

type_counts = order_types["Type"].value_counts()
sns.barplot(x=type_counts.index, y=type_counts.values, color=PRIMARY, ax=axes[1])
axes[1].set_title("Orders by Order Type", fontweight="bold")
axes[1].set_xlabel("Order Type")