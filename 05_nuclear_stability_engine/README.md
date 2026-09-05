# 05_nuclear_stability_engine

## Overview
The `05_nuclear_stability_engine` module provides computational methods for evaluating nuclear binding energy, valley-of-stability deviations, decay kinetics via Fermi's Golden Rule, and field-stimulated de-excitation/barrier modification pathways.

## Engine Structure
```
05_nuclear_stability_engine/
├── README.md
├── nuclide_matrix.py       # Module A: SEMF & Decay Q-Value Matrix
├── decay_kinetics.py       # Module B: Fermi Golden Rule & Half-Life Predictor
├── field_deexcitation.py   # Module C: Resonant Coupling & Barrier Modifier
└── requirements.txt
```
## Theoretical Models

### Module A: Ground-State Mass & Q-Value Evaluator (`nuclide_matrix.py`)
Utilizes the Semi-Empirical Mass Formula (SEMF / Weizsäcker Formula) to compute binding energy $B(Z, A)$ and $Q$-value reaction energetics:
$$B(Z, A) = a_v A - a_s A^{2/3} - a_c \frac{Z(Z-1)}{A^{1/3}} - a_a \frac{(A - 2Z)^2}{A} + \delta(Z, A)$$

### Module B: Decay Kinetics & Rate Predictor (`decay_kinetics.py`)
Computes transition rates $W$ and partial half-lives $t_{1/2}$ using Fermi's Golden Rule and phase-space density integration:
$$W = \frac{2\pi}{\hbar} |\langle \psi_f | H_{\text{perturb}} | \psi_i \rangle|^2 \rho(E_f)$$
Models bound-state $\beta^-$ decay and electron capture shutdown under fully ionized (electron-stripped) plasma environments.

### Module C: Resonant Coupling & Barrier Modifier (`field_deexcitation.py`)
Simulates coherent photonic coupling ($\text{XFEL/HHG}$) to metastable nuclear isomers via dipole/quadrupole transitions ($E1, E2, M1$), and calculates Gamow factor modification under ultra-intense laser fields ($E_0 \ge 10^{10}\text{ V/m}$).

---

## Quick Start Execution

Run the complete Module 05 verification suite:
```bash
python 05_nuclear_stability_engine/nuclide_matrix.py
python 05_nuclear_stability_engine/decay_kinetics.py
python 05_nuclear_stability_engine/field_deexcitation.py
   

## Usage
Execute the nuclide matrix evaluator directly:
```bash
python 05_nuclear_stability_engine/nuclide_matrix.py
```
---

