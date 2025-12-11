import pandas as pd

# Define Rules based on Medical Thresholds & Logic
# Columns: RuleID, Cond1, Op1, Val1, Cond2, Op2, Val2, Result_Attr, Result_Val
rules_data = [
    # --- LEVEL 1: Abstraction (Numbers -> Concepts) ---
    ["R1", "chol", ">", 240, "None", "None", "None", "chol_status", "High"],
    ["R2", "chol", "<=", 240, "None", "None", "None", "chol_status", "Normal"],
    
    ["R3", "trestbps", ">", 140, "None", "None", "None", "bp_status", "High"],
    ["R4", "trestbps", "<=", 140, "None", "None", "None", "bp_status", "Normal"],
    
    ["R5", "age", ">", 55, "None", "None", "None", "age_group", "Senior"],
    ["R6", "age", "<=", 55, "None", "None", "None", "age_group", "Adult"],

    # --- LEVEL 2: Chaining (Risk Assessment) ---
    # High Chol + High BP = High Risk
    ["R7", "chol_status", "==", "High", "bp_status", "==", "High", "risk_factor", "High"],
    # Senior + High BP = High Risk
    ["R8", "age_group", "==", "Senior", "bp_status", "==", "High", "risk_factor", "High"],
    # Exercise Angina (exang=1) + Oldpeak > 1.5 = Cardiac Stress
    ["R9", "exang", "==", 1, "oldpeak", ">", 1.5, "cardiac_stress", "Severe"],

    # --- LEVEL 3: Final Diagnosis (Target) ---
    # 1. High Risk + Chest Pain (cp > 0) -> Disease (1)
    ["R10", "risk_factor", "==", "High", "cp", ">", 0, "target", 1],
    
    # 2. Severe Cardiac Stress -> Disease (1)
    ["R11", "cardiac_stress", "==", "Severe", "None", "None", "None", "target", 1],
    
    # 3. Major Vessels Colored (ca > 0) is a strong indicator -> Disease (1)
    ["R12", "ca", ">", 0, "None", "None", "None", "target", 1],
    
    # 4. If Normal BP AND Normal Chol -> Healthy (0)
    ["R13", "bp_status", "==", "Normal", "chol_status", "==", "Normal", "target", 0]
]

columns = ["RuleID", "Cond1", "Op1", "Val1", "Cond2", "Op2", "Val2", "Result_Attr", "Result_Val"]
df_rules = pd.DataFrame(rules_data, columns=columns)

# Save to CSV
df_rules.to_csv("heart_rules.csv", index=False)
print("heart_rules.csv created successfully!")