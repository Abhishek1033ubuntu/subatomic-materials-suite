"""
Sub-Atomic Materials Suite - 06_portable_power_framework
Module B: Safety, Shielding & Containment Engine
"""

import numpy as np


class SafetyContainmentEngine:
    # Mass Attenuation Coefficients mu/rho (cm^2/g) at 1 MeV
    ATTENUATION_COEFFS = {
        "Tungsten": 0.066,
        "Lead": 0.071,
        "Tantalum": 0.064,
        "Borated_Polyethylene": 0.082,
        "Steel": 0.059
    }

    # Material Densities (g/cm^3)
    DENSITIES = {
        "Tungsten": 19.3,
        "Lead": 11.34,
        "Tantalum": 16.69,
        "Borated_Polyethylene": 0.95,
        "Steel": 7.85
    }

    def __init__(self):
        pass

    def calculate_radiation_attenuation(
        self,
        initial_dose_rate_mSv_h: float,
        shield_material: str,
        thickness_cm: float
    ) -> dict:
        """
        Calculates transmitted dose rate I(x) = I_0 * exp(-mu * x)
        through multilayer containment shielding.
        """
        mu_over_rho = self.ATTENUATION_COEFFS.get(shield_material, 0.066)
        density = self.DENSITIES.get(shield_material, 19.3)
        
        linear_attenuation_mu = mu_over_rho * density  # cm^-1
        
        transmitted_dose = initial_dose_rate_mSv_h * np.exp(-linear_attenuation_mu * thickness_cm)
        attenuation_factor = initial_dose_rate_mSv_h / transmitted_dose if transmitted_dose > 0 else np.inf

        # Regulatory threshold check (e.g., 0.002 mSv/h public contact limit)
        is_safe_for_public = transmitted_dose <= 0.002

        return {
            "initial_dose_mSv_h": initial_dose_rate_mSv_h,
            "transmitted_dose_mSv_h": float(transmitted_dose),
            "shield_material": shield_material,
            "shield_thickness_cm": thickness_cm,
            "attenuation_factor": round(float(attenuation_factor), 2),
            "public_safety_compliant": is_safe_for_public
        }

    def calculate_required_shield_thickness(
        self,
        initial_dose_rate_mSv_h: float,
        target_dose_rate_mSv_h: float = 0.002,
        shield_material: str = "Tungsten"
    ) -> float:
        """Calculates exact shield thickness (cm) required to meet regulatory safety limits."""
        if initial_dose_rate_mSv_h <= target_dose_rate_mSv_h:
            return 0.0

        mu_over_rho = self.ATTENUATION_COEFFS.get(shield_material, 0.066)
        density = self.DENSITIES.get(shield_material, 19.3)
        linear_attenuation_mu = mu_over_rho * density

        thickness_cm = np.log(initial_dose_rate_mSv_h / target_dose_rate_mSv_h) / linear_attenuation_mu
        return float(thickness_cm)


if __name__ == "__main__":
    safety = SafetyContainmentEngine()
    print("=== Module B: Safety & Containment Engine Test ===")
    
    # Test: Attenuation of 500 mSv/h source using 5 cm of Tungsten
    att = safety.calculate_radiation_attenuation(500.0, "Tungsten", 5.0)
    print(f"Transmitted Dose: {att['transmitted_dose_mSv_h']:.6f} mSv/h | Compliant: {att['public_safety_compliant']}")
    
    # Calculate required lead shield thickness for 1000 mSv/h source
    req_cm = safety.calculate_required_shield_thickness(1000.0, 0.002, "Lead")
    print(f"Required Lead Thickness for Safety: {req_cm:.2f} cm")
