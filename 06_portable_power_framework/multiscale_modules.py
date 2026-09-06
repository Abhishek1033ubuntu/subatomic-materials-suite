"""
Sub-Atomic Materials Suite - 06_portable_power_framework
Module A: Multiscale Power Engine (mW to MW)
"""

import numpy as np


class MultiscalePowerEngine:
    # Physical Constants
    E_CHARGE = 1.602176634e-19    # Coulombs
    AVOGADRO = 6.02214076e23       # mol^-1
    MEV_TO_JOULE = 1.60218e-13    # Joules per MeV
    JOULE_TO_KWH = 2.77778e-7     # kWh per Joule

    # Converter Material Bandgaps (eV)
    BANDGAPS = {
        "Diamond": 5.47,
        "SiC_4H": 3.26,
        "GaN": 3.40,
        "Silicon": 1.12
    }

    def __init__(self):
        pass

    def calculate_isotope_activity(self, mass_grams: float, molar_mass_g: float, half_life_years: float) -> float:
        """Calculates decay activity A (Bq = decays/sec) for a given isotope mass."""
        if half_life_years <= 0 or mass_grams <= 0:
            return 0.0
        
        half_life_seconds = half_life_years * 365.25 * 86400.0
        decay_constant = np.log(2.0) / half_life_seconds
        num_atoms = (mass_grams / molar_mass_g) * self.AVOGADRO
        
        activity_bq = decay_constant * num_atoms
        return float(activity_bq)

    def calculate_betavoltaic_power(
        self,
        activity_bq: float,
        average_decay_energy_mev: float,
        semiconductor: str = "Diamond",
        collection_efficiency: float = 0.85
    ) -> dict:
        """
        Calculates direct electrical power output and efficiency for solid-state
        betavoltaic/alphavoltaic conversion using wide-bandgap semiconductors.
        """
        bandgap_ev = self.BANDGAPS.get(semiconductor, 3.26)
        
        # Total raw decay power (Watts)
        p_decay_watts = activity_bq * (average_decay_energy_mev * self.MEV_TO_JOULE)
        
        # Average energy to create an Electron-Hole Pair (EHP): epsilon ~ 3 * E_g
        e_pair_ev = 3.0 * bandgap_ev
        
        # Theoretical internal quantum efficiency limit
        eta_internal_max = (bandgap_ev / e_pair_ev)  # ~33.3%
        
        # Net electrical output power
        p_electrical_watts = p_decay_watts * eta_internal_max * collection_efficiency
        net_efficiency_percent = (p_electrical_watts / p_decay_watts * 100.0) if p_decay_watts > 0 else 0.0

        return {
            "raw_decay_power_W": round(float(p_decay_watts), 6),
            "electrical_power_W": round(float(p_electrical_watts), 6),
            "semiconductor_used": semiconductor,
            "internal_conversion_efficiency_%": round(float(net_efficiency_percent), 2)
        }

    def scale_power_module(
        self,
        target_power_watts: float,
        specific_energy_mev: float,
        molar_mass_g: float,
        half_life_years: float,
        conversion_mode: str = "Betavoltaic"
    ) -> dict:
        """
        Scales fuel requirements, mass, and volume to achieve a target power output (mW to MW).
        """
        if conversion_mode == "Betavoltaic":
            efficiency = 0.25  # 25% net efficiency
        elif conversion_mode == "Thermoelectric":
            efficiency = 0.08  # 8% standard RTG efficiency
        else:
            efficiency = 0.40  # Triggered Isomer Dynamic Loop

        required_decay_power_w = target_power_watts / efficiency
        required_decay_power_joules_sec = required_decay_power_w

        energy_per_decay_j = specific_energy_mev * self.MEV_TO_JOULE
        required_activity_bq = required_decay_power_joules_sec / energy_per_decay_j

        half_life_seconds = half_life_years * 365.25 * 86400.0
        decay_constant = np.log(2.0) / half_life_seconds

        required_atoms = required_activity_bq / decay_constant
        required_mass_kg = (required_atoms / self.AVOGADRO) * (molar_mass_g / 1000.0)

        # Estimate energy density (kWh / kg)
        annual_energy_kwh = (target_power_watts * 8760.0) / 1000.0
        specific_energy_density_kwh_kg = annual_energy_kwh / required_mass_kg if required_mass_kg > 0 else 0.0

        if target_power_watts < 1.0:
            tier = "Micro-Scale (mW)"
        elif target_power_watts < 1000.0:
            tier = "Meso-Scale (W)"
        elif target_power_watts < 1000000.0:
            tier = "Macro-Scale (kW)"
        else:
            tier = "Industrial-Scale (MW)"

        return {
            "scale_tier": tier,
            "target_power_output_W": target_power_watts,
            "conversion_mode": conversion_mode,
            "required_fuel_mass_kg": round(float(required_mass_kg), 6),
            "annual_energy_yield_kWh": round(float(annual_energy_kwh), 2),
            "fuel_energy_density_kWh_kg": round(float(specific_energy_density_kwh_kg), 2)
        }


if __name__ == "__main__":
    engine = MultiscalePowerEngine()
    print("=== Module A: Multiscale Power Engine Test ===")
    
    # Test 1: Micro-scale Betavoltaic (e.g., Tritium or Ni-63 for sensors)
    act = engine.calculate_isotope_activity(mass_grams=0.01, molar_mass_g=63.0, half_life_years=100.1)
    bv = engine.calculate_betavoltaic_power(activity_bq=act, average_decay_energy_mev=0.017, semiconductor="Diamond")
    print(f"Micro-Scale Output: {bv['electrical_power_W']} W | Efficiency: {bv['internal_conversion_efficiency_%']}%")

    # Test 2: Macro-scale Power Scaling (100 kW module)
    macro = engine.scale_power_module(
        target_power_watts=100000.0,
        specific_energy_mev=2.5,
        molar_mass_g=180.0,
        half_life_years=10.0,
        conversion_mode="Isomeric Dynamic Loop"
    )
    print(f"Macro Scale ({macro['scale_tier']}): {macro['required_fuel_mass_kg']} kg fuel for {macro['target_power_output_W']/1000} kW")
