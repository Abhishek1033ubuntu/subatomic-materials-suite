"""
Sub-Atomic Materials Suite - Master Pipeline Orchestrator
Integrates Attosecond Photonic Processing, Direct Field Transmutation,
Subatomic Inverse Design, and Transport Conductivity Engine into a single execution flow.
"""

import sys
import os

# Ensure sub-modules can be imported relative to root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from photonic_processing.photonic_processor import PhotonicProcessor
from direct_field_transmutation.transmutation_engine import TransmutationEngine
from inverse_design.inverse_design_engine import InverseDesignEngine
from transport_conductivity.transport_engine import TransportConductivityEngine


def run_master_pipeline():
    print("==================================================================")
    print("      SUB-ATOMIC MATERIALS SUITE: MASTER ORCHESTRATION PIPELINE   ")
    print("==================================================================\n")

    # Step 1: Photonic Processor Drive
    print("[1/4] Executing Attosecond Photonic Processor Driver...")
    photonic = PhotonicProcessor(pulse_duration_as=80, peak_field_gvm=10.0)
    _ = photonic.generate_pulse()
    print(
        f"      -> Generated {photonic.pulse_duration_as} as pulse with peak field E0 = {photonic.peak_field_gvm} GV/m.\n"
    )

    # Step 2: Direct Field Transmutation (Non-Thermal Bond Cleavage)
    print("[2/4] Executing Direct Field Transmutation Engine...")
    transmutation = TransmutationEngine(
        applied_field_gvm=photonic.peak_field_gvm
    )
    fe_yield = transmutation.calculate_bond_cleavage_yield("Fe-O")
    si_yield = transmutation.calculate_bond_cleavage_yield("Si-O")
    print(f"      -> Fe-O Bond Cleavage Yield : {fe_yield:.2f}%")
    print(f"      -> Si-O Bond Cleavage Yield : {si_yield:.2f}%\n")

    # Step 3: Subatomic Inverse Design (Potential Well Deepening)
    print("[3/4] Executing Subatomic Inverse Design Engine...")
    inverse = InverseDesignEngine(peak_field_gvm=photonic.peak_field_gvm)
    u_eff = inverse.compute_effective_potential(base_depth_ev=-4.35)
    print("      -> Base Potential Well Depth      : -4.35 eV")
    print(f"      -> Field-Guided Effective Depth   : {u_eff:.2f} eV\n")

    # Step 4: Transport Conductivity Engine
    print(
        "[4/4] Executing Transport Conductivity Engine (10nm Au Interconnect)..."
    )
    transport = TransportConductivityEngine(material="Au", linewidth_nm=10.0)
    results = transport.run_comparison(u_eff_ev=u_eff)

    print("==================================================================")
    print("                      FINAL SIMULATION RESULTS                    ")
    print("==================================================================")
    print(
        f" Target Material                : {results['material']} ({results['linewidth_nm']} nm Interconnect)"
    )
    print(
        f" Standard Thermal Resistivity   : {results['thermal_mode']['resistivity_uohm_cm']:.3f} uOhm-cm"
    )
    print(
        f" Field-Guided Resistivity        : {results['field_guided_mode']['resistivity_uohm_cm']:.3f} uOhm-cm"
    )
    print(
        f" Thermal Conductivity           : {results['thermal_mode']['conductivity_MS_m']:.2f} MS/m"
    )
    print(
        f" Field-Guided Conductivity       : {results['field_guided_mode']['conductivity_MS_m']:.2f} MS/m"
    )
    print(" ----------------------------------------------------------------")
    print(
        f" Net Resistivity Reduction      : {results['metrics']['resistivity_reduction_pct']:.2f} %"
    )
    print(
        f" Net Conductivity Gain          : {results['metrics']['conductivity_gain_pct']:.2f} %"
    )
    print(
        "==================================================================\n"
    )


if __name__ == "__main__":
    run_master_pipeline()
