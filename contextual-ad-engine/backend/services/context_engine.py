"""
Context Engine — assembles raw signals from all sources and derives
higher-order insights that feed the generation layer.

Output schema matches doc 1 Section 9:
  { "raw": { location, weather, time, calendar, persona, browser },
    "derived": { mood, meal_context, comfort_need, spending_window,
                 cultural_moment, activity_likelihood,
                 format_recommendation, tone_suggestion } }
"""

import json
from datetime import date, datetime, timezone
from typing import Optional

import httpx

# ── In-memory caches ──────────────────────────────────────────────────────────
_location_cache: dict = {}
_weather_cache: dict = {}

# ── Dhaka fallback ────────────────────────────────────────────────────────────
_DHAKA = {
    "city": "Dhaka",
    "country": "BD",
    "lat": 23.7104,
    "lon": 90.4074,
    "timezone": "Asia/Dhaka",
}

# ── Open-Meteo weather code → condition string ────────────────────────────────
_WEATHER_CODES = {
    0: "clear", 1: "mostly_clear", 2: "partly_cloudy", 3: "overcast",
    45: "fog", 48: "fog",
    51: "drizzle", 53: "drizzle", 55: "drizzle",
    61: "rain", 63: "rain", 65: "heavy_rain",
    71: "snow", 73: "snow", 75: "heavy_snow",
    80: "rain_showers", 81: "rain_showers", 82: "heavy_rain",
    95: "thunderstorm", 96: "thunderstorm", 99: "thunderstorm",
}


# ── Location ──────────────────────────────────────────────────────────────────

def get_location(ip_address: Optional[str] = None) -> dict:
    """ip-api.com lookup. Falls back to Dhaka on local IP or failure."""
    if not ip_address or ip_address in ("127.0.0.1", "::1", "testclient"):
        return _DHAKA.copy()

    if ip_address in _location_cache:
        return _location_cache[ip_address]

    try:
        resp = httpx.get(
            f"http://ip-api.com/json/{ip_address}",
            params={"fields": "status,city,countryCode,lat,lon,timezone"},
            timeout=3.0,
        )
        data = resp.json()
        if data.get("status") == "success":
            result = {
                "city":     data.get("city",        _DHAKA["city"]),
                "country":  data.get("countryCode", "BD"),
                "lat":      data.get("lat",         _DHAKA["lat"]),
                "lon":      data.get("lon",         _DHAKA["lon"]),
                "timezone": data.get("timezone",    _DHAKA["timezone"]),
            }
            _location_cache[ip_address] = result
            return result
    except Exception:
        pass

    return _DHAKA.copy()


# ── Weather ───────────────────────────────────────────────────────────────────

def get_weather(lat: float, lon: float) -> dict:
    """Open-Meteo current weather. Cached per (lat, lon, UTC-hour)."""
    cache_key = (round(lat, 2), round(lon, 2), datetime.now(timezone.utc).hour)

    if cache_key in _weather_cache:
        return _weather_cache[cache_key]

    try:
        resp = httpx.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": (
                    "temperature_2m,relative_humidity_2m,apparent_temperature,"
                    "precipitation,weather_code,wind_speed_10m"
                ),
            },
            timeout=5.0,
        )
        cur = resp.json().get("current", {})
        code = cur.get("weather_code", 0)
        base_condition = _WEATHER_CODES.get(code, "clear")
        temp = cur.get("temperature_2m", 28)

        if temp >= 35:
            condition = f"hot_{base_condition}"
        elif temp <= 15:
            condition = f"cool_{base_condition}"
        else:
            condition = base_condition

        result = {
            "temp_c":      round(temp, 1),
            "feels_like":  round(cur.get("apparent_temperature", temp), 1),
            "humidity":    cur.get("relative_humidity_2m", 70),
            "precipitation": cur.get("precipitation", 0),
            "wind":        cur.get("wind_speed_10m", 0),
            "weather_code": code,
            "condition":   condition,
        }
        _weather_cache[cache_key] = result
        return result

    except Exception:
        return {
            "temp_c": 28, "feels_like": 30, "humidity": 70,
            "precipitation": 0, "wind": 5,
            "weather_code": 0, "condition": "clear",
        }


# ── Time ──────────────────────────────────────────────────────────────────────

def get_time_context() -> dict:
    """Bangladesh-specific time buckets, seasons, and meal windows."""
    now = datetime.now()
    h, m = now.hour, now.minute
    month = now.month
    weekday = now.weekday()          # Mon=0 … Sun=6

    # Time bucket (doc 1 §3.3)
    if 4 <= h < 6:
        bucket = "early_morning"
    elif 6 <= h < 12:
        bucket = "morning"
    elif h == 12:
        bucket = "noon"
    elif 13 <= h < 17:
        bucket = "afternoon"
    elif 17 <= h < 20:
        bucket = "evening"
    elif 20 <= h < 23:
        bucket = "night"
    else:
        bucket = "late_night"

    # Bangladesh weekend = Friday (4) & Saturday (5)
    day_type = "weekend" if weekday in (4, 5) else "weekday"

    # Bangladesh seasons (doc 1 §3.3)
    if month in (12, 1, 2):
        season = "winter"
    elif month in (3, 4):
        season = "spring"
    elif month in (5, 6):
        season = "summer"
    elif month in (7, 8, 9):
        season = "monsoon"
    else:
        season = "autumn"

    # Meal window (doc 1 §3.3)
    if 6 <= h < 10:
        meal_window = "breakfast"
    elif 12 <= h < 15:
        meal_window = "lunch"
    elif 16 <= h < 18:
        meal_window = "snack"
    elif 19 <= h < 22:
        meal_window = "dinner"
    elif h >= 22 or h < 4:
        meal_window = "late_night"
    else:
        meal_window = "between_meals"

    _days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    return {
        "hour":         h,
        "minute":       m,
        "day_of_week":  _days[weekday],
        "day_of_month": now.day,
        "month":        month,
        "year":         now.year,
        "time_bucket":  bucket,
        "day_type":     day_type,
        "season":       season,
        "meal_window":  meal_window,
    }


# ── Cultural calendar ─────────────────────────────────────────────────────────

def get_cultural_context() -> dict:
    from services.cultural_calendar import (
        get_active_events,
        get_days_until_events,
        get_shopping_window_events,
    )
    today = date.today()
    return {
        "active_events":       get_active_events(today),
        "days_until_next":     get_days_until_events(today),
        "in_shopping_window":  get_shopping_window_events(today),
    }


# ── Persona ───────────────────────────────────────────────────────────────────

def get_persona(persona_id: str, db) -> Optional[dict]:
    row = db.execute(
        "SELECT * FROM personas WHERE persona_id = ?", (persona_id,)
    ).fetchone()
    if not row:
        return None
    p = dict(row)
    p["persona_data"] = json.loads(p.get("persona_data") or "{}")
    return p


# ── Browser signals ───────────────────────────────────────────────────────────

def get_browser_signals(headers: dict) -> dict:
    accept_lang = headers.get("accept-language", "en-US")
    primary = accept_lang.split(",")[0].split(";")[0].strip()
    return {
        "language":         primary,
        "accept_languages": accept_lang,
    }


# ── Derive context (rule-based, doc 1 §5) ────────────────────────────────────

def derive_context(raw: dict) -> dict:
    weather  = raw.get("weather", {})
    time     = raw.get("time", {})
    calendar = raw.get("calendar", {})
    persona  = raw.get("persona", {})

    temp         = weather.get("temp_c", 28)
    condition    = weather.get("condition", "clear")
    time_bucket  = time.get("time_bucket", "afternoon")
    day_type     = time.get("day_type", "weekday")
    season       = time.get("season", "summer")
    meal_window  = time.get("meal_window", "between_meals")
    day_of_month = time.get("day_of_month", 15)
    active       = calendar.get("active_events", [])
    days_until   = calendar.get("days_until_next", {})
    in_window    = calendar.get("in_shopping_window", [])
    spending     = persona.get("spending_tier", "mid")

    # ── Mood ──────────────────────────────────────────────────────────────────
    if temp >= 35 and time_bucket == "afternoon":
        mood = "hot_afternoon_refresh_seeking"
    elif "rain" in condition and time_bucket in ("evening", "night"):
        mood = "rainy_evening_cozy"
    elif day_type == "weekend" and time_bucket == "evening":
        mood = "weekend_chill"
    elif time_bucket == "morning" and day_type == "weekday":
        mood = "weekday_morning_rush"
    elif time_bucket == "late_night":
        mood = "late_night_browsing"
    elif season == "winter" and time_bucket in ("evening", "night"):
        mood = "winter_evening_comfort"
    elif season == "summer" and temp >= 30:
        mood = "summer_heat_seeking_relief"
    else:
        mood = "neutral_browsing"

    # ── Meal context (Ramadan-aware) ──────────────────────────────────────────
    ramadan_active = any("Ramadan" in e for e in active)
    if ramadan_active:
        if meal_window in ("lunch", "snack"):
            meal_context = "ramadan_fasting_iftar_prep"
        elif meal_window == "dinner":
            meal_context = "ramadan_iftar_time"
        elif meal_window == "late_night" or time.get("hour", 0) < 5:
            meal_context = "ramadan_sehri_window"
        else:
            meal_context = "ramadan_fasting"
    else:
        meal_context = meal_window

    # ── Comfort need ──────────────────────────────────────────────────────────
    if temp >= 35:
        comfort_need = "cooling"
    elif temp <= 15:
        comfort_need = "warming"
    elif "rain" in condition:
        comfort_need = "indoor_comfort"
    else:
        comfort_need = "neutral"

    # ── Spending window ───────────────────────────────────────────────────────
    high_tier = spending in ("mid_to_high", "high")
    if day_of_month <= 7 and day_type == "weekend" and high_tier:
        spending_window = "high_intent"
    elif day_of_month <= 7:
        spending_window = "moderate_intent"
    elif day_of_month >= 25:
        spending_window = "month_end_cautious"
    else:
        spending_window = "neutral"

    # ── Cultural moment ───────────────────────────────────────────────────────
    if active:
        cultural_moment = active[0]
    elif in_window:
        slug = in_window[0].lower().replace(" ", "_").replace("-", "_")
        cultural_moment = f"pre_{slug}_shopping"
    else:
        imminent = [n for n, d in days_until.items() if 0 < d <= 7]
        if imminent:
            slug = imminent[0].lower().replace(" ", "_").replace("-", "_")
            cultural_moment = f"approaching_{slug}"
        else:
            cultural_moment = "none_active"

    # ── Activity likelihood ───────────────────────────────────────────────────
    if time_bucket in ("morning", "noon", "afternoon") and day_type == "weekday":
        activity_likelihood = "commuting_or_working"
    elif time_bucket in ("evening", "night") and day_type == "weekend":
        activity_likelihood = "leisure_social"
    elif time_bucket == "late_night":
        activity_likelihood = "solo_browsing"
    elif day_type == "weekend":
        activity_likelihood = "leisure_relaxed"
    else:
        activity_likelihood = "general_browsing"

    # ── Format recommendation ─────────────────────────────────────────────────
    # In MVP, assume good connectivity (4G). Frontend will override with real signal.
    format_recommendation = "rich_media_ok"

    # ── Tone suggestion ───────────────────────────────────────────────────────
    if cultural_moment != "none_active":
        tone_suggestion = "culturally_warm"
    elif mood in ("hot_afternoon_refresh_seeking", "weekend_chill", "late_night_browsing"):
        tone_suggestion = "casual_playful"
    elif mood == "weekday_morning_rush":
        tone_suggestion = "direct_helpful"
    elif mood in ("winter_evening_comfort", "rainy_evening_cozy"):
        tone_suggestion = "warm_nostalgic"
    else:
        tone_suggestion = "warm_casual"

    return {
        "mood":                  mood,
        "activity_likelihood":   activity_likelihood,
        "meal_context":          meal_context,
        "comfort_need":          comfort_need,
        "spending_window":       spending_window,
        "cultural_moment":       cultural_moment,
        "format_recommendation": format_recommendation,
        "tone_suggestion":       tone_suggestion,
    }


# ── Master function ───────────────────────────────────────────────────────────

def get_full_context(persona_id: str, request_info: dict, db) -> dict:
    """
    Orchestrates all data sources into the complete context object.
    Output matches doc 1 Section 9 schema.
    """
    ip      = request_info.get("ip")
    headers = request_info.get("headers", {})

    location = get_location(ip)
    weather  = get_weather(location["lat"], location["lon"])
    time_ctx = get_time_context()
    cultural = get_cultural_context()
    persona  = get_persona(persona_id, db)
    browser  = get_browser_signals(headers)

    persona_summary = {}
    if persona:
        pdata = persona.get("persona_data", {})
        persona_summary = {
            "id":               persona["persona_id"],
            "age":              persona["age"],
            "city":             persona["city"],
            "language":         persona["language_preference"],
            "spending_tier":    persona["spending_tier"],
            "occupation_mode":  persona["occupation_mode"],
            "purchase_history": pdata.get("purchase_history", []),
        }

    raw = {
        "location": location,
        "weather":  weather,
        "time":     time_ctx,
        "calendar": cultural,
        "persona":  persona_summary,
        "browser":  browser,
    }

    derived = derive_context(raw)

    return {"raw": raw, "derived": derived}
