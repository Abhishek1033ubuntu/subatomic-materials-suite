python main.py

---

#### File 2: `main.py`
Create a file named `main.py` and paste the following consolidated execution script:

```python
"""
Inverse Material Design via Sub-Atomic Vector Screening (IMD-SACS)
Repository 1: Practical Property Identification & Inverse Screening Engine
"""

import numpy as np
import pandas as pd

# Physical Constants
kB_eV = 8.617333262145e-5  # Boltzmann constant in eV/K
T_body_K = 310.15           # 37 °C Human Body Temperature

def run_inorganic_steel_synthesis(target_Tm_C=1510.0, op_temp_C=25.0):
    target_Tm_K = target_Tm_C + 273.15
    op_temp_K = op_temp_C + 273.15
    
    print("=========================================================================")
    print("    INORGANIC METALLURGY: SOIL DECONSTRUCTION & STEEL SYNTHESIS         ")
    print("=========================================================================")
    
    soil_feedstock = {
        "Fe2O3 (Iron Source)": {"Mass_Percent": 10.0, "E_sever_eV": 12.80, "Extracted_Vector": "Fe"},
        "SiO2 (Silica Matrix)": {"Mass_Percent": 60.0, "E_sever_eV": 18.50, "Extracted_Vector": "Si"},
        "Organic Carbon (Trace C)": {"Mass_Percent": 2.0, "E_sever_eV": 4.50, "Extracted_Vector": "C"}
    }
    
    df_feed = pd.DataFrame(soil_feedstock).T
    print(df_feed[["Mass_Percent", "E_sever_eV", "Extracted_Vector"]])
    
    E_coh_steel_target = 15.0 * kB_eV * target_Tm_K
    gamma_op = E_coh_steel_target / (kB_eV * op_temp_K)
    r0_steel_eff = 1.22 
    req_cohesion_factor = (E_coh_steel_target * (r0_steel_eff**2)) / 1.8
    
    print(f"\n[TARGET VECTOR SPECIFICATION]")
    print(f"  • Target Melting Point: {target_Tm_C} °C ({target_Tm_K} K)")
    print(f"  • Required Cohesive Energy (E_target): {E_coh_steel_target:.4f} eV")
    print(f"  • Operational Scaling Ratio (Gamma at 25°C): {gamma_op:.2f} (Solid Stable)")
    print(f"  • Target Combined Cohesion Factor (Z_eff * Valence): {req_cohesion_factor:.3f}")
    
    steel_variants = [
        {"Variant": "Pure Extracted Iron (Fe)", "Z_eff": 6.25, "Valence": 2.0, "r0": 1.26, "Tm_C": 1538.0},
        {"Variant": "Re-Engineered Carbon Steel (Fe-C Matrix)", "Z_eff": 6.45, "Valence": 2.5, "r0": 1.22, "Tm_C": 1510.0},
        {"Variant": "High-Strength Tool Steel (Fe-Si-C Matrix)", "Z_eff": 6.80, "Valence": 3.0, "r0": 1.20, "Tm_C": 1420.0}
    ]
    
    df_steel = pd.DataFrame(steel_variants)
    df_steel["E_coh_computed_eV"] = 1.8 * (df_steel["Z_eff"] * df_steel["Valence"]) / (df_steel["r0"]**2)
    df_steel["Gamma_25C"] = df_steel["E_coh_computed_eV"] / (kB_eV * op_temp_K)
    
    print("\n[MATCHING CANDIDATES]")
    print(df_steel[["Variant", "Z_eff", "Valence", "r0", "Tm_C", "E_coh_computed_eV", "Gamma_25C"]])
    print(f"\n[VERDICT]: Optimal match -> {df_steel.iloc[1]['Variant']} (Gamma = {df_steel.iloc[1]['Gamma_25C']:.2f})\n")

def run_bio_graft_synthesis(target_modulus_kPa=1050.0, target_degradation_days=45):
    print("=========================================================================")
    print("    BIO-ORGANIC MATRIX: ARTICULAR CARTILAGE SCAFFOLD MAPPING           ")
    print("=========================================================================")
    
    kB_T_body = kB_eV * T_body_K
    crosslink_density_moles_m3 = (target_modulus_kPa * 1000.0) / (8.314 * T_body_K)
    req_crosslink_spacing_nm = (1.0 / (crosslink_density_moles_m3 * 6.022e23))**(1/3) * 1e9
    req_E_network_eV = 15.0 * kB_T_body
    
    print(f"[BIO-TARGET VECTOR SPECIFICATION]")
    print(f"  • Target Modulus: {target_modulus_kPa} kPa")
    print(f"  • Required Network Cohesion: {req_E_network_eV:.4f} eV")
    print(f"  • Target Crosslink Density: {crosslink_density_moles_m3:.2f} mol/m³")
    print(f"  • Target Mesh Spacing: {req_crosslink_spacing_nm:.2f} nm")
    
    bio_candidates = [
        {"Scaffold": "GelMA (Gelatin Methacryloyl)", "Bonding": "H-Bond + Covalent Hybrid", "Modulus_kPa": 1050.0, "Degradation_Days": 45},
        {"Scaffold": "PEGDA Hydrogel", "Bonding": "Covalent Crosslinked Network", "Modulus_kPa": 800.0, "Degradation_Days": 90},
        {"Scaffold": "Chitosan-Alginate Matrix", "Bonding": "Ionic Electrostatic Network", "Modulus_kPa": 350.0, "Degradation_Days": 20}
    ]
    
    df_bio = pd.DataFrame(bio_candidates)
    df_bio["Gamma_bio_at_37C"] = (req_E_network_eV * (df_bio["Modulus_kPa"] / target_modulus_kPa)) / kB_T_body
    
    print("\n[MATCHING BIO-CANDIDATES]")
    print(df_bio[["Scaffold", "Bonding", "Modulus_kPa", "Degradation_Days", "Gamma_bio_at_37C"]])
    print(f"\n[VERDICT]: Optimal match -> {df_bio.iloc[0]['Scaffold']} (Gamma_bio = {df_bio.iloc[0]['Gamma_bio_at_37C']:.2f})\n")

if __name__ == "__main__":
    run_inorganic_steel_synthesis()
    run_bio_graft_synthesis()
