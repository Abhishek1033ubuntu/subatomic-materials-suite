# Module 07: Millimeter-Wave Waveguide Boundary & PIM Optimizer (>30 GHz)

**Lead Author:** Abhishek Singh  
**ORCID:** https://orcid.org/0009-0004-6913-096X  
**GitHub:** https://github.com/Abhishek1033ubuntu  
**Suite Version:** `v1.4.0` (`subatomic-materials-suite`)  
**Copyright:** Copyright (c) 2026 Abhishek Singh. All rights reserved.

---

## 1. Problem Scope & Physical Motivation

In hollow rectangular millimeter-wave waveguides operating above **30 GHz** (such as WR-28 in the Ka-band from 26.5 to 40 GHz up to WR-10 in the W-band from 75 to 110 GHz), electromagnetic skin depth shrinks into the sub-micron regime. At these frequencies, three boundary mechanisms degrade signal integrity:

* **Surface-Roughness Skin Loss:** Microscopic surface asperities alter current density and increase effective conductor attenuation when RMS roughness (R<sub>q</sub>) approaches skin depth (&delta;).
* **Ferromagnetic Trace Impurities:** Magnetic contaminants or ferromagnetic underlayers (such as nickel in ENIG finishes) introduce magnetic hysteresis and non-linear B-H response under high-frequency tangential magnetic fields.
* **Non-Linear Metal-Oxide-Metal (MOM) Junctions:** Thin oxide or tarnish films at flange interfaces and micro-contacts act as non-linear tunneling or rectifying junctions, generating spurious harmonic and Passive Intermodulation (PIM) products.

---

## 2. Core Equations & Coupled Solvers

`waveguide_boundary_optimizer.py` couples four physical calculations across frequency (f):

* **Electromagnetic Skin Depth:** &delta;(f) = &radic;(2 / (&omega; &middot; &mu;<sub>0</sub> &middot; &mu;<sub>r</sub> &middot; &sigma;)), where &omega; = 2&pi;f, &mu;<sub>0</sub> = 4&pi; &times; 10<sup>-7</sup> H/m, &mu;<sub>r</sub> is relative permeability, and &sigma; is electrical conductivity (S/m).
* **Cascaded Multilayer Surface Impedance:** Computes effective wall surface impedance Z<sub>s</sub>(f) from the innermost waveguide surface through each coating layer to the bulk substrate using transmission-line impedance transformation:
  Z<sub>load</sub> = Z<sub>c</sub> &middot; (Z<sub>load</sub> + Z<sub>c</sub> tanh(&gamma;d)) / (Z<sub>c</sub> + Z<sub>load</sub> tanh(&gamma;d)), with propagation constant &gamma; = &radic;(j&omega;&mu;&sigma;) and characteristic impedance Z<sub>c</sub> = &radic;(j&omega;&mu;/&sigma;).
* **Huray Snowball Roughness Multiplier:** Scales conductor resistance by K<sub>SR</sub>(f) &ge; 1 to account for extra surface area and field concentration on asperity nodules of radius r<sub>n</sub> relative to &delta;(f).
* **TE<sub>10</sub> Conductor Attenuation & IM<sub>3</sub> Estimator:** Evaluates dominant-mode attenuation &alpha;<sub>c</sub> (dB/m) for rectangular dimensions (a &times; b) above cutoff f<sub>c</sub> = c<sub>0</sub> / (2a), and estimates third-order intermodulation (IM<sub>3</sub> in dBc) from oxide barrier height (&Phi;<sub>B</sub>), flange clamping pressure, roughness crowding (R<sub>q</sub>/&delta;), and magnetic susceptibility (&chi;<sub>m</sub>).

---

## 3. Boundary Screening Criteria & Champion Stack

Candidate wall coatings are screened against four boundary conditions above 30 GHz:

* **High Conductivity & Low Skin Loss:** Maximize &sigma; in the skin-current zone while keeping top passivation thickness thin relative to &delta;.
* **Non-Magnetic Purity:** Enforce &chi;<sub>m</sub> &le; 0 (diamagnetic or non-ferromagnetic) to eliminate magnetic hysteresis and reject ferromagnetic nickel underlayers.
* **Oxide & Tarnish Suppression:** Favor noble or oxide-free boundary surfaces to prevent non-linear MOM tunneling at flange mating faces.
* **Interfacial Grading & Planarity:** Pair low-roughness preparation (R<sub>q</sub> &lt; 20 nm) with a graded stack so fields do not penetrate into rough or oxidized substrate interfaces.

**Selected Graded Champion Stack:** Electropolished Cu substrate &rarr; TaN diffusion barrier (40 nm) &rarr; high-conductivity Ag core (1.8 &mu;m) &rarr; ultrathin Au passivation cap (40 nm).

---

## 4. Benchmark Output Summary (WR-28, 30–40 GHz)

Running `python waveguide_boundary_optimizer.py` across 30–40 GHz (43 dBm carrier reference, 35 MPa flange clamping pressure) illustrates the trade-offs among candidate finishes:

| Configuration | R<sub>q</sub> | 30 GHz Loss (dB/m) | 30 GHz IM<sub>3</sub> (dBc) | 40 GHz Loss (dB/m) | 40 GHz IM<sub>3</sub> (dBc) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Standard ENIG (Ni Underlayer)** | 180 nm | Higher due to Ni &mu;<sub>r</sub> &amp; roughness | Degraded by ferromagnetic Ni | Higher due to Ni &amp; roughness | Degraded by ferromagnetic Ni |
| **Pure Ag Plating (Tarnished)** | 120 nm | Low core loss, elevated K<sub>SR</sub> | Elevated from oxide/tarnish | Low core loss, elevated K<sub>SR</sub> | Elevated from oxide/tarnish |
| **Champion Graded Cu/TaN/Ag/Au** | 15 nm | Lowest smooth-wall attenuation | Strongly suppressed (no Ni/oxide) | Lowest smooth-wall attenuation | Strongly suppressed (no Ni/oxide) |

*(Run `waveguide_boundary_optimizer.py` directly to print exact numerical values for each frequency step and adjust layer thicknesses, roughness R<sub>q</sub>, or waveguide band dimensions.)*
