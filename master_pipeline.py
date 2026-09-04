# ==============================================================================
# SUB-ATOMIC MANUFACTURING MASTER ORCHESTRATION PIPELINE
# Integrates Repositories:
# 1. non-thermal-photonic-processing (Attosecond Field Drive)
# 2. direct-field-transmutation (Selective Ionization & Extraction)
# 3. subatomic-inverse-design (Field-Guided Alloy Assembly)
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------
# GLOBAL CONSTANTS & PHYSICAL PARAMETERS
# ------------------------------------------------------------------------------
C = 2.99792458e8               # Speed of light (m/s)
EPS0 = 8.8541878128e-12        # Vacuum permittivity (F/m)
EV_TO_J = 1.602176634e-19      # eV to Joules conversion

# Ore Binding Thresholds (GV/m)
THRESHOLD_FE_O = 4.0
THRESHOLD_SI_O = 6.3

# Pair Potential Parameters (Lennard-Jones + Optical Field Coupling)
R_EQ_TIC = 2.13                # Angstroms
E_NATURAL_TIC = 4.35           # eV
ALPHA_TIC = 5.2e-30            # Polarizability (m^3)

# ------------------------------------------------------------------------------
# MODULE 1: ATTOSECOND PHOTONIC DRIVE SIMULATION (Repo 3)
# ------------------------------------------------------------------------------
def generate_photonic_drive(t_fs, peak_field_GVm=10.0, pulse_duration_as=80, cep_rad=0.0):
    tau_s = pulse_duration_as * 1e-18
    t_s = t_fs * 1e-15
    omega0 = 2 * np.pi * C / (800e-9)
    
    envelope = np.exp(-4 * np.log(2) * (t_s / tau_s)**2)
    E_field = peak_field_GVm * envelope * np.cos(omega0 * t_s + cep_rad)
    
    # Calculate Instantaneous Intensity (W/cm^2)
    intensity_W_cm2 = (0.5 * EPS0 * C * (E_field * 1e9)**2) / 1e4
    return E_field, envelope * peak_field_GVm, intensity_W_cm2

# ------------------------------------------------------------------------------
# MODULE 2: DIRECT FIELD TRANSMUTATION & EXTRACTION (Repo 1)
# ------------------------------------------------------------------------------
def calculate_ore_ionisation(E_peak_GVm):
    yield_fe = 100.0 / (1.0 + np.exp(-3.0 * (E_peak_GVm - THRESHOLD_FE_O)))
    yield_si = 100.0 / (1.0 + np.exp(-3.0 * (E_peak_GVm - THRESHOLD_SI_O)))
    return yield_fe, yield_si

# ------------------------------------------------------------------------------
# MODULE 3: SUB-ATOMIC INVERSE DESIGN & TRAP DEEPENING (Repo 2)
# ------------------------------------------------------------------------------
def calculate_effective_potential(r_ang, E_field_GVm):
    # Standard Lennard-Jones 12-6 Potential
    U_lj = 4 * E_NATURAL_TIC * ((R_EQ_TIC / r_ang)**12 - (R_EQ_TIC / r_ang)**6) - E_NATURAL_TIC
    
    # Optical Gradient Field Coupling
    E_Vm = E_field_GVm * 1e9
    U_field_J = 0.5 * ALPHA_TIC * (E_Vm**2) * np.exp(-((r_ang - R_EQ_TIC) / 0.4)**2)
    U_field_eV = U_field_J / EV_TO_J
    
    return U_lj - U_field_eV

# ------------------------------------------------------------------------------
# MASTER PIPELINE EXECUTION
# ------------------------------------------------------------------------------
def run_master_pipeline():
    print("=" * 70)
    print("      EXECUTING MASTER SUB-ATOMIC MANUFACTURING PIPELINE")
    print("=" * 70)
    
    t_fs = np.linspace(-1.0, 1.0, 1000)
    peak_field = 10.0  # GV/m
    
    # Step 1: Generate Photonic Pulse
    E_field, envelope, intensity = generate_photonic_drive(t_fs, peak_field_GVm=peak_field)
    max_intensity = np.max(intensity)
    print(f"\n[STEP 1: PHOTONIC DRIVE generated]")
    print(f"  ► Peak Field Strength:     {peak_field:.2f} GV/m")
    print(f"  ► Max Optical Intensity:   {max_intensity:.3e} W/cm²")
    
    # Step 2: Evaluate Non-Thermal Extraction Yields
    yield_fe, yield_si = calculate_ore_ionisation(peak_field)
    print(f"\n[STEP 2: FIELD TRANSMUTATION evaluated]")
    print(f"  ► Fe Extraction Yield:     {yield_fe:.2f}% (Threshold: {THRESHOLD_FE_O} GV/m)")
    print(f"  ► Si Extraction Yield:     {yield_si:.2f}% (Threshold: {THRESHOLD_SI_O} GV/m)")
    
    # Step 3: Evaluate Assembly Potential Trap
    r_axis = np.linspace(1.5, 5.0, 500)
    U_eff = calculate_effective_potential(r_axis, peak_field)
    min_trap_eV = np.min(U_eff)
    print(f"\n[STEP 3: INVERSE DESIGN ASSEMBLY evaluated]")
    print(f"  ► Natural Ti-C Well Depth: -{E_NATURAL_TIC:.2f} eV")
    print(f"  ► Field-Guided Trap Depth: {min_trap_eV:.2f} eV (Field: {peak_field} GV/m)")
    print(f"  ► Effective Well Enhancement: {abs(min_trap_eV)/E_NATURAL_TIC:.2f}x")
    
    # Render Master Multi-Panel Visualization
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    
    # Subplot 1: Laser Pulse Drive
    axs[0].plot(t_fs, E_field, 'navy', lw=1.5, label='E-Field (10 GV/m)')
    axs[0].plot(t_fs, envelope, 'r--', alpha=0.7, label='Envelope (80 as)')
    axs[0].set_title("1. Attosecond Photonic Processing")
    axs[0].set_xlabel("Time (fs)")
    axs[0].set_ylabel("Electric Field (GV/m)")
    axs[0].grid(True, alpha=0.3)
    axs[0].legend(loc='upper right')
    
    # Subplot 2: Selective Ore Ionization
    e_range = np.linspace(0, 10, 200)
    y_fe, y_si = calculate_ore_ionisation(e_range)
    axs[1].plot(e_range, y_fe, 'b-', lw=2, label='Fe-O Stripping')
    axs[1].plot(e_range, y_si, 'g-', lw=2, label='Si-O Stripping')
    axs[1].axvline(peak_field, color='red', linestyle=':', label='Operating Field (10 GV/m)')
    axs[1].set_title("2. Non-Thermal Ore Extraction")
    axs[1].set_xlabel("Field Strength (GV/m)")
    axs[1].set_ylabel("Ionization Yield (%)")
    axs[1].grid(True, alpha=0.3)
    axs[1].legend(loc='lower right')
    
    # Subplot 3: Potential Well Trapping
    axs[2].plot(r_axis, calculate_effective_potential(r_axis, 0.0), 'b--', label='Unassisted (0 GV/m)')
    axs[2].plot(r_axis, U_eff, 'r-', lw=2, label=f'Field Trap ({peak_field} GV/m)')
    axs[2].set_title("3. Field-Guided Assembly Trap")
    axs[2].set_xlabel("Interatomic Distance (Å)")
    axs[2].set_ylabel("Effective Potential Energy (eV)")
    axs[2].grid(True, alpha=0.3)
    axs[2].legend(loc='upper right')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_master_pipeline()
