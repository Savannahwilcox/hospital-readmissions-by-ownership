# Checks whether the for profit gap is really a size gap. For profit
# hospitals are smaller, and smaller hospitals tend to have higher
# readmission ratios

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

df = pd.read_csv("data/clean/hf_by_owner.csv", dtype={"Facility ID": str})
df = df.rename(columns={"Excess Readmission Ratio": "ratio",
                        "Number of Discharges": "discharges"})

# CMS hides discharge counts for some hospitals so they can't be sized
print("Hospitals missing discharge count:", df["discharges"].isna().sum())
df = df.dropna(subset=["discharges"])

# simple way: compare ownership inside each size group
df["size_group"] = pd.qcut(df["discharges"], 4,
                           labels=["Smallest", "Small-mid", "Mid-large", "Largest"])
table = df.pivot_table(index="size_group", columns="owner", values="ratio",
                       aggfunc="mean", observed=True)
print()
print(table.round(4))

# regression: ownership and size at the same time
before = smf.ols("ratio ~ C(owner, Treatment('Nonprofit'))", data=df).fit()
after = smf.ols("ratio ~ C(owner, Treatment('Nonprofit')) + np.log(discharges)", data=df).fit()

print()
print("WITHOUT SIZE")
print(before.params.round(4))
print()
print("WITH SIZE")
print(after.summary().tables[1])
print("R-squared:", round(after.rsquared, 3))