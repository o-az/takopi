from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from .constants import TELEGRAM_CONFIG_PATH


def _load_toml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    import tomllib

    return tomllib.loads(path.read_text(encoding="utf-8"))


def load_telegram_config(path: Optional[str] = None) -> Dict[str, Any]:
    cfg_path = Path(path) if path else TELEGRAM_CONFIG_PATH
    return _load_toml(cfg_path)


def config_get(config: Dict[str, Any], key: str) -> Any:
    if key in config:
        return config[key]
    nested = config.get("telegram")
    if isinstance(nested, dict) and key in nested:
        return nested[key]
    return None


def parse_allowed_chat_ids(value: str) -> Optional[set[int]]:
    """
    Parse a comma-separated chat id string like "123,456".
    """
    v = (value or "").strip()
    if not v:
        return None
    out: set[int] = set()
    for part in v.split(","):
        part = part.strip()
        if not part:
            continue
        out.add(int(part))
    return out


def parse_chat_id_list(value: Any) -> Optional[set[int]]:
    if value is None:
        return None
    if isinstance(value, str):
        return parse_allowed_chat_ids(value)
    if isinstance(value, int):
        return {value}
    if isinstance(value, (list, tuple, set)):
        out: set[int] = set()
        for item in value:
            if item is None:
                continue
            if isinstance(item, str):
                if not item.strip():
                    continue
                out.add(int(item))
            else:
                out.add(int(item))
        return out or None
    return None


def resolve_chat_ids(config: Dict[str, Any]) -> Optional[set[int]]:
    chat_ids = parse_chat_id_list(config_get(config, "chat_id"))
    if chat_ids is None:
        chat_ids = parse_chat_id_list(config_get(config, "allowed_chat_ids"))
    if chat_ids is None:
        chat_ids = parse_chat_id_list(config_get(config, "startup_chat_ids"))
    return chat_ids
