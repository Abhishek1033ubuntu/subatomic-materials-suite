# 05_nuclear_stability_engine

## Overview
The `05_nuclear_stability_engine` module provides computational methods for evaluating nuclear binding energies, ground-state stability, and spontaneous decay pathways for synthesized or field-mutated isotopes.

## Theoretical Models
1. **Semi-Empirical Mass Formula (SEMF / Weizsäcker Formula):**
   $$B(Z, A) = a_v A - a_s A^{2/3} - a_c \frac{Z(Z-1)}{A^{1/3}} - a_a \frac{(A - 2Z)^2}{A} + \delta(Z, A)$$
2. **Decay $Q$-Value Kinetics:**
   Evaluates spontaneous thresholds for $\alpha$-decay, $\beta^-$-decay, $\beta^+$-decay, and Electron Capture (EC).

## Usage
Execute the nuclide matrix evaluator directly:
```bash
python 05_nuclear_stability_engine/nuclide_matrix.py
---

### Step 3: Update Root `README.md`

Replace your root **`README.md`** with the updated version below. It includes the **Gemini Development Partner** badge alongside Zenodo and ORCID metadata.

```markdown
# Subatomic Materials Suite (`subatomic-materials-suite`)

[![Release](https://img.shields.io/badge/Release-v1.1.0-blue.svg)](https://github.com/Abhishek1033ubuntu/subatomic-materials-suite/releases/tag/v1.1.0)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0004--6913--096X-green.svg)](https://orcid.org/0009-0004-6913-096X)
[![Gemini AI Partner](https://img.shields.io/badge/Development%20Partner-Gemini%202.5-8E7CC3?logo=google-gemini&logoColor=white)](https://gemini.google.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An integrated High-Performance Computing (HPC) simulation framework for field-guided atomic assembly, quantum transport modeling, and subatomic/nuclear state engineering.

---

## Suite Architecture

The suite consists of 5 modular simulation engines:

1. **`01_direct-field-transmutation`**: Models non-thermal bond cleavage using intense electric field vectors ($E_0 \ge 4.0\text{--}6.3\text{ GV/m}$).
2. **`02_subatomic-inverse-design`**: Simulates field-assisted potential well deepening ($U_{\text{eff}} = -10.83\text{ eV}$) for defect-free atomic alignment.
3. **`03_non-thermal-photonic-processing`**: Attosecond photonic driver ($80\text{ as}$, $10.0\text{ GV/m}$) for non-thermal lattice excitation.
4. **`04_transport_conductivity`**: Mayadas-Shatzkes and Fuchs-Sondheimer quantum transport model for sub-10nm metallic interconnects.
5. **`05_nuclear_stability_engine`**: Semi-Empirical Mass Formula (SEMF) evaluator for nuclide binding energy, valley of beta-stability, and decay $Q$-values.

---

## Validated Benchmarks (10 nm Gold Interconnect)

| Metric | Conventional Standard | Suite Field-Guided Target | Improvement |
| :--- | :--- | :--- | :--- |
| **Resistivity ($\rho$)** | $24.68\ \mu\Omega\cdot\text{cm}$ | $2.78\ \mu\Omega\cdot\text{cm}$ | **88.72% Reduction** |
| **Conductivity ($\sigma$)** | $4.05\text{ MS/m}$ | $35.93\text{ MS/m}$ | **786.71% Increase** |
| **Surface Specularity ($p$)** | $0.20$ | $0.85$ | Specular electron reflection |
| **Grain Diameter ($d$)** | $10.0\text{ nm}$ | $100.0\text{ nm}$ | Near single-crystal grain boundaries |

---

## Quick Start

### Installation
```bash
git clone [https://github.com/Abhishek1033ubuntu/subatomic-materials-suite.git](https://github.com/Abhishek1033ubuntu/subatomic-materials-suite.git)
cd subatomic-materials-suite
pip install -r requirements.txt
Run Full Pipeline
Bash
python master_pipeline.py
Run Nuclear Stability Evaluator
Bash
python 05_nuclear_stability_engine/nuclide_matrix.py
```

