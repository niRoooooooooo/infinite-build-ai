# Master Document — Data Collection APIs

**Project:** Contextual Ad Intelligence Engine (Bangladesh-focused)
**Stage:** Hackathon MVP (1–3 day build)
**Scope of this document:** Data collection layer only. Generation, SEO, and creative APIs covered in separate documents.

---

## 1. Purpose

This document specifies every external data source the system uses to gather real-time context for ad personalization. Each entry includes the API, what data it returns, how to integrate it, cost, rate limits, and whether it's required for MVP or optional.

The data collection layer feeds the **Context Engine**, which combines raw signals into derived insights ("mood," "meal time," "spending window") that are then passed to the Generation Layer.

---

## 2. Architecture Overview

```
[ External APIs ] → [ Context Engine ] → [ Derived Contexts ] → [ Generation Layer ]
       ↑                                                              ↓
[ Browser Signals ]                                          [ Ad Output ]
       ↑
[ Demo Persona DB ]
```

Three input streams feed the Context Engine:
1. **External APIs** — location, weather, holidays, etc.
2. **Browser signals** — language, connection speed, color scheme
3. **Demo persona DB** — simulated first-party data (purchase history, age, preferences)

---

## 3. Data Sources — Required for MVP

### 3.1 Location (IP-based)

| Field | Detail |
|---|---|
| **API** | ip-api.com |
| **URL** | `http://ip-api.com/json/{ip}` (or `/json/` for caller's IP) |
| **Auth** | None |
| **Cost** | Free |
| **Rate limit** | 45 requests/minute per IP |
| **Returns** | country, regionName, city, lat, lon, timezone, isp |
| **Priority** | MVP-critical |

**Backup:** ipapi.co (free 1000/day, requires no key for basic use)

**Integration note:** Call once per session, cache the result. No need to re-fetch.

---

### 3.2 Weather (current + forecast)

| Field | Detail |
|---|---|
| **API** | Open-Meteo |
| **URL** | `https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m` |
| **Auth** | None |
| **Cost** | Free, unlimited for non-commercial |
| **Rate limit** | 10,000 calls/day free tier |
| **Returns** | Temperature, "feels like," humidity, precipitation, weather code, wind, UV |
| **Priority** | MVP-critical |

**Backup:** OpenWeatherMap (free 1000/day, requires key) or WeatherAPI.com (free 1M/month, requires key)

**Integration note:** Pass lat/lon from the location step. Weather codes map to conditions (clear, rain, etc.) via Open-Meteo's documented code table.

---

### 3.3 Time & Calendar Context

| Field | Detail |
|---|---|
| **Source** | JavaScript Date object / Python datetime |
| **API** | None — built-in |
| **Cost** | Free |
| **Returns** | Hour, minute, day-of-week, day-of-month, month, year, timezone offset |
| **Priority** | MVP-critical |

**Derived fields to compute:**
- Time bucket: early-morning / morning / noon / afternoon / evening / night / late-night
- Day type: weekday / weekend (Bangladesh: Fri–Sat is weekend)
- Season (Bangladesh-specific): Winter (Dec–Feb), Spring (Mar–Apr), Summer (May–Jun), Monsoon (Jul–Sep), Autumn (Oct–Nov)
- Meal window: breakfast (6–10am), lunch (12–3pm), snack (4–6pm), dinner (7–10pm), late-night (10pm+)

---

### 3.4 Bangladesh Cultural Calendar

| Field | Detail |
|---|---|
| **Source** | Hand-curated JSON file |
| **API** | None — internal data |
| **Cost** | Free (time investment: ~1 hour) |
| **Priority** | MVP-critical (this is the local moat) |

**Required entries:**

```json
{
  "events": [
    { "name": "Ramadan 2026", "start": "2026-02-17", "end": "2026-03-18", "type": "religious_observance" },
    { "name": "Eid-ul-Fitr", "date": "2026-03-19", "type": "festival", "shopping_window_days": 7 },
    { "name": "Pohela Boishakh", "date": "2026-04-14", "type": "cultural", "shopping_window_days": 5 },
    { "name": "Independence Day", "date": "2026-03-26", "type": "national" },
    { "name": "Eid-ul-Adha", "date": "2026-05-27", "type": "festival", "shopping_window_days": 10 },
    { "name": "Victory Day", "date": "2026-12-16", "type": "national" },
    { "name": "Durga Puja", "date": "2026-09-30", "type": "religious" }
  ],
  "seasons": {
    "monsoon": { "start_month": 6, "end_month": 9 },
    "winter": { "start_month": 12, "end_month": 2 }
  },
  "exam_periods": [
    { "name": "HSC", "approx_start": "2026-04-01", "approx_end": "2026-05-15" },
    { "name": "SSC", "approx_start": "2026-02-01", "approx_end": "2026-03-15" }
  ]
}
```

**Logic to add:**
- Calculate "days until next event"
- Flag "in shopping window" if within event's pre-window
- Flag "currently active" for ongoing periods (Ramadan, monsoon)

---

### 3.5 Demo Persona Database

| Field | Detail |
|---|---|
| **Source** | Static JSON / local storage |
| **API** | None — internal |
| **Cost** | Free |
| **Priority** | MVP-critical (replaces first-party brand data) |

**Schema per persona:**

```json
{
  "id": "user_001",
  "display_name": "Rafi",
  "age": 22,
  "city": "Dhaka",
  "occupation_mode": "student",
  "language_preference": "banglish",
  "dietary": "none",
  "spending_tier": "low_to_mid",
  "purchase_history": [
    { "category": "fast_food", "item": "biryani", "count": 4 },
    { "category": "beverages", "item": "cold_coffee", "count": 2 }
  ],
  "browsing_history": ["laptops", "headphones"],
  "loyalty_status": "silver",
  "interests": ["gaming", "movies", "cricket"]
}
```

**Build 5 personas with varied profiles** — different cities, ages, occupations, dietary preferences, spending tiers. This becomes the input variety that makes your demo look intelligent.

---

### 3.6 Browser Signals

| Field | Detail |
|---|---|
| **Source** | Browser JavaScript |
| **API** | None — built-in |
| **Cost** | Free |
| **Priority** | MVP-medium (nice-to-have) |

**Signals to capture:**

| Signal | JS code | Returns |
|---|---|---|
| Language | `navigator.language` | "en-US", "bn-BD", etc. |
| Languages list | `navigator.languages` | Array |
| Connection type | `navigator.connection.effectiveType` | "4g", "3g", "2g" |
| Color scheme | `window.matchMedia('(prefers-color-scheme: dark)').matches` | true/false |
| Device type | `navigator.userAgent` parsing | mobile/desktop/tablet |
| Screen size | `window.innerWidth`, `window.innerHeight` | px values |
| Timezone | `Intl.DateTimeFormat().resolvedOptions().timeZone` | "Asia/Dhaka" |

**Note:** `navigator.connection` is not supported on Safari/iOS. Have a fallback default.

---

## 4. Data Sources — Optional (Add if time permits)

### 4.1 Public Holidays

| Field | Detail |
|---|---|
| **API** | Nager.Date |
| **URL** | `https://date.nager.at/api/v3/PublicHolidays/{year}/BD` |
| **Auth** | None |
| **Cost** | Free |
| **Priority** | Low (cultural calendar covers most of this) |

---

### 4.2 Sports / Cricket

| Field | Detail |
|---|---|
| **API** | TheSportsDB |
| **URL** | `https://www.thesportsdb.com/api/v1/json/3/eventsnext.php?id={team_id}` |
| **Auth** | None |
| **Cost** | Free |
| **Priority** | Medium (huge cultural moment in BD) |

**Use case:** Detect if Bangladesh national cricket team is playing today or within 24 hours. Trigger sports-mode ads (snacks, beverages, jerseys).

---

### 4.3 Traffic Conditions

| Field | Detail |
|---|---|
| **API** | TomTom Traffic API |
| **URL** | `https://api.tomtom.com/traffic/services/4/flowSegmentData/...` |
| **Auth** | API key required |
| **Cost** | 2,500 free requests/day |
| **Priority** | Low (only relevant for Dhaka/Chittagong commute scenarios) |

---

### 4.4 News / Trending Topics

| Field | Detail |
|---|---|
| **API** | NewsAPI |
| **URL** | `https://newsapi.org/v2/top-headlines?country=bd` |
| **Auth** | API key required |
| **Cost** | Free 100 requests/day (developer tier) |
| **Priority** | Low — hard to use cleanly in ad generation |

**Caution:** Don't rely on this for live demo. Cache results or hardcode for the demo.

---

### 4.5 Air Quality

| Field | Detail |
|---|---|
| **API** | Open-Meteo Air Quality |
| **URL** | `https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm2_5,pm10,european_aqi` |
| **Auth** | None |
| **Cost** | Free |
| **Priority** | Low-medium (Dhaka has severe air quality issues — could be a creative angle) |

**Use case:** High AQI → indoor activity ads, air purifiers, masks, home delivery.

---

## 5. Derived Contexts (No External API — Built from above)

The Context Engine combines raw signals into higher-order contexts. **This is where the system looks intelligent.**

| Derived Context | Inputs | Example Output |
|---|---|---|
| **Mood / vibe** | weather + time + day-of-week + season | "Friday evening + cool + winter → weekend chill mode" |
| **Activity likelihood** | time + weather + location | "Saturday morning + sunny + Cox's Bazar → vacation mode" |
| **Meal context** | time + cultural calendar | "1pm BD → lunch. During Ramadan, 1pm → fasting, suggest iftar prep" |
| **Comfort need** | weather extremes | "38°C Dhaka → cooling priority (drinks, AC, ice cream)" |
| **Spending window** | day-of-month + day-of-week + persona spending tier | "1st week of month + weekend + mid-tier → higher spend appetite" |
| **Social occasion** | cultural calendar proximity | "3 days before Eid → gift mode" |
| **Stress level** | time + day + traffic (if available) | "Tue 8am + heavy Dhaka traffic → commute stress, quick coffee" |
| **Cultural moment** | calendar + sports | "Match day + evening → snack/beverage surge" |
| **Connectivity-aware format** | browser connection + device | "Slow 3G + mobile → text-heavy, no video" |

**Implementation:** A single function `deriveContext(rawSignals) → enrichedContext` that runs after data collection and before generation.

---

## 6. Cost Summary (Full MVP)

| Source | Cost | Notes |
|---|---|---|
| ip-api.com | $0 | No signup |
| Open-Meteo (weather + air quality) | $0 | No signup |
| Time/date logic | $0 | Built-in |
| Cultural calendar JSON | $0 | Hand-curated |
| Demo personas | $0 | Hand-curated |
| Browser signals | $0 | Built-in |
| Nager.Date (holidays) | $0 | No signup |
| TheSportsDB (sports) | $0 | No signup |
| TomTom Traffic (optional) | $0 | Free tier covers demo |
| NewsAPI (optional) | $0 | Free tier (100/day) |

**Total cost for data collection layer: $0**

---

## 7. Privacy & Ethics Statement (For Pitch)

The system uses only:
- **Public environmental data** (location, weather, time, calendar)
- **Browser-provided signals** (with no cross-site tracking)
- **First-party data from brands' own consented users** (in production)

The system explicitly does NOT:
- Buy data from data brokers
- Track users across other websites
- Infer religion, health status, sexual orientation, or political beliefs
- Use facial recognition or camera-based inference
- Scrape social media profiles

This is a strength to highlight in the pitch. Many MarTech tools cannot say this.

---

## 8. Integration Plan (For Build Team)

**Owner:** Backend / API integration developer

**Step 1 — Foundation (Day 1, morning, ~2 hours)**
- Create `getLocation()` function using ip-api.com
- Create `getWeather(lat, lon)` function using Open-Meteo
- Create `getTimeContext()` function using JS Date
- Test each independently with console output

**Step 2 — Internal data (Day 1, afternoon, ~2 hours)**
- Write `culturalCalendar.json`
- Write `demoPersonas.json` (5 personas minimum)
- Create `getCulturalContext(date)` function
- Create `getPersona(id)` function

**Step 3 — Browser signals (Day 1, evening, ~30 min)**
- Create `getBrowserSignals()` function
- Test on mobile + desktop

**Step 4 — Context Engine (Day 2, morning, ~3 hours)**
- Build `getFullContext(personaId)` master function that calls all of the above
- Build `deriveContext(rawSignals)` to produce derived insights
- Output: a single context object passed to the Generation Layer

**Step 5 — Caching & error handling (Day 2, afternoon, ~1 hour)**
- Cache location and weather per session
- Fallback values if any API fails (always return *something*, never crash)

---

## 9. Output Schema (What the Context Engine Hands Off)

This is what the Generation Layer receives:

```json
{
  "raw": {
    "location": { "city": "Dhaka", "country": "BD", "lat": 23.7, "lon": 90.4 },
    "weather": { "temp_c": 34, "condition": "hot_clear", "humidity": 70, "feels_like": 38 },
    "time": { "hour": 15, "day_of_week": "friday", "month": 5, "season": "summer" },
    "calendar": { "active_events": [], "days_until_next": { "Eid_ul_Adha": 27 } },
    "persona": { "id": "user_001", "age": 22, "city": "Dhaka", "language": "banglish", "purchase_history": [] },
    "browser": { "language": "en-US", "connection": "4g", "dark_mode": false, "device": "mobile" }
  },
  "derived": {
    "mood": "hot_afternoon_refresh_seeking",
    "meal_context": "post_lunch_snack_window",
    "comfort_need": "cooling",
    "spending_window": "neutral",
    "cultural_moment": "none_active",
    "format_recommendation": "rich_media_ok",
    "tone_suggestion": "casual_playful"
  }
}
```

This single object is what feeds the next layer.

---

## 10. Sections To Be Built (Separate Documents)

- **Document 2:** Generation Layer APIs (LLM, image generation, voice)
- **Document 3:** Creative Templates & Brand Kit System
- **Document 4:** Performance Measurement & Loyalty Loop
- **Document 5:** Optimization & Pattern Learning
- **Document 6:** Frontend / UI Architecture
- **Document 7:** Pitch & Demo Script
