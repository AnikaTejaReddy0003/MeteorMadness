from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Union
import requests

API_URL = "https://api.nasa.gov/planetary/apod"
DEFAULT_API_KEY = "NkXlYjwvpiIY0f2ReQBEkoIgvvVd24Fdeo65Jp71"


def _api_key(provided: Optional[str]) -> str:
    return provided or os.getenv("NASA_API_KEY") or DEFAULT_API_KEY


def _normalize(item: Dict[str, Any]) -> Dict[str, Any]:
    # JSON‑serializable dict tailored for your Jinja template.
    return {
        "title": item.get("title"),
        "date": item.get("date"),
        "explanation": item.get("explanation"),
        "media_type": item.get("media_type"),
        "url": item.get("url"),
        "hdurl": item.get("hdurl"),
        "copyright": item.get("copyright"),
    }


def _request(params: Dict[str, Any], timeout: float) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    try:
        resp = requests.get(API_URL, params=params, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError as e:
        try:
            detail = resp.json()
        except Exception:
            detail = None
        msg = detail.get("error", {}).get("message") if isinstance(detail, dict) else None
        raise RuntimeError(f"APOD request failed: {msg or str(e)}") from e
    except requests.RequestException as e:
        raise RuntimeError(f"APOD network error: {e}") from e
    except ValueError as e:
        raise RuntimeError(f"APOD returned invalid JSON: {e}") from e


def get_apod(
        *,
        api_key: Optional[str] = None,
        date: Optional[str] = None,  # YYYY-MM-DD
        start_date: Optional[str] = None,  # YYYY-MM-DD
        end_date: Optional[str] = None,  # YYYY-MM-DD
        count: Optional[int] = None,  # random N results
        hd: Optional[bool] = None,
        thumbs: Optional[bool] = None,
        timeout: float = 10.0,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Return JSON‑serializable dict or list[dict] from NASA APOD,
    normalized to fields your template expects.
    """
    params: Dict[str, Any] = {"api_key": _api_key(api_key)}
    if date:
        params["date"] = date
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if count is not None:
        params["count"] = int(count)
    if hd is not None:
        params["hd"] = "true" if hd else "false"
    if thumbs is not None:
        params["thumbs"] = "true" if thumbs else "false"

    data = _request(params, timeout)
    if isinstance(data, list):
        return [_normalize(item) for item in data]
    return _normalize(data)
