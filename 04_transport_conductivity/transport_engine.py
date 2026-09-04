import numpy as np

# Material constants database (at 300 K)
MATERIAL_DB = {
    "Au": {
        "rho_0": 2.24e-8,       # Bulk resistivity in Ohm-m (2.24 uOhm-cm)
        "lambda_0": 37.7e-9,    # Bulk electron mean free path in meters (37.7 nm)
        "name": "Gold"
    },
    "Cu": {
        "rho_0": 1.68e-8,       # Bulk resistivity in Ohm-m (1.68 uOhm-cm)
        "lambda_0": 39.0e-9,    # Bulk electron mean free path in meters (39.0 nm)
        "name": "Copper"
    },
    "Ti": {
        "rho_0": 42.0e-8,       # Bulk resistivity in Ohm-m (42.0 uOhm-cm)
        "lambda_0": 2.5e-9,     # Bulk electron mean free path in meters (2.5 nm)
        "name": "Titanium"
    }
}

class TransportConductivityEngine:
    def __init__(self, material="Au", linewidth_nm=10.0):
        """
        Initializes the Transport Engine.
        :param material: Target metal species ('Au', 'Cu', or 'Ti')
        :param linewidth_nm: Interconnect line width in nanometers (default: 10 nm)
        """
        if material not in MATERIAL_DB:
            raise ValueError(f"Material {material} not found in database.")
        
        self.material = material
        self.props = MATERIAL_DB[material]
        self.w = linewidth_nm * 1e-9  # Convert nm to meters

    def calculate_mayadas_shatzkes(self, grain_size_m, reflection_coeff):
        """
        Calculates resistivity multiplier due to grain boundary scattering.
        """
        lambda_0 = self.props["lambda_0"]
        if grain_size_m <= 0:
            return 1.0
        
        alpha = (lambda_0 / grain_size_m) * (reflection_coeff / (1.0 - reflection_coeff))
        if alpha < 1e-4:
            return 1.0
        
        # Mayadas-Shatzkes polynomial approximation
        ms_term = 1.0 - 1.5 * alpha + 3.0 * (alpha**2) - 3.0 * (alpha**3) * np.log(1.0 + 1.0 / alpha)
        return 1.0 / ms_term

    def calculate_fuchs_sondheimer(self, specularity_p):
        """
        Calculates resistivity multiplier due to surface boundary scattering.
        """
        lambda_0 = self.props["lambda_0"]
        fs_multiplier = 1.0 + (3.0 / 8.0) * (1.0 - specularity_p) * (lambda_0 / self.w)
        return fs_multiplier

    def evaluate_transport(self, u_eff_ev=-10.83, is_field_guided=True):
        """
        Evaluates physical transport properties for Thermal vs. Field-Guided processing.
        """
        if is_field_guided:
            # Field-guided: Deep well depth enhances grain size and surface smoothness
            enhancement_factor = abs(u_eff_ev) / 4.35  # Relative to base thermal well depth
            grain_size_m = 100.0e-9 * enhancement_factor  # ~249 nm grain size
            reflection_coeff = 0.10                       # Low grain boundary scattering
            specularity_p = 0.85                          # Smooth specular surfaces
        else:
            # Standard thermal processing parameters
            grain_size_m = 10.0e-9                        # Small 10 nm grains
            reflection_coeff = 0.45                       # High grain reflection
            specularity_p = 0.20                          # Diffuse surface scattering

        ms_ratio = self.calculate_mayadas_shatzkes(grain_size_m, reflection_coeff)
        fs_ratio = self.calculate_fuchs_sondheimer(specularity_p)

        # Matthiessen rule combination
        total_rho = self.props["rho_0"] * ms_ratio * fs_ratio
        total_conductivity_MSm = (1.0 / total_rho) / 1e6  # Convert to MS/m
        rho_uohm_cm = total_rho * 1e8                     # Convert to uOhm-cm
        line_resistance_ohm_nm = total_rho / (self.w**2) / 1e9 # Resistance per nm length

        return {
            "processing_mode": "Field-Guided Non-Thermal" if is_field_guided else "Standard Thermal",
            "grain_size_nm": grain_size_m * 1e9,
            "specularity_p": specularity_p,
            "reflection_r": reflection_coeff,
            "resistivity_uohm_cm": rho_uohm_cm,
            "conductivity_MS_m": total_conductivity_MSm,
            "line_resistance_ohm_per_nm": line_resistance_ohm_nm
        }

    def run_comparison(self, u_eff_ev=-10.83):
        """
        Runs comparative transport evaluation between thermal and field-guided modes.
        """
        thermal_res = self.evaluate_transport(u_eff_ev, is_field_guided=False)
        field_res = self.evaluate_transport(u_eff_ev, is_field_guided=True)

        resistivity_reduction_pct = (1.0 - (field_res["resistivity_uohm_cm"] / thermal_res["resistivity_uohm_cm"])) * 100.0
        conductivity_gain_pct = ((field_res["conductivity_MS_m"] / thermal_res["conductivity_MS_m"]) - 1.0) * 100.0

        return {
            "material": self.props["name"],
            "linewidth_nm": self.w * 1e9,
            "thermal_mode": thermal_res,
            "field_guided_mode": field_res,
            "metrics": {
                "resistivity_reduction_pct": resistivity_reduction_pct,
                "conductivity_gain_pct": conductivity_gain_pct
            }
        }


if __name__ == "__main__":
    # Test suite for 10nm Gold (Au) Interconnects
    engine = TransportConductivityEngine(material="Au", linewidth_nm=10.0)
    results = engine.run_comparison(u_eff_ev=-10.83)

    print("==========================================================")
    print(f" SUB-ATOMIC TRANSPORT ENGINE: {results['material']} ({results['linewidth_nm']} nm Line)")
    print("==========================================================")
    print(f"Standard Thermal Resistivity    : {results['thermal_mode']['resistivity_uohm_cm']:.3f} uOhm-cm")
    print(f"Field-Guided Resistivity         : {results['field_guided_mode']['resistivity_uohm_cm']:.3f} uOhm-cm")
    print("----------------------------------------------------------")
    print(f"Standard Thermal Conductivity   : {results['thermal_mode']['conductivity_MS_m']:.2f} MS/m")
    print(f"Field-Guided Conductivity        : {results['field_guided_mode']['conductivity_MS_m']:.2f} MS/m")
    print("----------------------------------------------------------")
    print(f"Resistivity Reduction           : {results['metrics']['resistivity_reduction_pct']:.2f} %")
    print(f"Conductivity Gain               : {results['metrics']['conductivity_gain_pct']:.2f} %")
    print("==========================================================")
