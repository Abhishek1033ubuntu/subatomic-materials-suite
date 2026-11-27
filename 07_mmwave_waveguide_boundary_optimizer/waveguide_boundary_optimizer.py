"""
Module 07: Millimeter-Wave Waveguide Boundary & PIM Optimizer (>30 GHz)
Repository: subatomic-materials-suite (v1.4.0)
Author: Abhishek Singh
ORCID: https://orcid.org/0009-0004-6913-096X
GitHub: https://github.com/Abhishek1033ubuntu
Copyright (c) 2026 Abhishek Singh. All rights reserved.

Description:
    Multi-physics boundary-condition screening and optimization model for
    hollow rectangular millimeter-wave waveguides (WR-28 to WR-10, 30-110 GHz).
    Evaluates:
      1. Cascaded transmission-line surface impedance Z_s(f) for graded
         Cu / TaN / Ag / ultrathin-Au wall coatings.
      2. Huray snowball surface-roughness attenuation factor K_SR(f) where
         RMS surface roughness R_q approaches electromagnetic skin depth delta.
      3. Non-linear third-order Passive Intermodulation (IM3) power from
         ferromagnetic trace impurities (chi_m) and metal-oxide-metal (MOM)
         tunneling barrier height (Phi_B) at flange interfaces.
"""

from dataclasses import dataclass
import numpy as np

MU_0 = 4.0 * np.pi * 1e-7  # Vacuum permeability (H/m)
EPS_0 = 8.8541878128e-12   # Vacuum permittivity (F/m)
C_0 = 299792458.0          # Speed of light in vacuum (m/s)
ETA_0 = np.sqrt(MU_0 / EPS_0)


@dataclass
class CoatingLayer:
    """Physical and electronic transport parameters for a waveguide wall layer."""
    name: str
    thickness_m: float          # Layer thickness (m); np.inf for bulk substrate
    conductivity_s_m: float     # Bulk DC/RF electrical conductivity (S/m)
    rel_permeability: float     # Relative magnetic permeability mu_r (1.0 = non-magnetic)
    mag_susceptibility: float   # Volume magnetic susceptibility chi_m
    oxide_barrier_ev: float     # Native surface oxide tunneling barrier (eV); 0.0 = noble


@dataclass
class WaveguideGeometry:
    """Standard rectangular waveguide dimensions (TE10 dominant mode)."""
    band_name: str
    a_m: float  # Broad wall width (m)
    b_m: float  # Narrow wall height (m)


def skin_depth(freq_hz: np.ndarray, sigma: float, mu_r: float = 1.0) -> np.ndarray:
    """Compute electromagnetic skin depth delta = sqrt(2 / (omega * mu * sigma))."""
    omega = 2.0 * np.pi * freq_hz
    return np.sqrt(2.0 / (omega * MU_0 * mu_r * sigma))


def multilayer_surface_impedance(
    freq_hz: np.ndarray, layers_outer_to_inner: list[CoatingLayer]
) -> np.ndarray:
    """
    Compute effective surface impedance Z_s (Ohms/sq) looking into a stratified
    conductor stack using cascaded transmission-line impedance transformation.
    layers_outer_to_inner[0] is the innermost vacuum-facing wall surface;
    layers_outer_to_inner[-1] is the bulk structural substrate.
    """
    omega = 2.0 * np.pi * freq_hz
    bulk = layers_outer_to_inner[-1]
    z_load = np.sqrt((1j * omega * MU_0 * bulk.rel_permeability) / bulk.conductivity_s_m)

    for layer in reversed(layers_outer_to_inner[:-1]):
        mu = MU_0 * layer.rel_permeability
        gamma = np.sqrt(1j * omega * mu * layer.conductivity_s_m)
        z_char = np.sqrt((1j * omega * mu) / layer.conductivity_s_m)
        tanh_gd = np.tanh(gamma * layer.thickness_m)
        z_load = z_char * (z_load + z_char * tanh_gd) / (z_char + z_load * tanh_gd)

    return z_load


def huray_roughness_factor(
    freq_hz: np.ndarray,
    rq_m: float,
    sigma_top: float,
    mu_r_top: float = 1.0,
    nodule_radius_m: float = 60e-9,
    matte_area_ratio: float = 0.35,
) -> np.ndarray:
    """
    Calculate Huray snowball surface-roughness loss multiplier K_SR >= 1.0.
    Scales excess conductor attenuation when RMS roughness R_q is comparable
    to millimeter-wave skin depth delta.
    """
    delta = skin_depth(freq_hz, sigma_top, mu_r_top)
    # Effective stacked sphere count N_s / A_flat scaled from RMS roughness R_q
    n_spheres_per_unit = (rq_m / nodule_radius_m) ** 2 * 1.5
    sphere_term = (n_spheres_per_unit * 4.0 * np.pi * (nodule_radius_m ** 2)) / (
        1.0 + (delta / nodule_radius_m) + 0.5 * (delta / nodule_radius_m) ** 2
    )
    return 1.0 + 1.5 * matte_area_ratio * sphere_term


def te10_conductor_attenuation_db_m(
    freq_hz: np.ndarray,
    wg: WaveguideGeometry,
    r_s_eff: np.ndarray,
) -> np.ndarray:
    """
    Compute TE10 dominant-mode conductor attenuation alpha_c (dB/m) in a hollow
    rectangular waveguide of width a and height b.
    """
    f_c = C_0 / (2.0 * wg.a_m)
    if np.any(freq_hz <= f_c):
        raise ValueError(f"Operating frequency must exceed TE10 cutoff {f_c / 1e9:.2f} GHz.")

    ratio = f_c / freq_hz
    numerator = r_s_eff * (1.0 + (2.0 * wg.b_m / wg.a_m) * (ratio ** 2))
    denominator = wg.b_m * ETA_0 * np.sqrt(1.0 - ratio ** 2)
    alpha_np_m = numerator / denominator
    return alpha_np_m * 8.685889638  # Convert Np/m to dB/m


def estimate_im3_pim_dbc(
    freq_hz: np.ndarray,
    surface_layer: CoatingLayer,
    underlayer: CoatingLayer,
    rq_m: float,
    carrier_power_dbm: float = 43.0,
    flange_pressure_mpa: float = 35.0,
) -> np.ndarray:
    """
    Phenomenological IM3 Passive Intermodulation estimator (dBc) combining:
      1. Non-linear tunneling across native surface oxide barrier Phi_B (MOM junction)
      2. Ferromagnetic hysteresis non-linearity from underlayer/trace susceptibility
      3. Asperity current crowding proportional to R_q / delta
    """
    delta = skin_depth(freq_hz, surface_layer.conductivity_s_m, surface_layer.rel_permeability)
    # Skin penetration weight into underlayer (exponential decay across surface thickness)
    penetration_weight = np.exp(-2.0 * surface_layer.thickness_m / delta)

    # 1. MOM oxide tunneling non-linearity factor (suppressed by noble Au & clamping pressure)
    mom_nonlinearity = (surface_layer.oxide_barrier_ev ** 2) * (20.0 / max(flange_pressure_mpa, 1.0))

    # 2. Magnetic hysteresis contribution (dominant when Ni underlayer is present)
    mag_nonlinearity = (
        abs(surface_layer.mag_susceptibility)
        + penetration_weight * abs(underlayer.mag_susceptibility) * 1e4
    )

    # 3. Roughness current crowding multiplier
    roughness_crowding = (rq_m / delta) ** 1.5

    total_nonlinearity = np.maximum(1e-18, (mom_nonlinearity + mag_nonlinearity) * (1.0 + roughness_crowding))
    # Third-order intermodulation scales at 3x carrier power (2 dB/dB relative in dBc)
    im3_dbc = -172.0 + 2.0 * (carrier_power_dbm - 43.0) + 10.0 * np.log10(total_nonlinearity)
    return np.clip(im3_dbc, -175.0, -70.0)


def run_benchmark() -> None:
    """Compare candidate waveguide wall coatings across Ka-band (30-40 GHz)."""
    freqs = np.linspace(30e9, 40e9, 6)
    wr28 = WaveguideGeometry(band_name="WR-28 (Ka-Band)", a_m=7.112e-3, b_m=3.556e-3)

    # Candidate 1: Standard ENIG (Copper -> Ferromagnetic Ni -> Thin Au)
    enig_stack = [
        CoatingLayer("Au_flash", 50e-9, 4.10e7, 1.0, -3.4e-5, 0.0),
        CoatingLayer("Electroless_Ni", 2.0e-6, 1.43e7, 100.0, 600.0, 0.0),
        CoatingLayer("OFHC_Cu", np.inf, 5.96e7, 1.0, -9.6e-6, 0.65),
    ]

    # Candidate 2: Pure Unpassivated Silver (High conductivity, sulfide tarnish risk)
    pure_ag_stack = [
        CoatingLayer("Ag_plate", 2.5e-6, 6.30e7, 1.0, -2.4e-5, 0.42),
        CoatingLayer("OFHC_Cu", np.inf, 5.96e7, 1.0, -9.6e-6, 0.65),
    ]

    # Candidate 3: Champion Graded Stack (Cu -> TaN -> 1.8 um Ag Core -> 40 nm Au Cap)
    champion_stack = [
        CoatingLayer("Au_passivation", 40e-9, 4.10e7, 1.0, -3.4e-5, 0.0),
        CoatingLayer("Ag_core", 1.8e-6, 6.30e7, 1.0, -2.4e-5, 0.0),
        CoatingLayer("TaN_barrier", 40e-9, 0.50e7, 1.0, 1.2e-5, 0.0),
        CoatingLayer("Electropolished_Cu", np.inf, 5.96e7, 1.0, -9.6e-6, 0.0),
    ]

    configs = [
        ("Standard ENIG (Ni Underlayer)", enig_stack, 180e-9),
        ("Pure Ag Plating (Tarnished)", pure_ag_stack, 120e-9),
        ("Champion Graded Cu/TaN/Ag/Au", champion_stack, 15e-9),
    ]

    print(f"=== {wr28.band_name} Boundary & PIM Screening (30 - 40 GHz) ===")
    for label, stack, rq in configs:
        z_s = multilayer_surface_impedance(freqs, stack)
        k_sr = huray_roughness_factor(freqs, rq, stack[0].conductivity_s_m, stack[0].rel_permeability)
        r_s_eff = np.real(z_s) * k_sr
        alpha_db_m = te10_conductor_attenuation_db_m(freqs, wr28, r_s_eff)
        im3 = estimate_im3_pim_dbc(freqs, stack[0], stack[1], rq)

        print(f"\n[{label}] (RMS Roughness R_q = {rq * 1e9:.0f} nm)")
        print(f"  30 GHz -> Loss: {alpha_db_m[0]:.4f} dB/m | K_SR: {k_sr[0]:.3f} | Est. IM3: {im3[0]:.1f} dBc")
        print(f"  40 GHz -> Loss: {alpha_db_m[-1]:.4f} dB/m | K_SR: {k_sr[-1]:.3f} | Est. IM3: {im3[-1]:.1f} dBc")


if __name__ == "__main__":
    run_benchmark()
