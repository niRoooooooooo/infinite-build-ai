import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

CALENDAR_PATH = Path(__file__).parent.parent.parent / "data" / "cultural_calendar.json"
_calendar_cache: Optional[dict] = None


def _load() -> dict:
    global _calendar_cache
    if _calendar_cache is None:
        with open(CALENDAR_PATH) as f:
            _calendar_cache = json.load(f)
    return _calendar_cache


def _to_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def get_active_events(today: Optional[date] = None) -> list:
    """Events currently happening (handles both single-day and multi-day events)."""
    if today is None:
        today = date.today()
    active = []
    for event in _load()["events"]:
        if "start" in event and "end" in event:
            if _to_date(event["start"]) <= today <= _to_date(event["end"]):
                active.append(event["name"])
        elif "date" in event:
            if _to_date(event["date"]) == today:
                active.append(event["name"])
    return active


def get_days_until_events(today: Optional[date] = None) -> dict:
    """Maps event_name → days until it starts (only future/today events)."""
    if today is None:
        today = date.today()
    result = {}
    for event in _load()["events"]:
        target = event.get("date") or event.get("start")
        if target:
            delta = (_to_date(target) - today).days
            if delta >= 0:
                result[event["name"]] = delta
    return result


def get_shopping_window_events(today: Optional[date] = None) -> list:
    """Events whose pre-event shopping window is currently active."""
    if today is None:
        today = date.today()
    in_window = []
    for event in _load()["events"]:
        if "shopping_window_days" not in event or "date" not in event:
            continue
        event_date = _to_date(event["date"])
        window_start = event_date - timedelta(days=event["shopping_window_days"])
        if window_start <= today <= event_date:
            in_window.append(event["name"])
    return in_window


def is_in_shopping_window(event_name: str, today: Optional[date] = None) -> bool:
    if today is None:
        today = date.today()
    return event_name in get_shopping_window_events(today)
