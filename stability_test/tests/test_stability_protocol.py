from pathlib import Path

import pytest
from openmm import unit
from openmm.app import StateDataReporter
from openmmml import MLPotential
from openmmtools.utils import get_fastest_platform

from stability_test.constants import available_nnps_and_implementation
from stability_test.protocolls import (BondProfileProtocol, DOFTestParameters,
                                       MultiTemperatureProtocol,
                                       PropagationProtocol,
                                       StabilityTestParameters)
from stability_test.simulation import SystemFactory
from stability_test.testsystems import (HipenTestsystemFactory,
                                        SmallMoleculeTestsystemFactory,
                                        WaterboxTestsystemFactory)


@pytest.mark.parametrize("nnp, implementation", available_nnps_and_implementation)
def test_setup_vacuum_protocol(nnp: str, implementation: str) -> None:
    """Test if we can run a simulation for a number of steps"""

    # ---------------------------#
    platform = get_fastest_platform()
    name = "ZINC00107550"

    testsystem = HipenTestsystemFactory().generate_testsystems(name)
    nnp_instance = MLPotential(nnp)

    system = SystemFactory().initialize_pure_ml_system(
        nnp_instance,
        testsystem.topology,
        implementation=implementation,
    )
    output_folder = "test_stability_protocol"
    log_file_name = f"vacuum_{name}_{nnp}_{implementation}"
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    stability_test = MultiTemperatureProtocol()

    reporter = StateDataReporter(
        file=None,  # it is necessary to set this to None since it otherwise can't be passed to mp
        reportInterval=50,
        step=True,  # must be set to true
        time=True,
        potentialEnergy=True,
        totalEnergy=True,
        temperature=True,
        density=True,
        speed=True,
    )
    params = StabilityTestParameters(
        protocol_length=200,
        temperature=unit.Quantity(300, unit.kelvin),
        ensemble="NVT",
        simulated_annealing=False,
        system=system,
        platform=platform,
        testsystem=testsystem,
        output_folder=output_folder,
        log_file_name=log_file_name,
        state_data_reporter=reporter,
    )

    stability_test.perform_stability_test(params)


@pytest.mark.parametrize("ensemble", ["NVE", "NVT", "NpT"])
@pytest.mark.parametrize("nnp, implementation", available_nnps_and_implementation)
def test_setup_waterbox_protocol(ensemble: str, nnp: str, implementation: str) -> None:
    """Test if we can run a simulation for a number of steps"""

    # ---------------------------#
    platform = get_fastest_platform()

    edge_size = 10
    testsystem = WaterboxTestsystemFactory().generate_testsystems(
        unit.Quantity(edge_size, unit.angstrom)
    )
    nnp_instance = MLPotential(nnp)

    system = SystemFactory().initialize_pure_ml_system(
        nnp_instance,
        testsystem.topology,
        implementation=implementation,
    )

    output_folder = "test_stability_protocol"
    log_file_name = f"waterbox_{edge_size}A_{nnp}_{implementation}_{ensemble}"
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    stability_test = PropagationProtocol(ensemble=ensemble)

    reporter = StateDataReporter(
        file=None,  # it is necessary to set this to None since it otherwise can't be passed to mp
        reportInterval=10,
        step=True,  # must be set to true
        time=True,
        potentialEnergy=True,
        totalEnergy=True,
        temperature=True,
        density=True,
        speed=True,
    )

    params = StabilityTestParameters(
        protocol_length=200,
        temperature=unit.Quantity(300, unit.kelvin),
        ensemble=ensemble,
        simulated_annealing=False,
        system=system,
        platform=platform,
        testsystem=testsystem,
        output_folder=output_folder,
        log_file_name=log_file_name,
        state_data_reporter=reporter,
    )

    stability_test.perform_stability_test(
        params,
    )


@pytest.mark.parametrize("nnp, implementation", available_nnps_and_implementation)
def test_DOF_protocol(nnp: str, implementation: str) -> None:
    """Test if we can run a simulation for a number of steps"""

    # ---------------------------#
    platform = get_fastest_platform()

    testsystem = SmallMoleculeTestsystemFactory().generate_testsystems(name="ethanol")

    nnp_instance = MLPotential(nnp)

    system = SystemFactory().initialize_pure_ml_system(
        nnp_instance,
        testsystem.topology,
        implementation=implementation,
    )

    output_folder = "test_stability_protocol"
    log_file_name = f"vacuum_{testsystem.testsystem_name}_{nnp}_{implementation}"
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    stability_test = BondProfileProtocol()
    params = DOFTestParameters(
        system=system,
        platform=platform,
        testsystem=testsystem,
        output_folder=output_folder,
        log_file_name=log_file_name,
        bond=[0, 3],
    )

    stability_test.perform_bond_scan(params)
