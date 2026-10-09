# runs the same size adjusted regression for all six conditions to see
# whether the for profit gap shows up beyond heart failure.

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

readmissions = pd.read_csv("data/raw/FY_2026_Hospital_Readmissions_Reduction_Program_Hospital.csv",
                           dtype={"Facility ID": str})
hospitals = pd.read_csv("data/raw/Hospital_General_Information.csv", dtype={"Facility ID": str})

owner_groups = {
    "Proprietary": "For-profit",
    "Physician": "For-profit",
    "Voluntary non-profit - Private": "Nonprofit",
    "Voluntary non-profit - Other": "Nonprofit",
    "Voluntary non-profit - Church": "Nonprofit",
    "Government - Hospital District or Authority": "Government",
    "Government - Local": "Government",
    "Government - State": "Government",
    "Government - Federal": "Government",
    "Veterans Health Administration": "Government",
    "Department of Defense": "Government",
    "Tribal": "Government",
}

df = readmissions.merge(hospitals[["Facility ID", "Hospital Ownership"]], on="Facility ID")
df["owner"] = df["Hospital Ownership"].map(owner_groups)
df = df.rename(columns={"Excess Readmission Ratio": "ratio",
                        "Number of Discharges": "discharges"})
df = df.dropna(subset=["ratio", "discharges", "owner"])

results = []
for condition, rows in df.groupby("Measure Name"):
    model = smf.ols("ratio ~ C(owner, Treatment('Nonprofit')) + np.log(discharges)",
                    data=rows).fit()
    for group in ["For-profit", "Government"]:
        name = f"C(owner, Treatment('Nonprofit'))[T.{group}]"
        low, high = model.conf_int().loc[name]
        results.append({
            "condition": condition,
            "group": group,
            "hospitals": len(rows),
            "gap_vs_nonprofit": model.params[name],
            "ci_low": low,
            "ci_high": high,
            "significant": low > 0 or high < 0,
        })

results = pd.DataFrame(results)
print(results.round(4).to_string(index=False))
results.to_csv("data/clean/gaps_by_condition.csv", index=False)