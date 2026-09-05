"""
Sub-Atomic Materials Suite - 05_nuclear_stability_engine
Module B: Fermi Golden Rule & Half-Life Predictor
"""

import numpy as np
from scipy.integrate import quad


class DecayKineticsPredictor:
    # Physical Constants
    HBAR = 1.054571817e-34    # J*s
    C = 299792458.0           # m/s
    ME = 9.1093837015e-31     # kg
    ME_MEV = 0.51099895       # MeV
    G_FERMI = 1.1663787e-5    # GeV^-2
    G_FERMI_SI = 1.43584e-62  # J * m^3

    def __init__(self):
        pass

    def Fermi_phase_space_integral(self, q_value_mev: float) -> float:
        """
        Computes relativistic Fermi phase-space factor f(Z, Q) for beta decay.
        Integrates dimensionless momentum spectrum p^2 * (q - e)^2.
        """
        if q_value_mev <= 0:
            return 0.0

        q_dimensionless = q_value_mev / self.ME_MEV

        def integrand(p):
            e = np.sqrt(p**2 + 1.0)
            if q_dimensionless + 1.0 - e < 0:
                return 0.0
            return p**2 * ((q_dimensionless + 1.0) - e)**2

        p_max = np.sqrt(max(0.0, (q_dimensionless + 1.0)**2 - 1.0))
        result, _ = quad(integrand, 0.0, p_max)
        return float(result)

    def calculate_beta_decay_rate(self, q_value_mev: float, matrix_element_sq: float = 1.0) -> dict:
        """
        Calculates beta decay transition probability W (1/s) and partial half-life t_1/2 (s)
        via Fermi's Golden Rule and phase-space integration.
        """
        if q_value_mev <= 0:
            return {"transition_rate_W_s1": 0.0, "half_life_seconds": np.inf, "status": "Stable to Beta Decay"}

        f_factor = self.Fermi_phase_space_integral(q_value_mev)
        
        # Approximate decay constant lambda = C_beta * f * |M|^2
        c_beta = 1.1e-4  # Empirical beta-scale factor
        decay_constant_lambda = c_beta * f_factor * matrix_element_sq
        
        if decay_constant_lambda > 0:
            half_life_s = np.log(2.0) / decay_constant_lambda
        else:
            half_life_s = np.inf

        return {
            "q_value_MeV": q_value_mev,
            "phase_space_f_factor": round(f_factor, 4),
            "transition_rate_W_s1": float(decay_constant_lambda),
            "half_life_seconds": float(half_life_s),
            "status": "Beta Unstable"
        }

    def evaluate_ionization_ec_suppression(self, q_ec_mev: float, charge_state: int, z_total: int) -> dict:
        """
        Evaluates the suppression of Electron Capture (EC) decay rate under extreme ionization.
        When charge_state == z_total (fully stripped bare nucleus), EC rate drops to zero.
        """
        if q_ec_mev <= 0:
            return {"ec_rate_relative": 0.0, "status": "EC Q-value negative"}

        orbital_electrons = z_total - charge_state
        fractional_k_shell_occupancy = min(1.0, max(0.0, orbital_electrons / 2.0))
        
        relative_ec_rate = fractional_k_shell_occupancy

        if relative_ec_rate == 0.0:
            state_desc = "EC Completely Suppressed (Bare Nucleus)"
        elif relative_ec_rate < 1.0:
            state_desc = f"EC Rate Suppressed to {relative_ec_rate*100:.1f}%"
        else:
            state_desc = "Normal Unsuppressed EC Decay"

        return {
            "charge_state": f"+{charge_state}",
            "orbital_electrons_remaining": orbital_electrons,
            "relative_ec_rate": relative_ec_rate,
            "status": state_desc
        }


if __name__ == "__main__":
    predictor = DecayKineticsPredictor()
    print("=== Module B: Decay Kinetics & Rate Predictor Test ===")
    
    # Test 1: Beta decay kinetics for Q = 2.5 MeV
    res_beta = predictor.calculate_beta_decay_rate(q_value_mev=2.5)
    print(f"Beta Decay (Q=2.5 MeV) | f-factor: {res_beta['phase_space_f_factor']} | Half-life: {res_beta['half_life_seconds']:.2f} s")

    # Test 2: EC Suppression for Bare Iron Nucleus (Z=26)
    res_ec = predictor.evaluate_ionization_ec_suppression(q_ec_mev=1.5, charge_state=26, z_total=26)
    print(f"EC Suppression (Bare Fe-56) | Relative Rate: {res_ec['relative_ec_rate']} | Status: {res_ec['status']}")
