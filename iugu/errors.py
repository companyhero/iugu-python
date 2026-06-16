from typing import Any


class ApiError(Exception):
    pass


def format_api_error_message(payload: Any) -> str | None:
    if not isinstance(payload, dict):
        return None

    errors = payload.get("errors")
    if errors:
        if isinstance(errors, dict):
            return "; ".join(f"{key}: {value}" for key, value in errors.items())
        return str(errors)

    error = payload.get("error")
    if error is None:
        return None

    parts = [str(error)]
    code = payload.get("code")
    msg = payload.get("msg")
    if code is not None:
        parts.append(f"code={code}")
    if msg:
        parts.append(str(msg))
    return " | ".join(parts)
