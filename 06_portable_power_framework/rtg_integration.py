"""
Sub-Atomic Materials Suite - 06_portable_power_framework
Module C: Solid-State & Hybrid RTG Generator Integration
"""

import numpy as np


class RTGIntegrationEngine:
    # Thermal Conductivity of Thermoelectric Elements (W/m*K)
    THERMAL_CONDUCTIVITY = {
        "Bi2Te3": 1.5,       # Bismuth Telluride (Low Temp < 500 K)
        "SiGe": 4.5,         # Silicon-Germanium (High Temp > 1000 K)
        "PbTe": 2.1          # Lead Telluride (Mid Temp 500-900 K)
    }

    # Seebeck Coefficients (uV/K)
    SEEBECK_COEFF = {
        "Bi2Te3": 200.0,
        "SiGe": 300.0,
        "PbTe": 250.0
    }

    def __init__(self):
        pass

    def calculate_thermoelectric_efficiency(
        self,
        t_hot_k: float,
        t_cold_k: float,
        material: str = "SiGe"
    ) -> dict:
        """
        Calculates maximum theoretical thermoelectric efficiency (Carnot + ZT figure of merit)
        for RTG thermal conversion.
        """
        if t_hot_k <= t_cold_k:
            return {"efficiency_%": 0.0, "status": "Temperature gradient non-existent or reversed"}

        # Carnot Efficiency Limit
        eta_carnot = (t_hot_k - t_cold_k) / t_hot_k
        
        # Average Figure of Merit ZT approximation for radioisotope materials
        zt_avg = 0.8  # Typical value for SiGe/PbTe space-grade thermocouples
        
        # Exact thermoelectric converter efficiency equation
        gamma = np.sqrt(1.0 + zt_avg)
        eta_thermoelectric = eta_carnot * ((gamma - 1.0) / (gamma + (t_cold_k / t_hot_k)))

        return {
            "t_hot_K": t_hot_k,
            "t_cold_K": t_cold_k,
            "delta_T_K": t_hot_k - t_cold_k,
            "carnot_limit_%": round(float(eta_carnot * 100.0), 2),
            "net_thermoelectric_efficiency_%": round(float(eta_thermoelectric * 100.0), 2),
            "material": material
        }

    def model_hybrid_generator_stack(
        self,
        thermal_input_power_w: float,
        beta_particle_flux_watts: float,
        t_hot_k: float = 1100.0,
        t_cold_k: float = 300.0
    ) -> dict:
        """
        Models a dual-stage hybrid power generator combining direct solid-state betavoltaics
        with a secondary thermoelectric heat recovery loop.
        """
        # Stage 1: Direct Betavoltaic Conversion (25% efficiency on beta flux)
        eta_beta = 0.25
        p_elec_stage1 = beta_particle_flux_watts * eta_beta
        unconverted_beta_heat = beta_particle_flux_watts * (1.0 - eta_beta)

        # Stage 2: Thermoelectric Conversion on Total Residual Heat
        total_thermal_budget = thermal_input_power_w + unconverted_beta_heat
        te_res = self.calculate_thermoelectric_efficiency(t_hot_k, t_cold_k, material="SiGe")
        eta_te = te_res["net_thermoelectric_efficiency_%"] / 100.0
        
        p_elec_stage2 = total_thermal_budget * eta_te
        total_electrical_output_w = p_elec_stage1 + p_elec_stage2

        total_input_energy_w = thermal_input_power_w + beta_particle_flux_watts
        overall_hybrid_efficiency = (total_electrical_output_w / total_input_energy_w * 100.0) if total_input_energy_w > 0 else 0.0

        return {
            "stage_1_betavoltaic_electrical_W": round(float(p_elec_stage1), 2),
            "stage_2_thermoelectric_electrical_W": round(float(p_elec_stage2), 2),
            "total_hybrid_electrical_output_W": round(float(total_electrical_output_w), 2),
            "waste_heat_to_dissipate_W": round(float(total_input_energy_w - total_electrical_output_w), 2),
            "overall_system_efficiency_%": round(float(overall_hybrid_efficiency), 2)
        }


if __name__ == "__main__":
    rtg = RTGIntegrationEngine()
    print("=== Module C: Solid-State & Hybrid Generator Integration Test ===")

    # Test 1: Thermoelectric efficiency for standard RTG (1100 K to 300 K)
    te = rtg.calculate_thermoelectric_efficiency(t_hot_k=1100.0, t_cold_k=300.0, material="SiGe")
    print(f"TEG Net Efficiency: {te['net_thermoelectric_efficiency_%']}% (Carnot Limit: {te['carnot_limit_%']}%)")

    # Test 2: Hybrid Dual-Stage Generator (1000 W Thermal + 200 W Beta Flux)
    hyb = rtg.model_hybrid_generator_stack(thermal_input_power_w=1000.0, beta_particle_flux_watts=200.0)
    print(f"Hybrid Generator Output: {hyb['total_hybrid_electrical_output_W']} W | System Efficiency: {hyb['overall_system_efficiency_%']}%")
