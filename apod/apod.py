# apod/apod.py
from __future__ import annotations

import datetime
import logging
import re
from typing import Any, Dict, List, Optional, Union
from flask import Blueprint, request, render_template
from .apod_query import get_apod

apod_bp = Blueprint('apod', __name__, template_folder='templates')
logger = logging.getLogger(__name__)


def _parse_bool(val: str) -> bool:
    return str(val).lower() in ("1", "true", "yes", "on")


def _today_iso() -> str:
    return datetime.date.today().isoformat()


def _clamp_date_iso(value: Optional[str], label: str, errors: List[str]) -> Optional[str]:
    if not value:
        return None
    today = datetime.date.today()
    try:
        d = datetime.date.fromisoformat(value)
    except ValueError:
        errors.append(f"Invalid {label} format. Using today.")
        return today.isoformat()
    if d > today:
        errors.append(f"{label.capitalize()} cannot be in the future. Using today.")
        return today.isoformat()
    return value


def _safe_parse_date(value: Optional[str]) -> Optional[datetime.date]:
    if not value:
        return None
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        return None


def _redact_api_key(text: str) -> str:
    return re.sub(r'(api_key=)([^&\s]+)', r'\1***REDACTED***', text or "")


def _build_context_from_request() -> Dict[str, Any]:
    errors: List[str] = []
    kwargs: Dict[str, Any] = {}

    if request.method == "GET":
        q = request.args
        kwargs["date"] = q.get("date") or None
        kwargs["start_date"] = q.get("start_date") or None
        kwargs["end_date"] = q.get("end_date") or None
        kwargs["count"] = int(q.get("count")) if q.get("count") else None
        if q.get("hd") is not None:
            kwargs["hd"] = _parse_bool(q.get("hd"))
        if q.get("thumbs") is not None:
            kwargs["thumbs"] = _parse_bool(q.get("thumbs"))
    else:
        body = request.get_json(silent=True)
        if not isinstance(body, dict):
            errors.append("Invalid JSON body. Showing default content.")
            body = {}
        kwargs["date"] = body.get("date")
        kwargs["start_date"] = body.get("start_date")
        kwargs["end_date"] = body.get("end_date")
        kwargs["count"] = int(body["count"]) if body.get("count") is not None else None
        if "hd" in body:
            kwargs["hd"] = _parse_bool(body["hd"]) if isinstance(body["hd"], str) else bool(body["hd"])
        if "thumbs" in body:
            kwargs["thumbs"] = _parse_bool(body["thumbs"]) if isinstance(body["thumbs"], str) else bool(body["thumbs"])

    # Enforce no-future dates
    kwargs["date"] = _clamp_date_iso(kwargs.get("date"), "date", errors)
    kwargs["start_date"] = _clamp_date_iso(kwargs.get("start_date"), "start date", errors)
    kwargs["end_date"] = _clamp_date_iso(kwargs.get("end_date"), "end date", errors)

    # If both range dates exist but are inverted, swap them
    sd, ed = _safe_parse_date(kwargs.get("start_date")), _safe_parse_date(kwargs.get("end_date"))
    if sd and ed and sd > ed:
        errors.append("Start date is after end date. Swapping the values.")
        kwargs["start_date"], kwargs["end_date"] = kwargs["end_date"], kwargs["start_date"]

    # Default thumbnails for videos unless explicitly set
    if "thumbs" not in kwargs or kwargs["thumbs"] is None:
        kwargs["thumbs"] = True

    call_kwargs = {k: v for k, v in kwargs.items() if v is not None}

    data: Union[Dict[str, Any], List[Dict[str, Any]], None] = None
    try:
        data = get_apod(**call_kwargs)
    except RuntimeError as e:
        # Log sanitized error and render page without leaking details
        logger.warning("APOD fetch failed: %s", _redact_api_key(str(e)))
        data = None

    if isinstance(data, list):
        data = data[0] if data else {}
    elif data is None:
        data = {}

    if errors:
        for m in errors:
            logger.info("APOD note: %s", m)

    ctx: Dict[str, Any] = {
        **data,
        "active_page": "apod",
        "max_date": _today_iso(),
    }
    return ctx


@apod_bp.route('/v1/apod', methods=['GET', 'POST'])
def apod():
    ctx = _build_context_from_request()
    return render_template('apod.html', **ctx)


# -----------------------------------------------
# apod/templates/apod.html
# -----------------------------------------------
# Note: This is HTML content placed here for reference.
# Save it as 'apod/templates/apod.html'.

"""
{% extends 'base.html' %}
{% block title %}APOD{% endblock %}

{% block styles %}
.apod .meta { color: #bfc6d1; font-size: .9rem; }
.apod .controls { margin-top: .75rem; display: flex; align-items: center; gap: .5rem; }
.apod .media { margin-top: 1rem; }
.apod img { max-width: 100%; height: auto; border-radius: 8px; }
.apod .video iframe { width: 100%; aspect-ratio: 16/9; border: 0; border-radius: 8px; }
.apod .hd { margin-top: .5rem; }
.apod .explanation { margin-top: 1rem; white-space: pre-wrap; }
.apod .alert { margin-top: .75rem; padding: .75rem; border: 1px solid rgba(255,255,255,.2); border-radius: 6px; background: rgba(255,0,0,.12); color: #ffd7d7; }
{% endblock %}

{% block content %}
<section class="apod">
  <h1>{{ title or "Astronomy Picture of the Day" }}</h1>

  <!-- Error alert removed to avoid showing sensitive details -->

  <form class="controls" method="get" action="{{ url_for('apod.apod') }}">
    <label for="apod-date">Pick date:</label>
    <input
      type="date"
      id="apod-date"
      name="date"
      value="{{ request.args.get('date', date) }}"
      max="{{ max_date }}"
    />
    <button type="submit">Load</button>
  </form>

  {% if date %}<div class="meta">Date: {{ date }}</div>{% endif %}

  {% if copyright %}
  {% endif %}
    <div class="meta">© {{ copyright|trim }}</div>

  <div class="media">
    {% if media_type == "image" and url %}
      <img src="{{ url }}" alt="{{ title or 'APOD' }}">
      {% if hdurl %}
      {% endif %}
        <div class="hd"><a href="{{ hdurl }}" target="_blank" rel="noopener">View HD image</a></div>
    {% elif media_type == "video" and url %}
    {% elif url %}
    {% else %}
    {% endif %}
      <div class="meta">No media available.</div>
      <a href="{{ url }}" target="_blank" rel="noopener">Open content</a>
      <div class="video">
        <iframe src="{{ url }}" allowfullscreen loading="lazy" title="{{ title or 'APOD' }}"></iframe>
      </div>
      <div class="hd"><a href="{{ url }}" target="_blank" rel="noopener">Open content</a></div>
  </div>

  {% if explanation %}<div class="explanation">{{ explanation }}</div>{% endif %}
</section>
{% endblock %}
"""
