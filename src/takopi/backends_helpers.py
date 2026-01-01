from __future__ import annotations

import shutil
from pathlib import Path
from typing import Callable

from .backends import EngineConfig, SetupIssue


def which_issue(
    cmd: str, issue: SetupIssue
) -> Callable[[EngineConfig, Path], list[SetupIssue]]:
    def _check(_cfg: EngineConfig, _path: Path) -> list[SetupIssue]:
        return [] if shutil.which(cmd) else [issue]

    return _check
