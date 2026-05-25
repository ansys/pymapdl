"""Cross-platform wrapper for docker compose in docker/run.

Runs ``docker compose`` with ``--env-file .env`` when the file exists in the
same directory, otherwise omits it so shell-exported variables are used instead.

Usage (via tox)::

    {envpython} {toxinidir}/docker/run/compose.py --profile mapdl up -d
    {envpython} {toxinidir}/docker/run/compose.py --profile mapdl down
"""

import os
from pathlib import Path
import subprocess  # nosec B404
import sys

_HERE = Path(__file__).parent


def main() -> None:
    env_file = _HERE / ".env"
    compose_file = _HERE / "docker-compose.yml"

    cmd = ["docker", "compose", "-f", str(compose_file)]
    if env_file.exists():
        cmd += ["--env-file", str(env_file)]
    else:
        if not os.environ.get("ANSYSLMD_LICENSE_FILE"):
            sys.exit(
                "ERROR: ANSYSLMD_LICENSE_FILE is not set. Add it to docker/run/.env or export it in your shell."
            )

        if not os.environ.get("DOCKER_IMAGE"):
            sys.exit(
                "ERROR: DOCKER_IMAGE is not set. Add it to docker/run/.env or export it in your shell."
            )

    cmd += sys.argv[1:]

    sys.exit(subprocess.call(cmd))  # nosec B603


if __name__ == "__main__":
    main()
