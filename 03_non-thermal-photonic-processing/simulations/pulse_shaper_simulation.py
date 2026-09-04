# ==============================================================================
# CONCEPT 3: NON-THERMAL PHOTONIC PROCESSING ENGINE
# File: pulse_shaper_simulation.py
# Environment: Google Colab / Python 3
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt

# Physical Constants
C = 2.99792458e8             # Speed of light (m/s)
EPS0 = 8.8541878128e-12      # Vacuum permittivity (F/m)
H_BAR = 1.054571817e-34      # Reduced Planck constant (J·s)

class AttosecondPulseShaper:
    def __init__(self, central_wavelength_nm=800, pulse_duration_as=80):
        """
        Parameters:
        -----------
        central_wavelength_nm : float
            Central laser wavelength in nanometers (e.g., 800 nm Ti:Sapphire drive)
        pulse_duration_as : float
            Full Width at Half Maximum (FWHM) pulse duration in attoseconds
        """
        self.lambda0 = central_wavelength_nm * 1e-9  # meters
        self.omega0 = 2 * np.pi * C / self.lambda0   # Angular frequency (rad/s)
        self.tau = pulse_duration_as * 1e-18        # seconds

    def generate_shaped_pulse(self, time_axis_fs, peak_field_GVm=10.0, cep_rad=0.0, chirp_factor=0.0):
        """
        Generates a chirped, CEP-stabilized electric field pulse envelope.
        E(t) = E0 * exp(-2*ln(2)*(t/tau)^2) * cos(omega0*t + chirp*t^2 + cep)
        """
        time_axis_s = time_axis_fs * 1e-15
        
        # Gaussian envelope
        envelope = np.exp(-4 * np.log(2) * (time_axis_s / self.tau)**2)
        
        # Phase profile with chirp and CEP
        phase = self.omega0 * time_axis_s + chirp_factor * (time_axis_s**2) + cep_rad
        
        # Electric field in GV/m
        E_field = peak_field_GVm * envelope * np.cos(phase)
        
        # Calculate instantaneous intensity profile (W/cm^2)
        # I = 0.5 * eps0 * c * |E|^2
        E_field_Vm = E_field * 1e9
        intensity_W_m2 = 0.5 * EPS0 * C * (E_field_Vm**2)
        intensity_W_cm2 = intensity_W_m2 / 1e4
        
        return E_field, envelope * peak_field_GVm, intensity_W_cm2

def run_photonic_processing_sim():
    # Time axis: -1.0 to +1.0 femtoseconds (1000 attoseconds total window)
    t_fs = np.linspace(-1.0, 1.0, 2000)
    
    shaper = AttosecondPulseShaper(central_wavelength_nm=800, pulse_duration_as=80)
    
    # Simulate 3 Carrier-Envelope Phase (CEP) offsets: 0, pi/2, pi
    E_cep0, env, I_peak = shaper.generate_shaped_pulse(t_fs, peak_field_GVm=10.0, cep_rad=0.0)
    E_cep_pi2, _, _ = shaper.generate_shaped_pulse(t_fs, peak_field_GVm=10.0, cep_rad=np.pi/2)
    
    fig, axs = plt.subplots(1, 2, figsize=(15, 5.5))
    
    # Subplot 1: Electric Field Pulse Profile & Envelope
    axs[0].plot(t_fs, env, 'r--', label='Field Envelope (10 GV/m Peak)', alpha=0.7)
    axs[0].plot(t_fs, -env, 'r--', alpha=0.7)
    axs[0].plot(t_fs, E_cep0, color='navy', lw=1.5, label='E-Field (CEP = 0 rad)')
    axs[0].plot(t_fs, E_cep_pi2, color='darkgreen', lw=1.2, label='E-Field (CEP = π/2 rad)', alpha=0.6)
    
    axs[0].set_title("Attosecond Laser Pulse Shaping & CEP Control")
    axs[0].set_xlabel("Time (femtoseconds)")
    axs[0].set_ylabel("Electric Field Strength (GV/m)")
    axs[0].set_xlim(-0.5, 0.5)
    axs[0].grid(True, alpha=0.3)
    axs[0].legend(loc='upper right')
    
    # Subplot 2: Instantaneous Optical Intensity Profile
    axs[1].plot(t_fs, I_peak, color='crimson', lw=2.0, label='Instantaneous Intensity')
    axs[1].set_title("Peak Optical Intensity Profile (Non-Thermal Regime)")
    axs[1].set_xlabel("Time (femtoseconds)")
    axs[1].set_ylabel("Intensity (W/cm²)")
    axs[1].set_xlim(-0.5, 0.5)
    axs[1].grid(True, alpha=0.3)
    axs[1].legend(loc='upper right')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_photonic_processing_sim()
