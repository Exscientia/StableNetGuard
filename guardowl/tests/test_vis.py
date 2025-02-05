prefix = "guardowl/tests/data/stability_testing"


def test_generate_visualization():
    from guardowl.vis import MonitoringPlotter

    prefix_path = f"{prefix}/ZINC00061095"
    s = MonitoringPlotter(
        f"{prefix_path}/vacuum_ZINC00061095_ani2x_nnpops_300.dcd",
        f"{prefix_path}/vacuum_ZINC00061095_ani2x_nnpops_300.pdb",
        f"{prefix_path}/vacuum_ZINC00061095_ani2x_nnpops_300.csv",
    )
    s.set_nglview()
    s.generate_summary()


def test_visualize_DOF_scan():
    from guardowl.vis import MonitoringPlotter

    prefix_path = f"{prefix}/ethanol"
    s = MonitoringPlotter(
        f"{prefix_path}/vacuum_ethanol_ani2x_nnpops.dcd",
        f"{prefix_path}/vacuum_ethanol_ani2x_nnpops.pdb",
        f"{prefix_path}/vacuum_ethanol_ani2x_nnpops.csv",
    )
    s.set_nglview()
    s.generate_summary(bonded_scan=True)


def test_waterbox():
    from guardowl.vis import MonitoringPlotter

    system_name = "waterbox"
    prefix_path = f"{prefix}/{system_name}/"
    ensemble = "npt"
    nnp = "ani2x"
    implementation = "nnpops"

    s = MonitoringPlotter(
        f"{prefix_path}/{system_name}_15A_{nnp}_{implementation}_{ensemble}_300K_300.dcd",
        f"{prefix_path}/{system_name}_15A_{nnp}_{implementation}_{ensemble}_300K_300.pdb",
        f"{prefix_path}/{system_name}_15A_{nnp}_{implementation}_{ensemble}_300K_300.csv",
    )

    s.set_nglview(wrap=True, periodic=True)
    s.nglview.add_representation("licorice", selection="water")
    s.generate_summary()
