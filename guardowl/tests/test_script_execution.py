import subprocess
import pytest


@pytest.mark.parametrize(
    "config_file_path",
    [
        "guardowl/tests/stability_test_hipen.yaml",
        "guardowl/tests/stability_test_waterbox.yaml",
        "guardowl/tests/stability_test_alanine_dipeptide.yaml",
    ],
)
@pytest.mark.parametrize("script_file_path", ["scripts/perform_stability_tests.py"])
def test_script_execution(config_file_path: str, script_file_path: str) -> None:
    print(f"Testing {script_file_path}")
    print(f"Using {config_file_path}")
    # Check if script exists and can be executed
    ret = subprocess.run(["python", script_file_path, "--help"], capture_output=True)
    print("Output from --help:")
    print(ret.stdout.decode("utf-8"))
    print("Error from --help:")
    print(ret.stderr.decode("utf-8"))
    assert ret.returncode == 0

    # Update the arguments to match your argparse in the script
    args = f"python {script_file_path} --config {config_file_path}".split()
    ret = subprocess.run(args, capture_output=True)
    print("Script Output:")
    print(ret.stdout.decode("utf-8"))

    print("Script Error:")
    print(ret.stderr.decode("utf-8"))

    assert ret.returncode == 0