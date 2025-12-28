from __future__ import annotations

from pathlib import Path

TELEGRAM_HARD_LIMIT = 4096
DEFAULT_CHUNK_LEN = 3500  # leave room for formatting / safety
TELEGRAM_CONFIG_PATH = Path.home() / ".codex" / "telegram.toml"
