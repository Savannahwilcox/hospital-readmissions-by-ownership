import pandas as pd

readmissions = pd.read_csv("data/raw/FY_2026_Hospital_Readmissions_Reduction_Program_Hospital.csv",
                           dtype={"Facility ID": str})
hospitals = pd.read_csv("data/raw/Hospital_General_Information.csv", dtype={"Facility ID": str})

print("READMISSIONS FILE")
print(readmissions.shape)
print(readmissions.columns.tolist())
print(readmissions.head(3).to_string())

print()
print("ROWS PER HOSPITAL")
print("Unique hospitals:", readmissions["Facility ID"].nunique())

print()
print("CONDITIONS MEASURED")
print(readmissions["Measure Name"].value_counts())

print()
print("EXCESS READMISSION RATIO")
print(readmissions["Excess Readmission Ratio"].describe())

print()
print("MISSING RATIOS BY CONDITION")
print(readmissions[readmissions["Excess Readmission Ratio"].isna()]["Measure Name"].value_counts())

print()
print("OWNERSHIP TYPES")
print(hospitals["Hospital Ownership"].value_counts())
