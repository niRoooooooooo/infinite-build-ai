import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile

from database import get_db

router = APIRouter(prefix="/api/brands", tags=["brands"])

_UPLOADS = Path(__file__).parent.parent / "uploads" / "products"
_LOGOS   = Path(__file__).parent.parent / "uploads" / "logos"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _brand_row(row) -> dict:
    d = dict(row)
    for f in ("voice_data", "visual_data", "constraints_data"):
        if d.get(f):
            d[f] = json.loads(d[f])
    return d


def _product_row(row) -> dict:
    d = dict(row)
    if d.get("target_audience"):
        d["target_audience"] = json.loads(d["target_audience"])
    return d


def _require_brand(brand_id: str, db):
    if not db.execute("SELECT 1 FROM brands WHERE brand_id = ?", (brand_id,)).fetchone():
        raise HTTPException(404, f"Brand '{brand_id}' not found")


# ── Brand CRUD ────────────────────────────────────────────────────────────────

@router.get("")
def list_brands(db=Depends(get_db)):
    rows = db.execute("SELECT * FROM brands ORDER BY display_name").fetchall()
    return [_brand_row(r) for r in rows]


@router.post("", status_code=201)
async def create_brand(
    display_name: str = Form(...),
    brand_id:     str = Form(None),
    tagline:      str = Form(None),
    description:  str = Form(None),
    voice_tone:   str = Form("warm_casual"),
    primary_color:   str = Form("#000000"),
    accent_color:    str = Form("#ffffff"),
    secondary_color: str = Form("#888888"),
    logo: UploadFile = File(None),
    db=Depends(get_db),
):
    bid = brand_id or f"brand_{uuid.uuid4().hex[:8]}"
    logo_url = None

    if logo and logo.filename:
        _LOGOS.mkdir(parents=True, exist_ok=True)
        ext      = Path(logo.filename).suffix or ".png"
        filename = f"{bid}{ext}"
        (_LOGOS / filename).write_bytes(await logo.read())
        logo_url = f"/uploads/logos/{filename}"

    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        """INSERT INTO brands
           (brand_id, display_name, tagline, description, logo_url,
            voice_data, visual_data, constraints_data, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            bid, display_name, tagline, description, logo_url,
            json.dumps({"tone": voice_tone}),
            json.dumps({"primary_color": primary_color,
                        "accent_color": accent_color,
                        "secondary_color": secondary_color}),
            json.dumps({}),
            now,
        ),
    )
    db.commit()
    return _brand_row(db.execute("SELECT * FROM brands WHERE brand_id=?", (bid,)).fetchone())


@router.get("/{brand_id}")
def get_brand(brand_id: str, db=Depends(get_db)):
    row = db.execute("SELECT * FROM brands WHERE brand_id=?", (brand_id,)).fetchone()
    if not row:
        raise HTTPException(404, f"Brand '{brand_id}' not found")
    return _brand_row(row)


@router.put("/{brand_id}")
async def update_brand(brand_id: str, request: Request, db=Depends(get_db)):
    _require_brand(brand_id, db)
    body = await request.json()

    current = _brand_row(
        db.execute("SELECT * FROM brands WHERE brand_id=?", (brand_id,)).fetchone()
    )

    for field in ("display_name", "tagline", "description", "logo_url"):
        if field in body:
            current[field] = body[field]

    for field in ("voice_data", "visual_data", "constraints_data"):
        if field in body and isinstance(body[field], dict):
            current[field].update(body[field])

    db.execute(
        """UPDATE brands SET display_name=?, tagline=?, description=?,
           logo_url=?, voice_data=?, visual_data=?, constraints_data=?
           WHERE brand_id=?""",
        (
            current["display_name"], current["tagline"],
            current["description"],  current["logo_url"],
            json.dumps(current["voice_data"]),
            json.dumps(current["visual_data"]),
            json.dumps(current["constraints_data"]),
            brand_id,
        ),
    )
    db.commit()
    return current


# ── Products ──────────────────────────────────────────────────────────────────

@router.get("/{brand_id}/products")
def list_products(brand_id: str, db=Depends(get_db)):
    _require_brand(brand_id, db)
    rows = db.execute(
        "SELECT * FROM products WHERE brand_id=? ORDER BY name", (brand_id,)
    ).fetchall()
    return [_product_row(r) for r in rows]


@router.post("/{brand_id}/products", status_code=201)
async def upload_product(
    brand_id:    str,
    name:        str = Form(...),
    category:    str = Form(...),
    description: str = Form(None),
    image: UploadFile = File(None),
    db=Depends(get_db),
):
    _require_brand(brand_id, db)

    image_url = None
    if image and image.filename:
        _UPLOADS.mkdir(parents=True, exist_ok=True)
        ext      = Path(image.filename).suffix or ".jpg"
        filename = f"{brand_id}_{uuid.uuid4().hex}{ext}"
        (_UPLOADS / filename).write_bytes(await image.read())
        image_url = f"/uploads/products/{filename}"

    product_id = f"prod_{uuid.uuid4().hex[:10]}"
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        """INSERT INTO products
           (product_id, brand_id, name, category, description,
            image_url, target_audience, created_at)
           VALUES (?, ?, ?, ?, ?, ?, '{}', ?)""",
        (product_id, brand_id, name, category, description, image_url, now),
    )
    db.commit()
    return _product_row(
        db.execute("SELECT * FROM products WHERE product_id=?", (product_id,)).fetchone()
    )


# ── Performance ───────────────────────────────────────────────────────────────

@router.get("/{brand_id}/performance")
def get_performance(brand_id: str, db=Depends(get_db)):
    _require_brand(brand_id, db)

    row = db.execute(
        """SELECT COUNT(*) AS total, SUM(converted) AS total_converted
           FROM conversion_events WHERE brand_id=?""",
        (brand_id,),
    ).fetchone()

    total    = row["total"] or 0
    acquired = row["total_converted"] or 0
    rate     = round(acquired / total * 100, 1) if total else 0.0

    segs = db.execute(
        """SELECT JSON_EXTRACT(persona_snapshot, '$.occupation_mode') AS seg,
                  COUNT(*) AS shown, SUM(converted) AS converted
           FROM conversion_events WHERE brand_id=?
           GROUP BY seg ORDER BY converted DESC""",
        (brand_id,),
    ).fetchall()

    breakdown = []
    best_seg, best_rate = "N/A", 0.0
    for s in segs:
        sh = s["shown"] or 0
        cv = s["converted"] or 0
        sr = round(cv / sh * 100, 1) if sh else 0.0
        breakdown.append({"segment": s["seg"] or "unknown",
                           "shown": sh, "converted": cv, "percent": sr})
        if sr > best_rate:
            best_rate, best_seg = sr, (s["seg"] or "unknown")

    return {
        "brand_id":                brand_id,
        "customers_acquired":      acquired,
        "total_ads_shown":         total,
        "overall_conversion_rate": rate,
        "best_segment":            best_seg,
        "segment_breakdown":       breakdown,
    }


# ── Top ads ───────────────────────────────────────────────────────────────────

@router.get("/{brand_id}/top-ads")
def get_top_ads(brand_id: str, db=Depends(get_db)):
    _require_brand(brand_id, db)

    rows = db.execute(
        """SELECT e.ad_id,
                  COUNT(*) AS shown,
                  SUM(e.converted) AS customers_acquired,
                  ROUND(SUM(e.converted)*1.0/COUNT(*), 3) AS conversion_rate,
                  a.creative_data, a.assets_data, a.ad_tags
           FROM conversion_events e
           LEFT JOIN ads a ON e.ad_id = a.ad_id
           WHERE e.brand_id=?
           GROUP BY e.ad_id HAVING COUNT(*) >= 3
           ORDER BY conversion_rate DESC LIMIT 5""",
        (brand_id,),
    ).fetchall()

    result = []
    for r in rows:
        d = dict(r)
        for f in ("creative_data", "assets_data", "ad_tags"):
            if d.get(f):
                d[f] = json.loads(d[f])
        result.append(d)
    return result
