# 06_portable_power_framework

## Overview
The `06_portable_power_framework` module provides computational design, scaling, and safety verification models for portable nuclear power generation. It enables the conversion of subatomic decay and triggered isomeric de-excitation into electrical power across micro ($mW$) to industrial ($MW$) scales.

## Architecture
```
06_portable_power_framework/
├── README.md
├── multiscale_modules.py     # Module A: Multiscale Power Engine (mW to MW)
├── safety_containment.py     # Module B: Safety, Shielding & Containment Engine
├── rtg_integration.py        # Module C: Solid-State Betavoltaic & RTG Integration
├── governance_protocols.py   # Module D: IAEA Safeguards & Non-Proliferation Matrix
└── requirements.txt
```
## Physics & Engineering Foundations

### 1. Solid-State Betavoltaic Conversion
Electrons emitted during decay create electron-hole pairs (EHPs) in wide-bandgap semiconductors ($\text{Diamond}$, $\text{4H-SiC}$). The internal power generation is governed by:
$$P_{\text{elec}} = A \cdot (E_{\text{avg}} \cdot q) \cdot \left(\frac{E_g}{\epsilon_{\text{pair}}}\right) \cdot \eta_{\text{coll}}$$

### 2. Multilayer Containment Shielding
Attenuates gammas and X-rays using the Beer-Lambert exponential relation:
$$I(x) = I_0 e^{-\mu x}$$
Where $\mu = (\mu/\rho) \cdot \rho$ is the linear attenuation coefficient of high-$Z$ shielding materials ($\text{Tungsten}$, $\text{Lead}$).

## Quick Start
```bash
python 06_portable_power_framework/multiscale_modules.py
python 06_portable_power_framework/safety_containment.py
```
