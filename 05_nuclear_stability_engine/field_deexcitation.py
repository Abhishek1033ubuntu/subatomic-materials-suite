"""
Sub-Atomic Materials Suite - 05_nuclear_stability_engine
Module C: Resonant Coupling & Barrier Modifier
"""

import numpy as np


class FieldDeexcitationEngine:
    # Physical Constants
    HBAR_EV_S = 6.582119569e-16  # eV*s
    C_MS = 299792458.0           # m/s
    E0_SCHWINGER = 1.32e18       # Schwinger QED limit (V/m)

    def __init__(self):
        pass

    def calculate_resonant_absorption_cross_section(
        self, photon_energy_ev: float, resonance_energy_ev: float, gamma_rad_ev: float, gamma_total_ev: float
    ) -> float:
        """
        Calculates nuclear resonant absorption cross-section sigma_res (m^2)
        using the Breit-Wigner single-level formula.
        """
        wavelength_m = (2.0 * np.pi * self.HBAR_EV_S * self.C_MS) / photon_energy_ev
        
        factor1 = (wavelength_m ** 2) / (2.0 * np.pi)
        numerator = gamma_rad_ev * gamma_total_ev
        denominator = (photon_energy_ev - resonance_energy_ev) ** 2 + (gamma_total_ev / 2.0) ** 2

        sigma_res = factor1 * (numerator / denominator)
        return float(sigma_res)

    def evaluate_stimulated_isomeric_depletion(
        self, laser_intensity_w_cm2: float, photon_energy_kev: float, isomeric_lifetime_s: float
    ) -> dict:
        """
        Evaluates stimulated de-excitation rate of metastable nuclear isomers
        under high-intensity X-ray Free-Electron Laser (XFEL) driving.
        """
        # Convert intensity from W/cm^2 to W/m^2
        intensity_wm2 = laser_intensity_w_cm2 * 1e4
        photon_energy_j = photon_energy_kev * 1000.0 * 1.60218e-19

        # Photon flux density phi (photons / m^2 * s)
        photon_flux = intensity_wm2 / photon_energy_j

        # Approximate resonant cross-section in barn (1 barn = 1e-28 m^2)
        sigma_approx_m2 = 1e-24  # 10,000 barns resonance peak

        # Stimulated transition rate W_stim = sigma * phi
        w_stimulated = sigma_approx_m2 * photon_flux
        w_spontaneous = 1.0 / isomeric_lifetime_s if isomeric_lifetime_s > 0 else 0.0

        acceleration_factor = (w_stimulated + w_spontaneous) / w_spontaneous if w_spontaneous > 0 else 1.0

        return {
            "laser_intensity_W_cm2": laser_intensity_w_cm2,
            "photon_flux_photons_m2_s": f"{photon_flux:.3e}",
            "stimulated_rate_s1": f"{w_stimulated:.3e}",
            "spontaneous_rate_s1": f"{w_spontaneous:.3e}",
            "deexcitation_acceleration_factor": round(float(acceleration_factor), 2)
        }

    def calculate_alpha_gamow_barrier_modification(
        self, z_daughter: int, q_alpha_mev: float, applied_field_v_m: float
    ) -> dict:
        """
        Calculates modification of Gamow quantum tunneling factor for alpha decay
        under external high-gradient optical field potentials.
        """
        if q_alpha_mev <= 0:
            return {"gamow_factor_unperturbed": 0.0, "modified_half_life_ratio": 1.0, "status": "Alpha decay energetically forbidden"}

        # Unperturbed Gamow Factor G
        # G ~ 2 * pi * alpha * Z_d * sqrt(m_alpha * c^2 / (2 * Q_alpha))
        alpha_const = 1.0 / 137.035999
        m_alpha_mev = 3727.379
        
        gamow_unperturbed = 2.0 * np.pi * alpha_const * z_daughter * np.sqrt(m_alpha_mev / (2.0 * q_alpha_mev))

        # Field perturbation factor scaling relative to Schwinger limit
        field_ratio = applied_field_v_m / self.E0_SCHWINGER
        delta_gamow = gamow_unperturbed * (field_ratio * 0.01)

        gamow_modified = gamow_unperturbed - delta_gamow
        half_life_ratio = np.exp(-2.0 * delta_gamow)

        return {
            "applied_field_V_m": f"{applied_field_v_m:.2e}",
            "gamow_factor_unperturbed": round(float(gamow_unperturbed), 4),
            "gamow_factor_modified": round(float(gamow_modified), 4),
            "half_life_modification_ratio": float(half_life_ratio),
            "status": "Gamow Barrier Evaluated"
        }


if __name__ == "__main__":
    engine = FieldDeexcitationEngine()
    print("=== Module C: Resonant Coupling & Barrier Modifier Test ===")

    # Test 1: Isomeric depletion under 10^16 W/cm^2 XFEL drive
    res_iso = engine.evaluate_stimulated_isomeric_depletion(
        laser_intensity_w_cm2=1e16, photon_energy_kev=14.4, isomeric_lifetime_s=3600.0
    )
    print(f"Isomer Depletion Acceleration Factor: {res_iso['deexcitation_acceleration_factor']}x")

    # Test 2: Alpha Gamow barrier modification at 10^10 V/m
    res_gamow = engine.calculate_alpha_gamow_barrier_modification(
        z_daughter=77, q_alpha_mev=3.0, applied_field_v_m=1.0e10
    )
    print(f"Alpha Gamow Unperturbed: {res_gamow['gamow_factor_unperturbed']} | Half-Life Ratio: {res_gamow['half_life_modification_ratio']}")
