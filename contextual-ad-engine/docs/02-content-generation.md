# Master Document — Content Generation APIs

**Project:** Contextual Ad Intelligence Engine (Bangladesh-focused)
**Stage:** Hackathon MVP (1–3 day build)
**Scope of this document:** Content generation layer — all APIs and systems that produce ad creative (copy, images, video, voice, SEO content).

---

## 1. Purpose

This document specifies the full content generation stack. It covers what gets generated, when, by which API, and how the system decides between fast pre-generated content and slower real-time personalized content.

The Generation Layer receives a context object from the Data Collection Layer and outputs ad-ready creative in multiple formats.

---

## 2. Two-Stage Generation Architecture

This is the core architectural insight: **not all ads need to be generated in real time.**

```
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 1 — PRE-GENERATED LIBRARY (instant, <100ms delivery)     │
│                                                                  │
│  For every reasonable context combination, generate ads in       │
│  advance. Store in a queryable library. When a user shows up,    │
│  match their context to the nearest pre-generated ad.            │
│                                                                  │
│  Used for: first impression, third-party sites, cold contact     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                     [ User engages ]
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 2 — REAL-TIME PERSONALIZATION (3–10 seconds)             │
│                                                                  │
│  Once user shows intent (click, scroll, app open), generate      │
│  hyper-personalized content using full context + persona data.   │
│  This is where richer formats (video, voice, interactive) live.  │
│                                                                  │
│  Used for: in-app experiences, retargeting, deep engagement      │
└─────────────────────────────────────────────────────────────────┘
```

### Why this matters

| Issue | Real-time only | Two-stage |
|---|---|---|
| First-impression speed | 8–15 sec (terrible) | <100ms |
| API cost per impression | High | Pre-paid, amortized |
| Personalization depth | Limited by time budget | Deep (when it counts) |
| Failure resilience | One API down = no ad | Library always available |

---

## 3. Content Types & Generation Stages

| Content Type | Stage 1 (Pre-gen) | Stage 2 (Real-time) | Generation Time |
|---|---|---|---|
| **Headline + body copy** | ✓ | ✓ | 1–3 sec |
| **Static image ad** | ✓ | ✓ | 3–8 sec |
| **Hero quote / tagline** | ✓ | ✓ | 1–2 sec |
| **GIF (template-based)** | ✓ | ✓ | 1–3 sec |
| **GIF (AI multi-frame)** | ✓ | ✓ | 10–20 sec |
| **Animated banner (CSS/JS)** | ✓ | ✓ | 5–10 sec |
| **Short video (template MP4)** | ✓ | ✓ | 5–15 sec |
| **Generative video (AI)** | ✗ | ✓ | 30s–5min |
| **Voice ad / TTS** | ✓ | ✓ | 2–5 sec |
| **Joke / cultural hook** | ✓ | ✓ | 1–2 sec |
| **SEO meta + descriptions** | ✓ | ✓ | 1–3 sec |
| **Interactive elements** | ✗ | ✓ | varies |

**For MVP demo:** Focus on headline, body, static image, and GIF (template-based). Voice ad as a wow moment if time allows. Template MP4 as one demo example. Generative video stays as roadmap.

---

## 4. LLM APIs — The Copy & Reasoning Layer

The LLM is the brain. It writes copy, picks tone, decides angle, and orchestrates other generation.

### 4.1 Primary recommendation: Google Gemini

| Field | Detail |
|---|---|
| **API** | Gemini API (`gemini-2.0-flash` or `gemini-2.5-pro`) |
| **Auth** | API key (free from Google AI Studio) |
| **Free tier** | Generous: 15 RPM, 1500 requests/day for Flash |
| **Speed** | Flash: ~1–2 sec per call |
| **Cost (paid)** | Flash: ~$0.075 / 1M input tokens |
| **Strengths** | Free tier covers a hackathon easily; supports multimodal (text + image input) |
| **Priority** | MVP-primary |

### 4.2 Alternatives

| API | Free tier | Speed | Notes |
|---|---|---|---|
| **OpenAI GPT-4o-mini** | ~$5 free credit | Fast | Cheap, good quality |
| **Anthropic Claude (Haiku 4.5)** | API credit on signup | Fast | Strong reasoning, good for nuanced copy |
| **Groq (Llama 3.x)** | Free, very fast | Extremely fast (~0.5s) | Open-source models, great for high-volume Stage 1 pre-gen |
| **Together AI** | Free credits | Fast | Hosted open models |

**Recommendation for MVP:** Use Gemini Flash for everything. If you blow through the free tier, switch to Groq for pre-generation (it's fast and free).

### 4.3 What the LLM generates

For each ad request, one LLM call typically returns a structured JSON response containing:

```json
{
  "headline": "Heavy rain in Dhaka? Hot khichuri in 30 min.",
  "subheadline": "Comfort food for a cozy evening",
  "body_copy": "When the sky opens up, the kitchen stays closed. We've got you.",
  "cta_text": "Order now",
  "cta_urgency": "medium",
  "tone": "warm_casual",
  "language": "english_with_banglish_phrase",
  "image_prompt": "Steaming bowl of khichuri on a wooden table, rain visible through window, warm yellow lighting, cozy mood",
  "color_mood": "warm_amber",
  "rationale": "Rainy evening + comfort food + casual tone → emotional, weather-anchored hook"
}
```

That single structured response drives every other generation step.

### 4.4 Prompt template (the core prompt)

This is the master prompt that turns context into creative. Keep it in a file, version it, iterate on it.

```
You are a Bangladesh-focused ad creative AI. Generate an ad for the brand 
described below, personalized to the user context.

BRAND:
{brand_kit_json}

USER CONTEXT:
{context_object_json}

DERIVED INSIGHTS:
{derived_context_json}

REQUIREMENTS:
- Output strict JSON with these fields: headline, subheadline, body_copy, 
  cta_text, cta_urgency, tone, language, image_prompt, color_mood, rationale
- Headline: max 8 words, hooks the moment (weather/time/cultural reference)
- Language: match user's language_preference (English / Banglish / Bangla)
- Tone: align with brand voice + user mood
- Image prompt: detailed enough for an image model to generate brand-consistent visual
- Rationale: 1 sentence explaining your creative choice (this is shown to the brand, not the user)
- Never use generic phrases like "best deals" or "limited time" — be specific to context

OUTPUT ONLY THE JSON. No preamble.
```

---

## 5. Image Generation APIs — The Visual Layer

### 5.1 Primary recommendation: Google Imagen / Gemini

| Field | Detail |
|---|---|
| **API** | Gemini 2.5 Flash Image (via Gemini API) |
| **Auth** | Same Google API key as LLM |
| **Speed** | 3–6 sec |
| **Free tier** | Included in Gemini free quota |
| **Cost (paid)** | ~$0.039 per image |
| **Strengths** | Fast, single API for text + image, decent quality |
| **Priority** | MVP-primary |

### 5.2 Alternatives

| API | Speed | Cost | Notes |
|---|---|---|---|
| **OpenAI DALL-E 3** | 5–10 sec | $0.04–$0.08 | Highest quality copy-in-image |
| **Stability AI (SDXL via API)** | 3–5 sec | ~$0.01 | Cheap, good for volume |
| **Replicate (any open model)** | 5–15 sec | $0.001–$0.05 | Most flexible, slowest setup |
| **Together AI (FLUX)** | 2–5 sec | ~$0.01 | Fast and cheap, very good quality |
| **Pollinations.ai** | 3–8 sec | **Free, no key** | Great for hackathons, unlimited |
| **Leonardo.ai** | 5–10 sec | Free tier (150 tokens/day) | Brand-consistent images possible |

### 5.3 Hackathon recommendation

**Use Pollinations.ai or Together AI FLUX for the MVP.** Pollinations is genuinely free with no signup. FLUX via Together gives better quality if you have $5–10 to spend.

### 5.4 Image prompt strategy

The LLM (Section 4) generates the image prompt. Append brand-kit-derived modifiers automatically:

```
{llm_generated_prompt}, 
brand colors {brand_kit.primary_color} and {brand_kit.accent_color},
{brand_kit.visual_style},
high quality, professional product photography, 
clean composition, brand-safe, suitable for advertising
```

This keeps every generated image consistent with the brand even though the LLM is creative.

---

## 6. Motion Generation APIs — GIFs, Animations & Video

**Honest assessment:** True AI video generation is too slow and expensive for hackathon Stage 1. For MVP, use a tiered motion approach: GIFs for fast lightweight motion, template-based MP4 for richer demos, and true AI video only as a roadmap mention.

### 6.1 GIF generation (recommended primary motion format for MVP)

GIFs are the sweet spot for hackathon: lightweight, browser-native, no video player needed, social-platform-ready, and fast to generate. Every social channel (Facebook, Instagram, WhatsApp, Messenger) auto-plays GIFs without user action.

**Three ways to generate GIFs:**

#### Method A — AI image → multi-frame → GIF (best quality)

1. Use the LLM to generate 3–5 variation prompts (same scene, slight changes — different lighting, different angle, subtle motion).
2. Generate each frame via the image API (Pollinations, Together FLUX, etc.).
3. Composite into a GIF using a library.

**Libraries for compositing GIFs:**

| Tool | Platform | Speed | Notes |
|---|---|---|---|
| **gif.js** | Browser (JavaScript) | 2–5 sec | Pure JS, no backend needed |
| **Pillow (PIL)** | Python | 1–3 sec | Simplest backend option |
| **imageio** | Python | 1–3 sec | More format flexibility |
| **FFmpeg** | Server | 1–2 sec | Highest quality, smallest file size |

**Recommendation:** `gif.js` in the browser for live generation, or Python Pillow for pre-generation. Both are free, both are fast.

#### Method B — Single image + CSS/JS animation exported as GIF

1. Generate one static image via image API.
2. Apply CSS animations (Ken Burns zoom, text fade-in, parallax) in a hidden canvas.
3. Capture frames using MediaRecorder API or html2canvas + gif.js.
4. Export as GIF.

**Use case:** Animated banner ads with the brand logo, headline animating in, product zooming. Looks professional, takes 3–5 seconds to render.

#### Method C — Pre-built GIF templates with AI swap-ins

1. Have 5–10 pre-built GIF templates (animated backgrounds, motion graphics).
2. AI generates only the text overlay and one foreground product image.
3. Composite text and product onto the template GIF.

**Speed:** <2 seconds. **Quality:** Polished, brand-consistent. **Effort:** Highest upfront work, lowest per-ad cost.

**For MVP demo:** Method C with 3 templates is the sweet spot. Highest perceived quality for the time invested.

#### GIF cost summary

| Approach | Cost per GIF | Generation time |
|---|---|---|
| AI multi-frame (Method A) | $0.05–$0.15 (image API costs) | 10–20 sec |
| Animated single image (Method B) | $0.01–$0.05 | 5–10 sec |
| Template + swap-in (Method C) | $0.01 | 1–3 sec |

### 6.2 Template-based MP4 video (for richer demos)

For situations where GIF isn't enough (longer content, voiceover, complex motion), build short videos by compositing:

- A background image (AI-generated or stock)
- The brand logo
- Animated text overlay (the headline)
- A simple Ken Burns zoom or fade effect
- Optional voice track (from Section 7)

**Tools to do this in-browser or server-side:**

| Tool | Type | Cost | Speed |
|---|---|---|---|
| **FFmpeg** | Server-side video compositing | Free, open-source | 1–5 sec per video |
| **Remotion** | React-based programmatic video | Free, MIT | 3–10 sec |
| **Canvas API + MediaRecorder** | Browser-native | Free | Fast, limited |
| **Lottie** | Animated SVG/JSON | Free | Instant playback |

**Recommendation:** Use FFmpeg server-side with pre-built templates. AI generates the image and copy; FFmpeg composites them into a 5–10 second MP4. Same approach as Method C above but exporting MP4 instead of GIF.

### 6.3 Motion format decision matrix

| Channel | Best format | Why |
|---|---|---|
| Facebook / Instagram feed | GIF or MP4 | Both auto-play; GIF is lighter |
| WhatsApp / Messenger | GIF | Native, no player needed |
| Email | GIF | MP4 doesn't play in most email clients |
| In-app banner | GIF or Lottie | Lightweight, smooth |
| Story / Reel | MP4 (vertical) | Platform expects video |
| SMS / Push notification | Static image | Motion not supported |

**For the demo:** Show one of each format to prove multi-format generation. GIF for "social feed," MP4 for "story," static image for "SMS / banner."

### 6.4 True AI video (Stage 2 / roadmap)

Only mention these in your pitch. Do not attempt for MVP.

| API | Speed | Cost | Quality | Notes |
|---|---|---|---|---|
| **Google Veo (via Gemini API)** | 30s–2min | Paid | High | Latest, best quality |
| **Runway Gen-3** | 30s–2min | ~$0.05/sec | High | Industry standard |
| **Luma Dream Machine** | 1–3 min | Free tier limited | Good | Easiest API |
| **Pika Labs** | 1–2 min | Free tier | Good | Good for short clips |
| **Replicate (multiple models)** | varies | $0.01–$0.50 per video | Mixed | Flexible |
| **Sora (OpenAI)** | 1–5 min | Paid tier | Highest | Limited access |

**For the demo:** Mention these as Stage 2 capabilities. Show one pre-rendered demo video to demonstrate the vision. Do not generate live during the demo.

---

## 7. Voice / TTS APIs — The Audio Layer

Voice ads are an underused format and a great wow moment in a demo.

### 7.1 Recommended options

| API | Cost | Quality | Languages |
|---|---|---|---|
| **ElevenLabs** | 10,000 chars/month free | Excellent (most natural) | Bangla supported |
| **Google Cloud TTS** | 1M chars/month free | Very good | Bangla supported |
| **OpenAI TTS** | ~$15 per 1M chars | Very good | Multilingual |
| **Azure Speech** | 500K chars/month free | Very good | Bangla supported |
| **Web Speech API** | Free, browser-native | Decent | Browser-dependent |

**Recommendation for MVP:** ElevenLabs (best quality) or Google Cloud TTS (highest free tier, supports Bangla).

### 7.2 Use case in demo

After generating a text ad, click a "Voice version" button → 3-second TTS plays the headline. Costs nothing, looks impressive, demonstrates multimodality without building a video pipeline.

---

## 8. SEO Content Generation

SEO content is a different beast from ad copy — longer-form, keyword-optimized, search-intent-driven. The same LLM handles it with a different prompt.

### 8.1 What gets generated

- **Meta titles** (50–60 chars, keyword-front-loaded)
- **Meta descriptions** (140–160 chars, with CTA)
- **Product descriptions** (long-form, keyword-rich)
- **Category page intros** (200–400 words)
- **Blog post outlines** for content marketing
- **Schema markup suggestions** (FAQ, Product, Review)

### 8.2 SEO-specific tools (optional)

| Tool | Purpose | Cost |
|---|---|---|
| **DataForSEO** | Keyword data, SERP analysis | Paid (pay-per-use) |
| **Google Trends (unofficial APIs)** | Trending searches | Free |
| **Keyword Surfer (browser)** | Keyword research | Free |
| **Ahrefs API / SEMrush API** | Full SEO data | Expensive |

**For MVP:** Skip dedicated SEO APIs. Use the LLM to generate SEO content based on the brand's product + context. Mention "full SEO suite with keyword research" as a roadmap item.

### 8.3 SEO prompt template

```
Generate SEO content for the following product, optimized for Bangladesh 
search behavior:

PRODUCT: {product_info}
BRAND: {brand_name}
TARGET KEYWORDS: {keywords}
LOCAL CONTEXT: {city}, {language_preference}

Output JSON with:
- meta_title (max 60 chars)
- meta_description (max 160 chars)  
- h1_suggestion
- product_description (200 words)
- faq_pairs (3 Q&A pairs)
- alt_text_for_main_image

Use natural Bangladeshi English / Banglish where appropriate.
```

---

## 9. "Jokes, Quotes, Cultural Hooks" — The Engagement Layer

You mentioned wanting to generate jokes, quotes, and cultural hooks. This is smart — it makes ads feel less like ads.

These are all just LLM calls with different prompts. No separate API needed.

### 9.1 Content sub-types

| Type | Use case | Prompt focus |
|---|---|---|
| **Punny headline** | Catch attention | "Write a pun using {product} and {context}" |
| **Cultural reference** | Build local resonance | "Reference {bd_cultural_moment} naturally" |
| **Joke / one-liner** | Make it shareable | "Write a funny one-liner about {situation}" |
| **Inspirational quote** | Aspirational brands | "Quote-style line about {brand_value}" |
| **Question hook** | Engagement | "Open with a relatable question about {context}" |
| **Stat-based hook** | Authority | "Lead with a surprising stat about {category}" |

### 9.2 Implementation

Add a "creative_style" field to the LLM prompt. Vary it during pre-generation to build a diverse library. Vary it in real-time based on user engagement history.

---

## 10. Brand Kit System (Critical for Consistency)

Every generation call needs brand grounding. Build a brand kit structure that gets injected into every prompt.

### 10.1 Brand kit schema

```json
{
  "brand_id": "pran_001",
  "brand_name": "Pran",
  "tagline": "Quality always",
  "voice": {
    "tone": "friendly, trustworthy, family-oriented",
    "do_say": ["fresh", "authentic", "made for you"],
    "do_not_say": ["cheap", "discount", "fake"],
    "personality": "warm, practical, local hero"
  },
  "visual": {
    "primary_color": "#E63946",
    "accent_color": "#FFD60A",
    "secondary_color": "#1D3557",
    "logo_url": "/brands/pran/logo.png",
    "visual_style": "vibrant, photographic, lifestyle-focused",
    "typography": "bold sans-serif headlines, friendly body"
  },
  "products": [
    { "id": "p1", "name": "Mango Juice", "category": "beverage", "target": "young_family" },
    { "id": "p2", "name": "Frooto", "category": "beverage", "target": "youth" }
  ],
  "constraints": {
    "halal_only": true,
    "claims_allowed": ["natural", "fresh", "local"],
    "claims_forbidden": ["medicinal", "weight loss", "cures"]
  }
}
```

### 10.2 How it's injected

Every LLM call gets the brand kit prepended to the system prompt. Every image call gets brand colors and style appended. Every video composite uses the brand logo.

This is what produces "brand coherence at scale" — the exact phrase from the Track 1 judging criteria.

### 10.3 For MVP

Build 3–5 brand kits manually. Examples:
- One FMCG (Pran)
- One e-commerce (Daraz)
- One food delivery (Foodpanda)
- One fintech (bKash)
- One local restaurant (your choice)

This variety in the demo proves the system isn't hardcoded.

---

## 11. Pre-Generation Strategy (Stage 1)

For your MVP, pre-generate a library of ads before demo day. This solves the latency problem and gives you instant-feeling responses.

### 11.1 What to pre-generate

For each brand, generate ads across a matrix of contexts:

```
5 brands × 5 cities × 4 weather conditions × 4 time-of-day × 3 personas 
= 1200 unique ads
```

That's overkill for a demo. Realistic MVP:

```
3 brands × 3 cities × 3 weather × 3 time × 3 personas = 243 ads
```

Even more focused:

```
2 brands × 5 high-impact context combos = 10 ads pre-rendered for the demo
```

10 polished pre-rendered ads are better than 1000 mediocre ones.

### 11.2 Pre-generation script

A simple Python script:

1. Loop through all (brand, city, weather, time, persona) combinations
2. For each, build the context object
3. Call LLM → get structured creative
4. Call image API → get visual
5. Composite → save to library
6. Index by context fingerprint

Run this overnight on Day 1. By Day 2, you have a ready library.

### 11.3 Matching at display time

When a user shows up with context X, query the library for the closest match using a similarity score over context dimensions. Return in <100ms.

Fallback: if no close match exists, generate in real time (Stage 2).

---

## 12. Generation Cost Summary

| Component | API | Cost per call | MVP cost estimate |
|---|---|---|---|
| Text/copy LLM | Gemini Flash | ~$0.0001 | <$1 for full MVP |
| Image generation | Pollinations.ai | Free | $0 |
| Image generation (alt) | Together FLUX | ~$0.01 | $5–10 |
| GIF compositing (gif.js / Pillow / FFmpeg) | self-hosted | Free | $0 |
| Voice TTS | ElevenLabs free | Free (10K chars) | $0 |
| Video compositing | FFmpeg | Free | $0 |
| Generative video | Skipped for MVP | — | $0 |

**Total realistic MVP cost: $0–$10 for the full generation layer.**

Note: Sign up early. Some APIs (Google Gemini, ElevenLabs) take a few minutes to issue keys. Do this on Day 1 morning.

---

## 13. Integration Plan (For Build Team)

**Owner:** Backend / AI integration developer + Content/design teammate

**Day 1 — Foundation**
- Morning: Sign up for all API keys (Gemini, Pollinations or Together, ElevenLabs)
- Morning: Build `generateCopy(context, brandKit)` → calls Gemini, returns structured JSON
- Afternoon: Build `generateImage(prompt, brandKit)` → calls image API, returns image URL
- Afternoon: Build `compositeAd(copy, image, brandKit)` → produces final ad as HTML or PNG
- Evening: Test end-to-end. One context → one full ad with image.

**Day 2 — Library & polish**
- Morning: Write pre-generation script. Run it. Get 10–20 high-quality pre-rendered ads.
- Afternoon: Build library matching function (query by context, return nearest ad).
- Afternoon: Add voice TTS button as wow moment.
- Afternoon: Build GIF generation pipeline (template-based first, AI multi-frame if time permits).
- Evening: Build template-based "video" output (FFmpeg or Remotion) — one demo example only.

**Day 3 — Lock and demo prep**
- No new APIs. Polish what works. Pre-render any specific demo flows.

---

## 14. Output Schema (What the Generation Layer Produces)

Each generated ad is stored as:

```json
{
  "ad_id": "ad_2026052900001",
  "generated_at": "2026-05-29T15:00:00Z",
  "stage": "pre_generated",
  "brand_id": "pran_001",
  "context_fingerprint": "dhaka_hot_afternoon_young_student_summer",
  "creative": {
    "headline": "Hot day in Dhaka? Cool down with mango magic.",
    "subheadline": "Frooto. Made for the moment.",
    "body_copy": "When the sun won't quit, neither should you.",
    "cta_text": "Find at your nearest store",
    "tone": "playful_refreshing",
    "language": "english"
  },
  "assets": {
    "image_url": "/cache/ads/ad_2026052900001.png",
    "gif_url": "/cache/ads/ad_2026052900001.gif",
    "video_url": "/cache/ads/ad_2026052900001.mp4",
    "voice_url": "/cache/ads/ad_2026052900001.mp3"
  },
  "metadata": {
    "rationale": "Hot Dhaka afternoon + young persona → playful tone, refreshment angle",
    "estimated_quality_score": 8.2,
    "render_time_ms": 4200
  }
}
```

This object is what the frontend displays and what the Performance/Loyalty layer (next document) tracks.

---

## 15. Privacy & Safety in Generation

The LLM is given guidelines via system prompt:

- Never generate content that targets sensitive attributes (religion, health, sexuality)
- Never make unverifiable claims (medical benefits, exaggerated results)
- Respect brand `claims_forbidden` list
- Match `halal_only` and other dietary constraints
- Output must be respectful of Bangladeshi cultural norms (no inappropriate humor, modest imagery)

Build a simple validator that checks generated copy against a blocklist before display. This becomes a talking point: "Every ad passes brand-safety and culture-safety checks before serving."

---

## 16. Sections To Be Built (Separate Documents)

- ✅ Document 1: Data Collection APIs
- ✅ Document 2: Content Generation APIs (this document)
- **Document 3:** Performance Measurement & Loyalty Loop
- **Document 4:** Optimization & Pattern Learning
- **Document 5:** Frontend / UI Architecture
- **Document 6:** Demo Flow & Pitch Script

---

## 17. Open Decisions for Your Team

Before building, your team needs to agree on:

1. **Primary LLM:** Gemini Flash (recommended) or alternative?
2. **Primary image API:** Pollinations (free, decent) or Together FLUX (paid, better quality)?
3. **GIF method:** Template-based swap-in (fastest), CSS animation capture (moderate), or AI multi-frame (best quality)?
4. **Include voice in MVP?** Yes/no — affects build time by ~2 hours
5. **Include template MP4 video in MVP?** Yes/no — affects build time by ~4 hours
6. **Pre-generation library size:** 10 hand-picked or 100+ matrix-generated?

My recommendation: Gemini Flash + Pollinations + GIF via template swap-in + voice yes + one template MP4 as demo example only + 10 hand-picked pre-rendered ads. This is the realistic 1–3 day build.
