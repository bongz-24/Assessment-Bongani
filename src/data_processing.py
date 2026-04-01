import pandas as pd

# =========================
# LOAD DATA
# =========================

medicine = pd.read_csv("../data/medicine_data.csv")
lab = pd.read_csv("../data/lab_data.txt", sep="\t")

print("Medicine Data:")
print(medicine.head())

print("\nLab Data:")
print(lab.head())

# =========================
# CLEANING
# =========================

# Standardise column names
medicine.columns = medicine.columns.str.strip().str.lower().str.replace(" ", "_")
lab.columns = lab.columns.str.strip().str.lower().str.replace(" ", "_")

# Convert dates
medicine['date_of_birth'] = pd.to_datetime(medicine['date_of_birth'])
medicine['dispensing_date'] = pd.to_datetime(medicine['dispensing_date'])

lab['date_of_birth'] = pd.to_datetime(lab['date_of_birth'])
lab['lab_test_date'] = pd.to_datetime(lab['lab_test_date'])

# Clean sex
def clean_sex(x):
    if str(x).lower().startswith('m'):
        return 'M'
    elif str(x).lower().startswith('f'):
        return 'F'
    else:
        return None

medicine['sex'] = medicine['sex'].apply(clean_sex)
lab['sex'] = lab['sex'].apply(clean_sex)

# =========================
# AGGREGATION
# =========================

# Medicine aggregation
medicine_agg = medicine.groupby('patient_id').agg(
    sex=('sex', 'first'),
    date_of_birth=('date_of_birth', 'first'),
    last_dispensing_date=('dispensing_date', 'max'),
    num_dispensed=('dispensing_date', 'count')
).reset_index()

print("\nMedicine Aggregated:")
print(medicine_agg.head())

# Lab aggregation (latest test)
lab_sorted = lab.sort_values('lab_test_date')

lab_agg = lab_sorted.groupby('patient_id').agg(
    hba1c_test_date=('lab_test_date', 'last'),
    hba1c_result=('lab_test_result', 'last')
).reset_index()

print("\nLab Aggregated:")
print(lab_agg.head())

# =========================
# MERGE
# =========================

df = pd.merge(medicine_agg, lab_agg, on='patient_id', how='left')

# =========================
# FEATURE ENGINEERING
# =========================

# Age
today = pd.to_datetime("today")
df['age'] = ((today - df['date_of_birth']).dt.days / 365).astype(int)

# Age groups
def age_group(age):
    if age < 30:
        return "<30"
    elif age < 40:
        return "30-39"
    elif age < 50:
        return "40-49"
    elif age < 60:
        return "50-59"
    else:
        return "60+"

df['age_group'] = df['age'].apply(age_group)

# Medication category
def classify_meds(group):
    meds = set(group['medication_name'].str.lower())

    has_insulin = any("insulin" in m for m in meds)
    has_metformin = any("metformin" in m for m in meds)

    if has_insulin and has_metformin:
        return "Insulin and Metformin"
    elif has_insulin:
        return "Insulin only"
    elif has_metformin:
        return "Metformin only"
    else:
        return "No drugs"

med_category = medicine.groupby('patient_id').apply(classify_meds).reset_index(name='med_category')

df = pd.merge(df, med_category, on='patient_id', how='left')

# Follow-up flag
def follow_up(row):
    if pd.isna(row['hba1c_result']):
        return 1
    elif row['hba1c_result'] >= 8:
        return 1
    elif row['med_category'] == "No drugs":
        return 1
    else:
        return 0

df['follow_up_flag'] = df.apply(follow_up, axis=1)

# =========================
# FINAL DATASET
# =========================

final_df = df[[
    'patient_id',
    'sex',
    'age_group',
    'med_category',
    'last_dispensing_date',
    'num_dispensed',
    'hba1c_test_date',
    'hba1c_result',
    'follow_up_flag'
]]

print("\nFinal Dataset:")
print(final_df.head())

# =========================
# SAVE OUTPUT
# =========================

final_df.to_csv("../output/final_dataset.csv", index=False)

print("\nSaved to ../output/final_dataset.csv")


import matplotlib.pyplot as plt

import matplotlib.pyplot as plt


# VISUALISATION


insulin_df = final_df[final_df['med_category'] == "Insulin only"]


viz_data = insulin_df.groupby(['age_group', 'sex']).size().unstack(fill_value=0)

print("\nVisualisation Data:")
print(viz_data)


ax = viz_data.plot(kind='bar')

plt.title("Distribution of Male vs Female Across Age Groups (Insulin Only)")
plt.xlabel("Age Group")
plt.ylabel("Number of Patients")
plt.xticks(rotation=0)
plt.legend(title="Sex")


for container in ax.containers:
    ax.bar_label(container)

plt.tight_layout()
plt.savefig("../output/insulin_distribution.png")
plt.show()

