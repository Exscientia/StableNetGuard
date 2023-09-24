import mdtraj as md
import numpy as np


class PropertyCalculator:
    def __init__(self, md_traj: md.Trajectory) -> None:
        self.md_traj = md_traj

    def calculate_water_rdf(self):  # type: ignore
        # Expression selection, a common feature of analysis tools for
        oxygen_pairs = self.md_traj.top.select_pairs(
            "name O and water", "name O and water"
        )
        bins = 300
        r_max = 1
        r_min = 0.01

        mdtraj_rdf = md.compute_rdf(
            self.md_traj, oxygen_pairs, (r_min, r_max), n_bins=bins
        )

        return mdtraj_rdf

    def monitor_water_bond_length(self):  # type: ignore
        bond_list = []
        for bond in self.md_traj.topology.bonds:
            if bond.atom1.residue.name == "HOH" and bond.atom2.residue.name == "HOH":
                bond_list.append((bond.atom1.index, bond.atom2.index))

        return self.monitor_bond_length(bond_list)

    def monitor_water_angle(self):  # type: ignore
        def _extract_angles() -> list:
            angle_list = []
            for bond_1 in self.md_traj.top.bonds:
                # skip if bond is not a water molecule
                if bond_1.atom1.residue.name != "HOH":
                    continue
                for bond_2 in self.md_traj.top.bonds:
                    # skip if bond is not a water molecule
                    if bond_2.atom1.residue.name != "HOH":
                        continue
                    water = {}
                    for bond in [bond_1, bond_2]:
                        water[bond.atom1.index] = bond.atom1.index
                        water[bond.atom2.index] = bond.atom2.index
                    if len(water.keys()) != 3:
                        continue

                    tmp_water = water.values()
                    tmp_water_elements = [atom.element.symbol for atom in tmp_water]
                    # oxy = tmp_water_elements.index("O")

                    angle_list.append([water["H"], water["O"], water["H"]])
            return angle_list

        angle_list = _extract_angles()
        return self.monitor_angle_length(angle_list)

    def monitor_bond_length(self, bond_pairs: list):  # type: ignore
        bond_length = md.compute_distances(self.md_traj, bond_pairs)
        return bond_length

    def monitor_angle_length(self, angle_list: list):  # type: ignore
        angles = md.compute_angles(self.md_traj, angle_list) * (180 / np.pi)
        return angles