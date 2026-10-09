# Compares heart failure readmissions across hospital ownership types.
# Groups CMS's 12 ownership categories into for-profit, nonprofit and
# government so no group is too small to compare.

import pandas as pd

readmissions = pd.read_csv("data/raw/FY_2026_Hospital_Readmissions_Reduction_Program_Hospital.csv",
                           dtype={"Facility ID": str})
hospitals = pd.read_csv("data/raw/Hospital_General_Information.csv", dtype={"Facility ID": str})

# heart failure has the fewest missing ratios of the six conditions
hf = readmissions[readmissions["Measure Name"] == "READM-30-HF-HRRP"]
hf = hf[hf["Excess Readmission Ratio"].notna()]
print("Heart failure hospitals with a ratio:", len(hf))

df = hf.merge(hospitals[["Facility ID", "Hospital Ownership"]], on="Facility ID", how="left")
print("No ownership match:", df["Hospital Ownership"].isna().sum())
df = df[df["Hospital Ownership"].notna()]

# physician-owned hospitals are for-profit businesses, so they go with proprietary
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
df["owner"] = df["Hospital Ownership"].map(owner_groups)

# above 1.0 means more readmissions than CMS expected-->  penalized
df["above_expected"] = df["Excess Readmission Ratio"] > 1.0

summary = df.groupby("owner").agg(
    hospitals=("owner", "size"),
    mean_ratio=("Excess Readmission Ratio", "mean"),
    pct_above=("above_expected", "mean"),
    median_discharges=("Number of Discharges", "median"),
)
summary["pct_above"] = summary["pct_above"] * 100
print(summary.round(3))

df.to_csv("data/clean/hf_by_owner.csv", index=False)