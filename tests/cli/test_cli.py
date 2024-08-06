import subprocess


def test_help_return_0_code():
    result = subprocess.run(["python", "-m", "pytomation", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
