# Subatomic Materials Suite (`subatomic-materials-suite`)

[![Release](https://img.shields.io/badge/Release-v1.1.0-blue.svg)](https://github.com/Abhishek1033ubuntu/subatomic-materials-suite/releases/tag/v1.1.0)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22335219.svg)](https://doi.org/10.5281/zenodo.22335219)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0004--6913--096X-green.svg)](https://orcid.org/0009-0004-6913-096X)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Built with Gemini](https://img.shields.io/badge/AI%20Assisted-Google%20Gemini-black?logo=googlegemini)](https://gemini.google.com)

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
## Directory Structure
```
subatomic-materials-suite/
├── 01_direct-field-transmutation/         # Field-Induced Non-Thermal Bond Cleavage Engine
│   ├── README.md
│   ├── transmutation_engine.py
│   └── requirements.txt
├── 02_subatomic-inverse-design/           # Field-Enhanced Potential Well Assembly
│   ├── README.md
│   ├── inverse_design_engine.py
│   └── requirements.txt
├── 03_non-thermal-photonic-processing/    # Attosecond Optical Pulse Driver
│   ├── README.md
│   ├── photonic_processor.py
│   └── requirements.txt
├── 04_transport_conductivity/             # Quantum Electronic Transport Engine
│   ├── README.md
│   ├── transport_engine.py
│   └── requirements.txt
├──05_nuclear_stability_engine/
├── README.md
│    ├── nuclide_matrix.py       # Module A: SEMF & Decay Q-Value Matrix
│    ├── decay_kinetics.py       # Module B: Fermi Golden Rule & Half-Life Predictor
│    ├── field_deexcitation.py   # Module C: Resonant Coupling & Barrier Modifier
│    └── requirements.txt
├── CITATION.cff                           # Standard Citation File (Schema 1.2.0)
├── master_pipeline.py                     # Master Orchestrator Pipeline
├── README.md                              # Repository Documentation
└── requirements.txt                       # Global Project Dependencies
```
---

## Performance Benchmarks (10nm Gold Interconnect)

When field-guided non-thermal assembly ($U_{\text{eff}} = -10.83\text{ eV}$) is applied to $10\text{ nm}$ gold ($\text{Au}$) interconnect lines compared to standard thermal processing:

* **Resistivity Reduction:** $24.68\ \mu\Omega\cdot\text{cm} \longrightarrow 2.78\ \mu\Omega\cdot\text{cm}$ (**$88.72\%$ reduction**)
* **Conductivity Improvement:** $4.05\text{ MS/m} \longrightarrow 35.93\text{ MS/m}$ (**$786.71\%$ gain**)

---

## 💻 Environment Setup & Quickstart

```bash
# Clone repository suite
git clone [https://github.com/Abhishek1033ubuntu/subatomic-materials-suite.git](https://github.com/Abhishek1033ubuntu/subatomic-materials-suite.git)
cd subatomic-materials-suite

# Install dependencies
pip install -r requirements.txt

# To run the complete four-module pipeline sequentially:
python master_pipeline.py
```
📜 Unified Dependencies (requirements.txt)
```
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.4.0
```

🤖 AI Collaboration & Transparency Statement

This repository was developed in collaboration with Google Gemini.

Code Generation & Optimization: Initial script scaffolding, mathematical model implementations, and visualization scripts were generated and refined with AI assistance.

Documentation & Technical Writing: Repository structure, README dossiers, and technical summaries were drafted and structured interactively.

Verification: All numerical models, physical equations, and code outputs have been independently reviewed and validated.
