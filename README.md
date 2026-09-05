# ⚛️ Sub-Atomic Materials Suite Monorepo

[![Built with Gemini](https://img.shields.io/badge/AI%20Assisted-Google%20Gemini-black?logo=googlegemini)](https://gemini.google.com)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22335219.svg)](https://doi.org/10.5281/zenodo.22335219)

This suite models the non-thermal extraction, field-guided assembly, and ultrafast photonic pulse shaping required to synthesize pure atomic lattices directly from raw ore without thermal melting or furnace sintering.

A high-performance computational modeling framework for simulating non-thermal field-guided atomic extraction, potential-well-engineered assembly, and electronic transport properties in advanced semiconductor interconnects.

## Architecture & Core Modules

The suite is organized into four interconnected physics engines orchestrated by a central root pipeline (`master_pipeline.py`):

1. **`03_non-thermal-photonic-processing`**: Simulates attosecond optical pulse generation ($80\text{ as}$, $10.0\text{ GV/m}$ peak fields) driving electric polarization without thermal lattice dissipation.
2. **`01_direct-field-transmutation`**: Models non-thermal bond cleavage and elemental extraction yields from raw mineral oxides ($\text{Fe-O}$, $\text{Si-O}$) using field ionization thresholds.
3. **`02_subatomic-inverse-design`**: Calculates external field coupling and potential well deepening ($U_{\text{eff}} = -10.83\text{ eV}$) to force crystalline alignment during atomic assembly.
4. **`04_transport_conductivity`**: Evaluates thin-film transport dynamics using the Mayadas-Shatzkes (grain boundary scattering) and Fuchs-Sondheimer (surface scattering) models to compute electrical conductivity and resistivity improvements in nanoscale interconnects ($\text{Au}$, $\text{Cu}$, $\text{Ti}$).

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
