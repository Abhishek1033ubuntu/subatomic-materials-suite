"""
Sub-Atomic Materials Suite - 06_portable_power_framework
Module D: IAEA Safeguards & Non-Proliferation Matrix
"""

import numpy as np


class GovernanceProtocolsEngine:
    # Critical Mass Limits (kg) for Fissile Materials under IAEA Safeguards
    CRITICAL_MASS_LIMITS_KG = {
        "Pu-239": 8.0,
        "U-235": 25.0,
        "U-233": 8.0,
        "Np-237": 25.0,
        "Am-241": 34.0
    }

    def __init__(self):
        pass

    def evaluate_non_proliferation_safety(
        self,
        isotope_name: str,
        total_mass_kg: float,
        is_fissile: bool = False,
        spontaneous_fission_rate_per_g_s: float = 0.0
    ) -> dict:
        """
        Evaluates isotopic inventory against international Non-Proliferation Treaty (NPT)
        and IAEA Significant Quantity (SQ) thresholds.
        """
        threshold_kg = self.CRITICAL_MASS_LIMITS_KG.get(isotope_name, np.inf)
        fraction_of_critical_mass = total_mass_kg / threshold_kg if threshold_kg != np.inf else 0.0

        is_npt_compliant = not is_fissile or (total_mass_kg < 0.10 * threshold_kg)
        
        if not is_fissile:
            category = "Category IV / Non-Fissile Radioisotope (Civilian Approved)"
            safeguard_status = "Exempt from Critical Mass Safeguards"
        elif total_mass_kg < 0.10 * threshold_kg:
            category = "Category III / Sub-Critical Fuel Quantity"
            safeguard_status = "IAEA Low-Threshold Inspection Active"
        else:
            category = "Category I / High-Consequence Material"
            safeguard_status = "IAEA Continuous Safeguards & Tracking Required"

        return {
            "isotope": isotope_name,
            "total_mass_kg": total_mass_kg,
            "fissile_material": is_fissile,
            "critical_mass_threshold_kg": threshold_kg if threshold_kg != np.inf else "N/A (Non-Fissile)",
            "fraction_of_critical_mass": round(float(fraction_of_critical_mass), 4),
            "security_category": category,
            "safeguard_status": safeguard_status,
            "non_proliferation_compliant": is_npt_compliant
        }

    def verify_iaea_transport_compliance(
        self,
        surface_dose_mSv_h: float,
        dose_1m_mSv_h: float,
        package_mass_kg: float
    ) -> dict:
        """
        Evaluates package transport classification under IAEA Regulations for the Safe
        Transport of Radioactive Material (SSR-6).
        """
        # IAEA Transport Index (TI) based on dose rate at 1 meter (in mrem/h = mSv/h * 100)
        transport_index = dose_1m_mSv_h * 100.0

        if surface_dose_mSv_h <= 0.005 and dose_1m_mSv_h <= 0.0005:
            category = "Category I-WHITE (Excepted / Low Level)"
            label_required = "WHITE-I"
        elif surface_dose_mSv_h <= 0.50 and dose_1m_mSv_h <= 0.01:
            category = "Category II-YELLOW (Medium Level)"
            label_required = "YELLOW-II"
        elif surface_dose_mSv_h <= 2.00 and dose_1m_mSv_h <= 0.10:
            category = "Category III-YELLOW (High Level)"
            label_required = "YELLOW-III"
        else:
            category = "Exclusive Use Transport Required (Exceeds Standard Limits)"
            label_required = "SPECIAL ARRANGEMENT"

        is_transportable_standard = surface_dose_mSv_h <= 2.00 and dose_1m_mSv_h <= 0.10

        return {
            "surface_dose_mSv_h": surface_dose_mSv_h,
            "dose_at_1m_mSv_h": dose_1m_mSv_h,
            "transport_index": round(float(transport_index), 2),
            "iaea_package_category": category,
            "required_shipping_label": label_required,
            "approved_for_standard_commercial_transport": is_transportable_standard
        }


if __name__ == "__main__":
    gov = GovernanceProtocolsEngine()
    print("=== Module D: IAEA Safeguards & Non-Proliferation Matrix Test ===")

    # Test 1: Non-Proliferation check for 2.0 kg Ta-180m Isomer Source
    np_res = gov.evaluate_non_proliferation_safety("Ta-180m", total_mass_kg=2.0, is_fissile=False)
    print(f"NPT Compliance ({np_res['isotope']}): {np_res['security_category']} | Compliant: {np_res['non_proliferation_compliant']}")

    # Test 2: Transport compliance check for package (0.12 mSv/h surface, 0.003 mSv/h at 1m)
    trans = gov.verify_iaea_transport_compliance(surface_dose_mSv_h=0.12, dose_1m_mSv_h=0.003, package_mass_kg=15.0)
    print(f"IAEA Shipping Category: {trans['iaea_package_category']} | Label: {trans['required_shipping_label']}")
