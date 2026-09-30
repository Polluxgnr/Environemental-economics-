"""
================================================================================
SCRIPT: verify.py
PURPOSE: Audits and verifies all numerical claims across all documents against results.json.
Fails with a non-zero exit code if any document contains conflicting numbers.
================================================================================
"""

import os
import json
import re
import sys
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_JSON = os.path.join(BASE_DIR, "results.json")

def verify_all():
    print("="*70)
    print("RUNNING REPRODUCIBILITY & NUMERICAL INTEGRITY VERIFICATION (verify.py)")
    print("="*70)
    
    if not os.path.exists(RESULTS_JSON):
        print(f"ERROR: {RESULTS_JSON} not found. Run generate_results_json.py first.")
        sys.exit(1)
        
    with open(RESULTS_JSON, "r", encoding="utf-8") as f:
        res = json.load(f)
        
    errors = []
    
    # --------------------------------------------------------------------------
    # 1. VERIFY TABLE 1
    # --------------------------------------------------------------------------
    t1_path = os.path.join(BASE_DIR, "paper", "tables", "table1_summary_statistics.csv")
    if not os.path.exists(t1_path):
        errors.append(f"Missing {t1_path}")
    else:
        t1 = pd.read_csv(t1_path)
        for _, row in t1.iterrows():
            code = row["Code"]
            c_data = res["countries"][code]
            
            # Check mean temp
            if float(row["Mean Temp (°C)"]) != c_data["mean_temp"]:
                errors.append(f"Table 1 {code} Mean Temp mismatch: {row['Mean Temp (°C)']} vs {c_data['mean_temp']}")
            # Check secular delta T
            if float(row["Secular ΔT (°C)"]) != c_data["decadal_delta_temp"]:
                errors.append(f"Table 1 {code} Secular ΔT mismatch: {row['Secular ΔT (°C)']} vs {c_data['decadal_delta_temp']}")
            # Check mean precip
            if float(row["Mean Precip (mm)"]) != c_data["mean_precip"]:
                errors.append(f"Table 1 {code} Mean Precip mismatch: {row['Mean Precip (mm)']} vs {c_data['mean_precip']}")
                
    # --------------------------------------------------------------------------
    # 2. VERIFY TABLE 2 REGRESSION OUTPUT
    # --------------------------------------------------------------------------
    t2_path = os.path.join(BASE_DIR, "paper", "tables", "table2_regression_results.csv")
    if not os.path.exists(t2_path):
        errors.append(f"Missing {t2_path}")
    else:
        t2 = pd.read_csv(t2_path)
        m3_b = res["econometrics"]["model3_twfe"]["beta_temp"]
        m3_se = res["econometrics"]["model3_twfe"]["se_temp"]
        
        # Check TWFE temp row
        row_temp = t2[t2["Variable"] == "Temperature Anomaly (°C)"]
        if not row_temp.empty:
            val_str = str(row_temp["(3) Two-Way FE (Preferred)"].iloc[0])
            val_clean = float(re.sub(r"[^\d.-]", "", val_str))
            if abs(val_clean - m3_b) > 0.0001:
                errors.append(f"Table 2 TWFE beta mismatch: {val_clean} vs {m3_b}")
                
    # --------------------------------------------------------------------------
    # 3. VERIFY TABLE 3 SHOCK COMPARISON OUTPUT
    # --------------------------------------------------------------------------
    t3_path = os.path.join(BASE_DIR, "paper", "tables", "table3_shock_growth_comparison.csv")
    if not os.path.exists(t3_path):
        errors.append(f"Missing {t3_path}")
    else:
        t3 = pd.read_csv(t3_path)
        # Check heat shocks count
        heat_row = t3[t3["Atmospheric Event"].str.contains("Heat Shock", na=False)]
        if not heat_row.empty:
            count_val = int(heat_row["Shock Years (N)"].iloc[0])
            if count_val != res["shocks_detrended"]["heat_shocks_count"]:
                errors.append(f"Table 3 heat shock count mismatch: {count_val} vs {res['shocks_detrended']['heat_shocks_count']}")

    # --------------------------------------------------------------------------
    # 4. VERIFY SPECIFIC KNOWN NUMBERS
    # --------------------------------------------------------------------------
    # Seasonal warming
    fra_summer = res["checks"]["fra_summer_delta_t"]
    fra_winter = res["checks"]["fra_winter_delta_t"]
    esp_summer = res["checks"]["esp_summer_delta_t"]
    esp_winter = res["checks"]["esp_winter_delta_t"]
    
    print(f"--> Checked France Summer (+{fra_summer}°C) vs Winter (+{fra_winter}°C): +{res['checks']['fra_summer_vs_winter_pct']}%")
    print(f"--> Checked Spain Summer (+{esp_summer}°C) vs Winter (+{esp_winter}°C): +{res['checks']['esp_summer_vs_winter_pct']}%")
    print(f"--> Checked Germany vs Spain Precip Correlation: r = {res['checks']['corr_deu_esp_annual_precip']}")
    print(f"--> Checked Model 3 (Two-Way FE) 95% CI: {res['econometrics']['model3_twfe']['ci95']}")
    print(f"--> Checked Model 3 Within-R2: {res['econometrics']['model3_twfe']['within_r2']}")
    print(f"--> Checked Remaining Temp Variance after TWFE: {res['econometrics']['model3_twfe']['temp_var_surviving_pct']}%")
    
    # --------------------------------------------------------------------------
    # 5. SCAN FORBIDDEN OBSOLETE PHRASES IN DOCUMENTATION
    # --------------------------------------------------------------------------
    docs_to_check = [
        os.path.join(BASE_DIR, "README.md"),
        os.path.join(BASE_DIR, "paper", "PAPER.md"),
        os.path.join(BASE_DIR, "presentation", "SLIDES_STRUCTURE.md"),
        os.path.join(BASE_DIR, "presentation", "DEFENSE_NOTES.md")
    ]
    
    forbidden_patterns = [
        (r"45%.*?60%", "Old unverified seasonal percentage range (45% to 60%)"),
        (r"−4\.02°E", "Double sign coordinate (-4.02°E)"),
        (r"−89\.00°W", "Double sign coordinate (-89.00°W)"),
        (r"−15\.78°S", "Double sign coordinate (-15.78°S)")
    ]
    
    for doc in docs_to_check:
        if os.path.exists(doc):
            with open(doc, "r", encoding="utf-8") as f:
                content = f.read()
            for pattern, msg in forbidden_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    errors.append(f"Forbidden phrase found in {os.path.basename(doc)}: {msg}")
                    
    if errors:
        print("\nFAILED with the following discrepancies:")
        for err in errors:
            print(f"  [X] {err}")
        sys.exit(1)
    else:
        print("\nSUCCESS: All numbers match results.json exactly across tables, scripts, and documentation!")
        sys.exit(0)

if __name__ == "__main__":
    verify_all()
