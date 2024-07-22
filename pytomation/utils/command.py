import subprocess
import sys


def run(cwd, *command: any, timeout=None, check=True, env=None):
    return subprocess.run(
        [str(c) for c in command],
        cwd=cwd,
        timeout=timeout,
        check=check,
        stdout=sys.stdout,
        env=env,
    )
