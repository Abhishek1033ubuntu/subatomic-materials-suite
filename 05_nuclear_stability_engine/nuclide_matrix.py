"""
Sub-Atomic Materials Suite - 05_nuclear_stability_engine
Module A: Initial Nuclide Stability Matrix and Decay Path Evaluator
"""

import numpy as np


class NuclideStabilityMatrix:
    # Physical Constants
    M_P = 1.00727647      # Proton mass (u)
    M_N = 1.00866491      # Neutron mass (u)
    M_E_MEV = 0.51099895  # Electron mass equivalent (MeV)
    M_ALPHA_MEV = 3727.379  # Alpha particle mass equivalent (MeV)
    AMU_TO_MEV = 931.494102  # 1 u in MeV

    # SEMF Coefficients (in MeV)
    A_V = 15.79   # Volume term
    A_S = 18.34   # Surface term
    A_C = 0.714   # Coulomb term
    A_A = 23.21   # Asymmetry term

    def __init__(self):
        pass

    def calculate_pairing_term(self, z: int, a: int) -> float:
        """Calculates pairing energy delta (MeV) based on parity."""
        n = a - z
        if z % 2 == 0 and n % 2 == 0:
            return 12.0 / np.sqrt(a)   # Even-Even (extra stability)
        elif z % 2 != 0 and n % 2 != 0:
            return -12.0 / np.sqrt(a)  # Odd-Odd (unstable)
        else:
            return 0.0                 # Odd-A

    def calculate_binding_energy(self, z: int, a: int) -> float:
        """Calculates total nuclear binding energy B(Z, A) in MeV using SEMF."""
        if a < 1 or z < 0 or z > a:
            return 0.0

        n = a - z
        coulomb = self.A_C * (z * (z - 1)) / (a ** (1.0 / 3.0))
        asymmetry = self.A_A * ((a - 2 * z) ** 2) / a
        pairing = self.calculate_pairing_term(z, a)

        b_energy = (self.A_V * a) - (self.A_S * (a ** (2.0 / 3.0))) - coulomb - asymmetry + pairing
        return max(0.0, b_energy)

    def calculate_atomic_mass(self, z: int, a: int) -> float:
        """Calculates total atomic mass M(Z, A) in atomic mass units (u)."""
        b_energy_mev = self.calculate_binding_energy(z, a)
        b_energy_u = b_energy_mev / self.AMU_TO_MEV
        total_mass_u = (z * self.M_P) + ((a - z) * self.M_N) - b_energy_u
        return total_mass_u

    def evaluate_stability(self, z: int, a: int) -> dict:
        """
        Evaluates nuclide binding energy, distance from line of stability,
        and potential Q-values for spontaneous decay modes.
        """
        n = a - z
        b_total = self.calculate_binding_energy(z, a)
        b_per_nucleon = b_total / a if a > 0 else 0.0
        m_curr = self.calculate_atomic_mass(z, a)

        # Ideal proton count for mass number A
        z_stable_ideal = a / (2.0 + (self.A_C / (2.0 * self.A_A)) * (a ** (2.0 / 3.0)))
        z_deviation = z - z_stable_ideal

        # Q-value Calculations (MeV)
        # 1. Beta-Minus Decay (Z -> Z+1)
        m_beta_minus = self.calculate_atomic_mass(z + 1, a)
        q_beta_minus = (m_curr - m_beta_minus) * self.AMU_TO_MEV

        # 2. Beta-Plus / EC Decay (Z -> Z-1)
        m_beta_plus = self.calculate_atomic_mass(z - 1, a)
        q_beta_plus = ((m_curr - m_beta_plus) * self.AMU_TO_MEV) - (2.0 * self.M_E_MEV)
        q_ec = (m_curr - m_beta_plus) * self.AMU_TO_MEV  # Electron capture threshold

        # 3. Alpha Decay (Z -> Z-2, A -> A-4)
        if a > 4 and z > 2:
            m_alpha_daughter = self.calculate_atomic_mass(z - 2, a - 4)
            q_alpha = ((m_curr - m_alpha_daughter) * self.AMU_TO_MEV) - self.M_ALPHA_MEV
        else:
            q_alpha = -999.0

        # Classify Primary Instability / Decay Mode
        if q_alpha > 0 and a > 140:
            primary_mode = "Alpha Decay (α)"
        elif q_beta_minus > 0:
            primary_mode = "Beta-Minus (β-)"
        elif q_beta_plus > 0:
            primary_mode = "Beta-Plus / EC (β+/EC)"
        elif q_ec > 0:
            primary_mode = "Electron Capture (EC Only)"
        else:
            primary_mode = "Stable / Ground-State Bound"

        return {
            "nuclide": f"Z={z}, A={a} (N={n})",
            "binding_energy_total_MeV": round(b_total, 3),
            "binding_energy_per_nucleon_MeV": round(b_per_nucleon, 3),
            "atomic_mass_u": round(m_curr, 6),
            "z_ideal_stability": round(z_stable_ideal, 2),
            "deviation_from_valley": round(z_deviation, 2),
            "q_values_MeV": {
                "Q_beta_minus": round(q_beta_minus, 3),
                "Q_beta_plus": round(q_beta_plus, 3),
                "Q_electron_capture": round(q_ec, 3),
                "Q_alpha": round(q_alpha, 3) if q_alpha != -999.0 else "N/A"
            },
            "predicted_mode": primary_mode
        }


if __name__ == "__main__":
    engine = NuclideStabilityMatrix()

    # Test Cases:
    # 1. Iron-56 (Peak nuclear binding stability)
    # 2. Gold-197 (Stable heavy nucleus)
    # 3. Carbon-14 (Unstable beta-emitter)
    test_nuclides = [(26, 56), (79, 197), (6, 14)]

    print("==========================================================================")
    print("      05_NUCLEAR_STABILITY_ENGINE: NUCLIDE MATRIX INITIALIZATION          ")
    print("==========================================================================")

    for z_val, a_val in test_nuclides:
        res = engine.evaluate_stability(z_val, a_val)
        print(f"\nTarget Nuclide        : {res['nuclide']}")
        print(f"Total Binding Energy  : {res['binding_energy_total_MeV']} MeV")
        print(f"Binding / Nucleon     : {res['binding_energy_per_nucleon_MeV']} MeV/nucleon")
        print(f"Valley Deviation      : {res['deviation_from_valley']} (Z_ideal = {res['z_ideal_stability']})")
        print(f"Predicted Mode        : {res['predicted_mode']}")
        print(f"Q-values (MeV)        : {res['q_values_MeV']}")
        print("--------------------------------------------------------------------------")
