import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "app.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS brands (
            brand_id        TEXT PRIMARY KEY,
            display_name    TEXT NOT NULL,
            tagline         TEXT,
            description     TEXT,
            logo_url        TEXT,
            voice_data      TEXT NOT NULL DEFAULT '{}',
            visual_data     TEXT NOT NULL DEFAULT '{}',
            constraints_data TEXT NOT NULL DEFAULT '{}',
            created_at      TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS products (
            product_id      TEXT PRIMARY KEY,
            brand_id        TEXT NOT NULL,
            name            TEXT NOT NULL,
            category        TEXT NOT NULL,
            description     TEXT,
            image_url       TEXT,
            target_audience TEXT NOT NULL DEFAULT '{}',
            created_at      TEXT NOT NULL,
            FOREIGN KEY (brand_id) REFERENCES brands(brand_id)
        );

        CREATE TABLE IF NOT EXISTS personas (
            persona_id          TEXT PRIMARY KEY,
            display_name        TEXT NOT NULL,
            age                 INTEGER NOT NULL,
            gender              TEXT NOT NULL DEFAULT 'unspecified',
            city                TEXT NOT NULL,
            occupation_mode     TEXT NOT NULL,
            language_preference TEXT NOT NULL,
            dietary             TEXT,
            spending_tier       TEXT NOT NULL,
            persona_data        TEXT NOT NULL DEFAULT '{}'
        );

        CREATE TABLE IF NOT EXISTS ads (
            ad_id                   TEXT PRIMARY KEY,
            brand_id                TEXT NOT NULL,
            product_id              TEXT,
            persona_id              TEXT,
            creative_data           TEXT NOT NULL DEFAULT '{}',
            assets_data             TEXT NOT NULL DEFAULT '{}',
            ad_tags                 TEXT NOT NULL DEFAULT '{}',
            context_snapshot        TEXT NOT NULL DEFAULT '{}',
            optimization_metadata   TEXT NOT NULL DEFAULT '{}',
            stage                   TEXT NOT NULL DEFAULT 'pre_generated',
            created_at              TEXT NOT NULL,
            FOREIGN KEY (brand_id)   REFERENCES brands(brand_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            FOREIGN KEY (persona_id) REFERENCES personas(persona_id)
        );

        CREATE TABLE IF NOT EXISTS conversion_events (
            event_id          TEXT PRIMARY KEY,
            timestamp         TEXT NOT NULL,
            ad_id             TEXT NOT NULL,
            brand_id          TEXT NOT NULL,
            persona_id        TEXT NOT NULL,
            context_snapshot  TEXT NOT NULL,
            persona_snapshot  TEXT NOT NULL,
            ad_tags           TEXT NOT NULL,
            converted         INTEGER NOT NULL,
            conversion_source TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS user_patterns (
            brand_id     TEXT NOT NULL,
            persona_id   TEXT NOT NULL,
            pattern_data TEXT NOT NULL DEFAULT '{}',
            confidence   REAL NOT NULL DEFAULT 0.3,
            sample_size  INTEGER NOT NULL DEFAULT 0,
            updated_at   TEXT NOT NULL,
            PRIMARY KEY (brand_id, persona_id)
        );

        CREATE TABLE IF NOT EXISTS optimization_cycles (
            cycle_id         TEXT PRIMARY KEY,
            brand_id         TEXT NOT NULL,
            week_number      INTEGER NOT NULL,
            events_processed INTEGER NOT NULL DEFAULT 0,
            users_updated    INTEGER NOT NULL DEFAULT 0,
            results_summary  TEXT NOT NULL DEFAULT '{}',
            completed_at     TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_products_brand   ON products(brand_id);
        CREATE INDEX IF NOT EXISTS idx_ads_brand        ON ads(brand_id);
        CREATE INDEX IF NOT EXISTS idx_ads_persona      ON ads(persona_id);
        CREATE INDEX IF NOT EXISTS idx_events_brand     ON conversion_events(brand_id);
        CREATE INDEX IF NOT EXISTS idx_events_persona   ON conversion_events(persona_id);
        CREATE INDEX IF NOT EXISTS idx_events_converted ON conversion_events(converted);
        CREATE INDEX IF NOT EXISTS idx_events_timestamp ON conversion_events(timestamp);
        CREATE INDEX IF NOT EXISTS idx_events_ad        ON conversion_events(ad_id);
        CREATE INDEX IF NOT EXISTS idx_patterns_persona ON user_patterns(persona_id);
        CREATE INDEX IF NOT EXISTS idx_cycles_brand     ON optimization_cycles(brand_id);
    """)
    conn.commit()
    conn.close()


def list_tables() -> list:
    conn = get_connection()
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables
