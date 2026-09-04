# ⚡ Non-Thermal Photonic Processing Engine (`non-thermal-photonic-processing`)

[![Built with Gemini](https://img.shields.io/badge/AI%20Assisted-Google%20Gemini-black?logo=googlegemini)](https://gemini.google.com)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22305317.svg)](https://doi.org/10.5281/zenodo.22305317)

## Overview
The **Non-Thermal Photonic Processing Engine** models attosecond pulse shaping, Carrier-Envelope Phase (CEP) locking, and optical intensity profiles required to physicalize electric field strengths from $0.1\text{--}10.0\text{ GV/m}$ in real time.

---
> [!IMPORTANT]
> **Repository Migration Notice**  
> This standalone module has been integrated into the unified **[Sub-Atomic Materials Suite Monorepo](https://github.com/Abhishek1033ubuntu/subatomic-materials-suite/tree/main/03_non-thermal-photonic-processing)**.  
> Future updates, multi-physics integration, and execution scripts are maintained in the new repository.

---

## 📐 Mathematical Formulation

The electric field temporal profile $E(t)$ and instantaneous intensity profile $I(t)$ are modeled as:

$$E(t) = E_0 \cdot \exp\left( -4 \ln(2) \left[\frac{t}{\tau}\right]^2 \right) \cdot \cos(\omega_0 t + \phi_{\text{CEP}})$$

$$I(t) = \frac{1}{2} \varepsilon_0 c |E(t)|^2$$

Where:
* $E_0$: Peak electric field strength ($10.0\text{ GV/m}$)
* $\tau$: Pulse duration FWHM ($80\text{ attoseconds}$)
* $\omega_0$: Central drive frequency ($800\text{ nm}$ Ti:Sapphire drive)
* $\phi_{\text{CEP}}$: Carrier-Envelope Phase offset ($0$ to $\pi/2\text{ rad}$)

---

## 📊 Pulse & Intensity Analysis

![Attosecond Laser Pulse Shaping](assets/pulse_shaping_output.png)

### Key Performance Metrics
* **Peak Electric Field ($E_{\text{peak}}$):** $10.0\text{ GV/m}$
* **Peak Intensity ($I_{\text{peak}}$):** $1.327 \times 10^{13}\text{ W/cm}^2$
* **Pulse Duration ($\tau_{\text{FWHM}}$):** $80\text{ attoseconds}$ ($0.08\text{ fs}$)
* **Thermal Response Time ($\tau_{\text{phonon}}$):** $> 100\text{ fs}$ (Ensures zero-thermal heating, $\Delta T = 0.000\text{ K}$)

🤖 AI Collaboration & Transparency Statement
This repository was developed in collaboration with Google Gemini.

Code Generation & Optimization: Initial script scaffolding, mathematical model implementations, and visualization scripts were generated and refined with AI assistance.

Documentation & Technical Writing: Repository structure, README dossiers, and technical summaries were drafted and structured interactively.

Verification: All numerical models, physical equations, and code outputs have been independently reviewed and validated.
