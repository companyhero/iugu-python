"""Extrai o código LR (adquirente) de respostas JSON ou texto da API Iugu."""

from __future__ import annotations

import json
import re
from typing import Any

_MAX_DEPTH = 8

# Texto livre ou mensagem de erro: "LR: 51", "LR":"05", etc.
_LR_IN_TEXT = re.compile(
    r'(?:["\']?LR["\']?\s*[:=]\s*["\']?|lr_code\s*[:=]\s*["\']?|\bLR\s*[:=]\s*)([0-9A-Za-z]+)',
    re.IGNORECASE,
)


def _as_str(value: Any) -> str | None:
    if value is None:
        return None
    s = str(value).strip()
    return s or None


def _lr_on_dict_keys(obj: dict[str, Any]) -> str | None:
    for key, value in obj.items():
        if isinstance(key, str) and key.lower() in ("lr", "lr_code", "reason_code"):
            return _as_str(value)
    return None


def parse_lr_code(data: Any, *, _depth: int = 0) -> str | None:
    """Devolve o LR se existir no payload; caso contrário ``None``."""
    if data is None or _depth > _MAX_DEPTH:
        return None

    if isinstance(data, str):
        m = _LR_IN_TEXT.search(data)
        if m:
            return _as_str(m.group(1))
        stripped = data.strip()
        if stripped.startswith("{") or stripped.startswith("["):
            try:
                return parse_lr_code(json.loads(stripped), _depth=_depth + 1)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    if isinstance(data, (int, float)):
        return _as_str(data)

    if isinstance(data, dict):
        found = _lr_on_dict_keys(data)
        if found:
            return found
        for value in data.values():
            found = parse_lr_code(value, _depth=_depth + 1)
            if found:
                return found
        return None

    if isinstance(data, (list, tuple)):
        for item in data:
            found = parse_lr_code(item, _depth=_depth + 1)
            if found:
                return found
        return None

    return None
