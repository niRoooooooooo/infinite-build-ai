"""
Generation Engine — orchestrates Gemini LLM copy generation and
Pollinations.ai image generation into fully composed ad objects.
"""

import json
import logging
import os
import re
import time
import uuid
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

import httpx
from dotenv import load_dotenv

_ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(_ENV_PATH, override=True)

logger = logging.getLogger(__name__)

_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
_GEMINI_MODEL   = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
_POLLINATIONS   = "https://image.pollinations.ai/prompt/{prompt}?width=800&height=800&nologo=true"

_GIF_FORMATS   = {"gif_template", "gif_ai_multiframe"}
_SKIP_IMG_FMT  = {"voice_audio"}

_VALID_VISUAL  = {
    "static_image", "gif_template", "gif_ai_multiframe",
    "animated_banner", "video_mp4", "voice_audio",
}
_VALID_COPY    = {
    "joke_pun", "cultural_reference", "question_hook", "stat_hook",
    "inspirational_quote", "urgency_driven", "direct_offer",
    "story_narrative", "relatable_observation",
}
_VALID_TONE    = {
    "warm_casual", "playful_energetic", "serious_premium",
    "urgent_action", "nostalgic_emotional", "informative_helpful",
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _top3(prefs: dict) -> list:
    return [k for k, _ in sorted(prefs.items(), key=lambda x: -x[1])[:3]]


def _deterministic_fallback(brand, product, persona, context) -> dict:
    loc  = context.get("raw", {}).get("location", {})
    wx   = context.get("raw", {}).get("weather", {})
    t    = context.get("raw", {}).get("time", {})
    city = loc.get("city", "Dhaka")
    cond = wx.get("condition", "clear").replace("_", " ")
    slot = t.get("time_bucket", "afternoon").replace("_", " ")
    name = product.get("name", "this product")
    bname= brand.get("display_name", "us")

    return {
        "headline":       f"{name} — made for {city}'s {cond} {slot}",
        "subheadline":    f"From {bname}, for you.",
        "body_copy":      f"Exactly what you need right now. {product.get('description','')[:80]}",
        "cta_text":       "Get it now",
        "cta_urgency":    "medium",
        "tone":           "warm_casual",
        "copy_styles":    ["direct_offer"],
        "visual_format":  "static_image",
        "image_prompt":   f"{name} product shot, clean background, warm lighting",
        "color_mood":     "neutral warm",
        "rationale":      "Fallback ad — Gemini unavailable",
        "quote":          None,
        "joke":           None,
        "cultural_hook":  None,
    }


def _parse_gemini_json(text: str) -> dict:
    """Extract JSON from Gemini response, handling preambles and code fences."""
    text = text.strip()

    # 1. Try to find JSON inside a code fence anywhere in the text
    fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence_match:
        return json.loads(fence_match.group(1))

    # 2. Strip a leading code fence at the start (no closing fence)
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```\s*$", "", text)

    # 3. Extract the first {...} block (handles preamble text before JSON)
    brace_match = re.search(r"\{.*\}", text, re.DOTALL)
    if brace_match:
        return json.loads(brace_match.group(0))

    return json.loads(text)


def _sanitise_creative(creative: dict) -> dict:
    """Ensure enum fields contain only allowed values; clamp to safe defaults."""
    if creative.get("visual_format") not in _VALID_VISUAL:
        creative["visual_format"] = "static_image"

    raw_styles = creative.get("copy_styles", [])
    clean = [s for s in raw_styles if s in _VALID_COPY]
    creative["copy_styles"] = clean if clean else ["direct_offer"]

    if creative.get("tone") not in _VALID_TONE:
        creative["tone"] = "warm_casual"

    return creative


# ── Prompt builder ────────────────────────────────────────────────────────────

def _build_prompt(brand, product, persona, context, optimization=None) -> str:
    pdata = persona.get("persona_data", {})
    fmt_prefs  = _top3(pdata.get("format_preferences", {}))
    copy_prefs = _top3(pdata.get("copy_preferences", {}))
    tone_prefs = _top3(pdata.get("tone_preferences", {}))

    raw     = context.get("raw", {})
    derived = context.get("derived", {})
    loc     = raw.get("location", {})
    wx      = raw.get("weather", {})
    t       = raw.get("time", {})

    opt_section = ""
    if optimization:
        opt_section = f"""
OPTIMIZATION GUIDANCE:
Mode: {optimization.get('mode')}
Target visual format: {optimization.get('target_format')}
Target copy styles: {optimization.get('target_copy_styles')}
Target tone: {optimization.get('target_tone')}
Rationale: {optimization.get('rationale')}
If mode is "explore", DELIBERATELY pick content that differs from the user's proven preferences.
"""

    return f"""You are a Bangladesh-focused ad creative AI. Generate one short, contextual ad for the brand below, personalized to the user's exact moment. Pick the visual format and copy style that best fits the user's mood and brand voice — vary deliberately, do not default to 'try this product' framing. Always respond with valid JSON matching the schema. Never use generic phrases like 'best deals' or 'limited time' — every word must reference the specific context, persona, or brand voice.

BRAND:
Name: {brand.get('display_name')}
Tagline: {brand.get('tagline', '')}
Voice: {json.dumps(brand.get('voice_data', {}))}
Visual style: {json.dumps(brand.get('visual_data', {}))}
Constraints: {json.dumps(brand.get('constraints_data', {}))}

PRODUCT:
Name: {product.get('name')}
Category: {product.get('category')}
Description: {product.get('description', '')}
Reference image: {product.get('image_url') or 'none'}

USER:
Age: {persona.get('age')}
City: {persona.get('city')}
Language preference: {persona.get('language_preference')}
Spending tier: {persona.get('spending_tier')}
Top format preferences: {fmt_prefs}
Top copy preferences: {copy_prefs}
Top tone preferences: {tone_prefs}

CONTEXT:
Location: {loc.get('city', 'Dhaka')}
Weather: {wx.get('condition', 'clear')}, {wx.get('temp_c', 28)}°C, feels like {wx.get('feels_like', 28)}°C
Time: {t.get('time_bucket')} on a {t.get('day_of_week')} ({t.get('season')}, {t.get('meal_window')} window)
Mood: {derived.get('mood')}
Cultural moment: {derived.get('cultural_moment')}
Comfort need: {derived.get('comfort_need')}
Activity: {derived.get('activity_likelihood')}
Tone suggestion: {derived.get('tone_suggestion')}
{opt_section}
ALLOWED VALUES — use ONLY these exact strings:
visual_format: static_image | gif_template | gif_ai_multiframe | animated_banner | video_mp4 | voice_audio
copy_styles (pick 1-2): joke_pun | cultural_reference | question_hook | stat_hook | inspirational_quote | urgency_driven | direct_offer | story_narrative | relatable_observation
tone (pick 1): warm_casual | playful_energetic | serious_premium | urgent_action | nostalgic_emotional | informative_helpful

LANGUAGE RULES:
- "english" → English only
- "banglish" → mix English + Bangla phonetically (e.g., "Gorom-er din, ekta cool mango lassi try kor!")
- "bangla" → short Bangla phrases woven in naturally (not full Bangla sentences)

VARIETY RULES:
- Headline: max 8 words, hooks the specific moment (weather, time, cultural cue, mood)
- If copy_styles includes "inspirational_quote" → populate "quote" field (5-10 aspirational words)
- If copy_styles includes "joke_pun" → populate "joke" field (one-liner)
- If copy_styles includes "cultural_reference" → populate "cultural_hook" field (1-sentence local reference: Pohela Boishakh, Eid, cricket, monsoon, rickshaw ride, hartal, iftar, etc.)
- gif_template → best for playful_energetic or late_night moods
- static_image → best for serious_premium, informative, or morning contexts
- animated_banner → moderate engagement contexts (evening browsing, weekend chill)
- voice_audio → only when activity suggests non-visual context

OUTPUT ONLY VALID JSON. No preamble. No code fences. No explanation outside the JSON.
{{
  "headline": "string, max 8 words",
  "subheadline": "string",
  "body_copy": "string, 1-2 sentences",
  "cta_text": "string, 2-4 words",
  "cta_urgency": "low | medium | high",
  "tone": "one of the tone options",
  "copy_styles": ["one or two from copy_styles options"],
  "visual_format": "one of visual_format options",
  "image_prompt": "detailed image generation prompt including brand colors, mood, product, scene",
  "color_mood": "describes overall color/aesthetic",
  "rationale": "1 sentence explaining the creative choice",
  "quote": null,
  "joke": null,
  "cultural_hook": null
}}"""


# ── LLM call ──────────────────────────────────────────────────────────────────

def generate_copy(brand, product, persona, context, optimization=None) -> dict:
    """Call Gemini, parse JSON. Retry once on parse failure. Fallback on error."""
    if not _GEMINI_API_KEY:
        logger.warning("No GEMINI_API_KEY — using deterministic fallback")
        return _deterministic_fallback(brand, product, persona, context)

    prompt = _build_prompt(brand, product, persona, context, optimization)

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{_GEMINI_MODEL}:generateContent?key={_GEMINI_API_KEY}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.85,
            "maxOutputTokens": 2048,
        },
        "thinkingConfig": {"thinkingBudget": 0},
    }

    for attempt in range(2):
        try:
            if attempt == 1:
                # Stricter retry instruction
                payload["contents"][0]["parts"][0]["text"] = (
                    "Return ONLY raw JSON matching the schema below. "
                    "No markdown, no code fences, no explanation.\n\n" + prompt
                )

            resp = httpx.post(url, json=payload, timeout=45.0)
            resp.raise_for_status()
            data = resp.json()

            parts = (
                data.get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [])
            )
            # Thinking models include parts with thought=True — skip those
            text = "".join(
                p.get("text", "")
                for p in parts
                if not p.get("thought", False)
            )
            creative = _parse_gemini_json(text)
            return _sanitise_creative(creative)

        except json.JSONDecodeError:
            if attempt == 0:
                logger.warning("Gemini returned non-JSON on attempt 1 — retrying")
                continue
            logger.error("Gemini returned non-JSON on retry — using fallback")
            return _deterministic_fallback(brand, product, persona, context)

        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            if status in (429, 503) and attempt == 0:
                logger.warning("Gemini %s — waiting 8s then retrying", status)
                time.sleep(8)
                continue
            logger.error("Gemini HTTP error %s: %s", status, exc)
            return _deterministic_fallback(brand, product, persona, context)

        except Exception as exc:
            logger.error("Gemini call failed: %s", exc)
            return _deterministic_fallback(brand, product, persona, context)

    return _deterministic_fallback(brand, product, persona, context)


# ── Image generation ──────────────────────────────────────────────────────────

def generate_image(image_prompt: str, brand_kit: dict, visual_format: str):
    """Return a Pollinations.ai URL. Returns None for voice_audio."""
    if visual_format in _SKIP_IMG_FMT:
        return None

    visual_data   = brand_kit.get("visual_data", {})
    primary       = visual_data.get("primary_color", "#333333")
    accent        = visual_data.get("accent_color", "#FFFFFF")
    visual_style  = visual_data.get("visual_style", "clean, professional")

    full_prompt = (
        f"{image_prompt}, brand colors {primary} and {accent}, "
        f"{visual_style}, high quality, professional advertising photography, "
        "clean composition, brand-safe, suitable for advertising"
    )

    if visual_format in _GIF_FORMATS:
        full_prompt += (
            ", cinematic motion, dynamic composition, animated feel, "
            "multi-frame sequence, vibrant action"
        )

    try:
        encoded = quote(full_prompt, safe="")
        url = _POLLINATIONS.format(prompt=encoded)
        # Validate the URL is reachable (HEAD request, short timeout)
        r = httpx.head(url, timeout=8.0, follow_redirects=True)
        if r.status_code < 400:
            return url
    except Exception as exc:
        logger.warning("Pollinations unreachable: %s", exc)

    # Fallback to product's own image
    return brand_kit.get("product_image_url")


# ── Master compose function ───────────────────────────────────────────────────

def compose_ad(brand_id, product_id, persona_id, context_obj, db,
               optimization=None) -> dict:
    """
    Fetches brand/product/persona from DB, generates copy + image,
    assembles and returns an ad dict ready for DB insertion.
    """
    # ── Fetch brand ───────────────────────────────────────────────────────────
    brand_row = db.execute(
        "SELECT * FROM brands WHERE brand_id=?", (brand_id,)
    ).fetchone()
    if not brand_row:
        raise ValueError(f"Brand '{brand_id}' not found")
    brand = dict(brand_row)
    for f in ("voice_data", "visual_data", "constraints_data"):
        brand[f] = json.loads(brand.get(f) or "{}")

    # ── Fetch product ─────────────────────────────────────────────────────────
    product_row = db.execute(
        "SELECT * FROM products WHERE product_id=?", (product_id,)
    ).fetchone()
    if not product_row:
        raise ValueError(f"Product '{product_id}' not found")
    product = dict(product_row)

    # ── Fetch persona ─────────────────────────────────────────────────────────
    persona_row = db.execute(
        "SELECT * FROM personas WHERE persona_id=?", (persona_id,)
    ).fetchone()
    if not persona_row:
        raise ValueError(f"Persona '{persona_id}' not found")
    persona = dict(persona_row)
    persona["persona_data"] = json.loads(persona.get("persona_data") or "{}")

    # ── Generate copy ─────────────────────────────────────────────────────────
    creative = generate_copy(brand, product, persona, context_obj, optimization)

    # ── Generate image ────────────────────────────────────────────────────────
    brand_kit = dict(brand)
    brand_kit["product_image_url"] = product.get("image_url")

    visual_format = creative.get("visual_format", "static_image")
    img_url = generate_image(
        creative.get("image_prompt", product.get("name", "")),
        brand_kit,
        visual_format,
    )

    # ── Assemble assets ───────────────────────────────────────────────────────
    assets_data = {
        "image_url": None,
        "gif_url":   None,
        "video_url": None,
        "voice_url": None,
    }
    if visual_format in _GIF_FORMATS:
        assets_data["gif_url"] = img_url
    elif visual_format == "video_mp4":
        assets_data["video_url"] = img_url
    elif visual_format != "voice_audio":
        assets_data["image_url"] = img_url

    # ── Build ad dict ─────────────────────────────────────────────────────────
    ad_id = f"ad_{uuid.uuid4().hex[:12]}"
    now   = datetime.now(timezone.utc).isoformat()

    return {
        "ad_id":      ad_id,
        "brand_id":   brand_id,
        "product_id": product_id,
        "persona_id": persona_id,
        "creative_data": {
            "headline":      creative.get("headline"),
            "subheadline":   creative.get("subheadline"),
            "body_copy":     creative.get("body_copy"),
            "cta_text":      creative.get("cta_text"),
            "cta_urgency":   creative.get("cta_urgency"),
            "color_mood":    creative.get("color_mood"),
            "quote":         creative.get("quote"),
            "joke":          creative.get("joke"),
            "cultural_hook": creative.get("cultural_hook"),
        },
        "assets_data": assets_data,
        "ad_tags": {
            "visual":      visual_format,
            "copy_styles": creative.get("copy_styles", ["direct_offer"]),
            "tone":        creative.get("tone", "warm_casual"),
        },
        "context_snapshot": context_obj,
        "optimization_metadata": {
            "mode":                    (optimization or {}).get("mode", "free"),
            "directive":               (optimization or {}).get("rationale", "LLM picks freely"),
            "user_profile_source":     "persona_preferences",
            "user_profile_confidence": None,
            "sample_size":             0,
            "rationale":               creative.get("rationale"),
            "image_prompt_used":       creative.get("image_prompt"),
        },
        "stage":      "real_time",
        "created_at": now,
    }
