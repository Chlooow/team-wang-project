from __future__ import annotations

import os
import subprocess
from pathlib import Path


def run_dbt_snapshot(project_dir: str = "dbt") -> None:
    project = Path(project_dir).resolve()
    env = os.environ.copy()
    env["DBT_PROFILES_DIR"] = str(project)
    subprocess.run(
        ["dbt", "snapshot", "--project-dir", str(project), "--profiles-dir", str(project)],
        check=True,
        env=env,
    )
