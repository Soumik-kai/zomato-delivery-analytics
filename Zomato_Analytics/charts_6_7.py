import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_DIR = "eda_charts"
PRIMARY = "#E23744"
sns.set_theme(style="whitegrid", font_scale=1.05)

# Load data for A6 & A7
food = pd.read_excel("food.xlsx")
order_types = pd.read_excel("orders_Type.xlsx")
orders = pd.read_excel("orders.xlsx")
restaurants = pd.read_excel("restaurant.xlsx")
users = pd.read_excel("users.xlsx")

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
axes[1].set_ylabel("Count")
axes[1].tick_params(axis="x", rotation=20)

plt.suptitle("Figure A6: Food Preference & Order Type Analysis", fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/A6_veg_nonveg_and_order_type.png", dpi=300, bbox_inches="tight")
plt.close()

# --- Figure A7: Correlation Matrix of Numerical Features ---
orders["sales_amount"] = pd.to_numeric(orders["sales_amount"], errors="coerce")
orders["sales_qty"] = pd.to_numeric(orders["sales_qty"], errors="coerce")
restaurants["rating"] = pd.to_numeric(restaurants["rating"], errors="coerce")
users["Age"] = pd.to_numeric(users["Age"], errors="coerce")

df = orders.merge(restaurants, left_on="r_id", right_on="id", how="left")
df = df.merge(users, on="user_id", how="left")

num_cols = df[["sales_qty", "sales_amount", "Age", "rating"]].dropna()
plt.figure(figsize=(7, 5.5))
sns.heatmap(num_cols.corr(), annot=True, fmt=".2f", cmap="RdBu_r", center=0, square=True)
plt.title("Figure A7: Correlation Matrix of Numerical Features", fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/A7_correlation_heatmap.png", dpi=300)
plt.close()

print("Done! A6 and A7 saved in eda_charts/")