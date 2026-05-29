import json
import uuid
from datetime import datetime, timezone
from typing import Optional


def _get_conn(db):
    """Returns db if provided, otherwise opens its own connection."""
    if db is not None:
        return db, False
    from database import get_connection
    return get_connection(), True


def log_conversion_event(
    ad_id: str,
    persona_id: str,
    brand_id: str,
    context: dict,
    ad_tags: dict,
    converted: bool,
    source: str,
    persona_snapshot: Optional[dict] = None,
    db=None,
) -> str:
    """Writes a conversion event to DB. Returns event_id."""
    conn, owned = _get_conn(db)
    event_id = f"evt_{uuid.uuid4().hex}"
    timestamp = datetime.now(timezone.utc).isoformat()

    conn.execute(
        """INSERT INTO conversion_events
           (event_id, timestamp, ad_id, brand_id, persona_id,
            context_snapshot, persona_snapshot, ad_tags, converted, conversion_source)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            event_id,
            timestamp,
            ad_id,
            brand_id,
            persona_id,
            json.dumps(context or {}),
            json.dumps(persona_snapshot or {}),
            json.dumps(ad_tags or {}),
            1 if converted else 0,
            source,
        ),
    )
    conn.commit()
    if owned:
        conn.close()
    return event_id


def get_events_for_brand(brand_id: str, limit: int = 1000, db=None) -> list:
    conn, owned = _get_conn(db)
    rows = conn.execute(
        """SELECT * FROM conversion_events WHERE brand_id = ?
           ORDER BY timestamp DESC LIMIT ?""",
        (brand_id, limit),
    ).fetchall()
    result = _deserialise_events(rows)
    if owned:
        conn.close()
    return result


def get_events_for_persona(persona_id: str, db=None) -> list:
    conn, owned = _get_conn(db)
    rows = conn.execute(
        "SELECT * FROM conversion_events WHERE persona_id = ? ORDER BY timestamp DESC",
        (persona_id,),
    ).fetchall()
    result = _deserialise_events(rows)
    if owned:
        conn.close()
    return result


def get_winning_patterns(
    brand_id: str,
    min_sample_size: int = 10,
    min_conversion_rate: float = 0.4,
    db=None,
) -> list:
    """Aggregates events into winning (segment × format × tone) combos."""
    conn, owned = _get_conn(db)
    rows = conn.execute(
        """SELECT
              JSON_EXTRACT(persona_snapshot, '$.age_bracket')   AS age_bracket,
              JSON_EXTRACT(persona_snapshot, '$.city')          AS city,
              JSON_EXTRACT(persona_snapshot, '$.occupation_mode') AS occupation,
              JSON_EXTRACT(ad_tags, '$.visual')                 AS visual_format,
              JSON_EXTRACT(ad_tags, '$.tone')                   AS tone,
              COUNT(*)                                           AS shown,
              SUM(converted)                                     AS converted,
              ROUND(SUM(converted) * 1.0 / COUNT(*), 3)         AS conversion_rate
           FROM conversion_events
           WHERE brand_id = ?
           GROUP BY age_bracket, city, occupation, visual_format, tone
           HAVING COUNT(*) >= ? AND conversion_rate >= ?
           ORDER BY conversion_rate DESC""",
        (brand_id, min_sample_size, min_conversion_rate),
    ).fetchall()
    result = [dict(r) for r in rows]
    if owned:
        conn.close()
    return result


def _deserialise_events(rows) -> list:
    result = []
    for r in rows:
        d = dict(r)
        for field in ("context_snapshot", "persona_snapshot", "ad_tags"):
            if d.get(field):
                try:
                    d[field] = json.loads(d[field])
                except (json.JSONDecodeError, TypeError):
                    pass
        result.append(d)
    return result
