"""
Seeds the database with personas, brands, and products.
Idempotent — safe to run multiple times.
Does NOT seed ads or conversion events (Phase 3+).
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database import get_connection, init_db

DATA_DIR = Path(__file__).parent.parent.parent / "data"
SEED_TIMESTAMP = "2026-05-29T00:00:00Z"

# ── Brand kit data ────────────────────────────────────────────────────────────

BRANDS = [
    {
        "brand_id": "brand_pran_001",
        "display_name": "PRAN",
        "tagline": "Quality Always",
        "description": (
            "Bangladesh's leading food and beverage brand, trusted by families for "
            "decades. Known for quality juices, snacks, and groceries made from "
            "locally sourced ingredients."
        ),
        "logo_url": "/static/logos/pran.png",
        "voice_data": {
            "tone": "warm_family",
            "personality": "trustworthy, reliable, wholesome",
            "language_style": "bangla_mix",
            "key_messages": [
                "Quality always",
                "Made for Bangladeshi families",
                "Pure and natural",
            ],
        },
        "visual_data": {
            "primary_color": "#e30613",
            "accent_color": "#f9a01b",
            "secondary_color": "#ffffff",
            "style": "bold_vibrant",
        },
        "constraints_data": {
            "avoid_topics": ["competitor_brands", "unhealthy_habits"],
            "avoid_tones": ["edgy", "dark"],
            "max_price_mention": True,
        },
    },
    {
        "brand_id": "brand_daraz_001",
        "display_name": "Daraz",
        "tagline": "It's shopping o'clock",
        "description": (
            "Bangladesh's largest e-commerce platform. Millions of products, fast "
            "delivery, and unbeatable deals — from electronics to fashion, delivered "
            "to your door."
        ),
        "logo_url": "/static/logos/daraz.png",
        "voice_data": {
            "tone": "exciting_deals",
            "personality": "energetic, tech-savvy, deal-oriented",
            "language_style": "banglish",
            "key_messages": [
                "Best deals online",
                "Fast delivery",
                "Millions of products",
            ],
        },
        "visual_data": {
            "primary_color": "#f85c00",
            "accent_color": "#ffffff",
            "secondary_color": "#333333",
            "style": "clean_modern",
        },
        "constraints_data": {
            "avoid_topics": ["failed_deliveries", "counterfeit_products"],
            "avoid_tones": ["passive", "slow"],
            "max_price_mention": True,
        },
    },
    {
        "brand_id": "brand_foodpanda_001",
        "display_name": "foodpanda",
        "tagline": "Good food. Good life.",
        "description": (
            "Bangladesh's favourite food delivery app. Order from hundreds of "
            "restaurants and get your food delivered in 30 minutes or less."
        ),
        "logo_url": "/static/logos/foodpanda.png",
        "voice_data": {
            "tone": "playful_hungry",
            "personality": "fun, casual, food-loving",
            "language_style": "banglish",
            "key_messages": [
                "Order now, eat now",
                "From your favourite restaurants",
                "Delivered fast",
            ],
        },
        "visual_data": {
            "primary_color": "#d70f64",
            "accent_color": "#ffffff",
            "secondary_color": "#ff6b9d",
            "style": "playful_rounded",
        },
        "constraints_data": {
            "avoid_topics": ["diet_culture", "unhealthy_guilt"],
            "avoid_tones": ["formal", "serious"],
            "max_price_mention": False,
        },
    },
    {
        "brand_id": "brand_bkash_001",
        "display_name": "bKash",
        "tagline": "Send money, feel free",
        "description": (
            "Bangladesh's most trusted mobile financial service. Send money, pay "
            "bills, recharge mobiles, and shop online — instantly and securely."
        ),
        "logo_url": "/static/logos/bkash.png",
        "voice_data": {
            "tone": "trustworthy_empowering",
            "personality": "reliable, accessible, empowering",
            "language_style": "bangla_mix",
            "key_messages": [
                "Send money instantly",
                "Safe and secure",
                "Bangladesh's most trusted mobile bank",
            ],
        },
        "visual_data": {
            "primary_color": "#e2136e",
            "accent_color": "#ffffff",
            "secondary_color": "#9b0080",
            "style": "professional_clean",
        },
        "constraints_data": {
            "avoid_topics": ["fraud", "system_downtime"],
            "avoid_tones": ["casual_jokes", "complex_jargon"],
            "max_price_mention": True,
        },
    },
    {
        "brand_id": "brand_mezbaan_001",
        "display_name": "Mezbaan",
        "tagline": "Taste of Home",
        "description": (
            "A beloved Dhaka restaurant since 1985, serving authentic Bangladeshi "
            "cuisine from fresh halal ingredients and traditional family recipes "
            "passed down through generations."
        ),
        "logo_url": "/static/logos/mezbaan.png",
        "voice_data": {
            "tone": "authentic_warm",
            "personality": "traditional, family-owned, proud Bangladeshi",
            "language_style": "bangla",
            "key_messages": [
                "Taste of home",
                "Original recipes since 1985",
                "Fresh halal ingredients daily",
            ],
        },
        "visual_data": {
            "primary_color": "#8b4513",
            "accent_color": "#f4a460",
            "secondary_color": "#fff8e7",
            "style": "traditional_warm",
        },
        "constraints_data": {
            "avoid_topics": ["fast_food_comparison", "western_food"],
            "avoid_tones": ["corporate", "impersonal"],
            "max_price_mention": True,
        },
    },
]

# ── Products per brand ────────────────────────────────────────────────────────

PRODUCTS = {
    "brand_pran_001": [
        {
            "product_id": "prod_pran_001",
            "name": "PRAN Mango Juice 250ml",
            "category": "beverage",
            "description": (
                "Refreshing mango juice made from Bangladeshi Fazli mangoes. "
                "No artificial preservatives. Perfect for hot summer days and lunchboxes."
            ),
            "image_url": "/uploads/products/sample_pran_mango.jpg",
            "target_audience": {
                "age_range": "all",
                "occupation": ["student", "family", "working_professional"],
                "city": ["Dhaka", "Chittagong", "Sylhet", "Rajshahi"],
                "dietary": ["halal", "none"],
            },
        },
        {
            "product_id": "prod_pran_002",
            "name": "PRAN Chanachur Masala",
            "category": "snack",
            "description": (
                "Crispy, spicy chanachur mix with a signature blend of Bangladeshi spices. "
                "The ultimate tea-time snack — comes in small, medium, and party packs."
            ),
            "image_url": "/uploads/products/sample_pran_chanachur.jpg",
            "target_audience": {
                "age_range": "13-45",
                "occupation": ["student", "family"],
                "city": ["Dhaka", "Chittagong", "Sylhet", "Rajshahi"],
                "dietary": ["halal", "none"],
            },
        },
        {
            "product_id": "prod_pran_003",
            "name": "PRAN Mustard Oil 1L",
            "category": "grocery",
            "description": (
                "Pure cold-pressed mustard oil from locally grown seeds. "
                "Essential for authentic Bangladeshi cooking — bharta, curry, and frying."
            ),
            "image_url": "/uploads/products/sample_pran_mustard_oil.jpg",
            "target_audience": {
                "age_range": "25-65",
                "occupation": ["family", "working_professional"],
                "city": ["Dhaka", "Chittagong", "Sylhet", "Rajshahi"],
                "dietary": ["halal", "none"],
            },
        },
        {
            "product_id": "prod_pran_004",
            "name": "PRAN Coconut Cookies",
            "category": "snack",
            "description": (
                "Light, crunchy coconut-flavored cookies with a hint of vanilla. "
                "A favorite after-school snack for children across Bangladesh."
            ),
            "image_url": "/uploads/products/sample_pran_cookies.jpg",
            "target_audience": {
                "age_range": "5-30",
                "occupation": ["student", "family"],
                "city": ["Dhaka", "Chittagong", "Sylhet", "Rajshahi"],
                "dietary": ["halal", "none"],
            },
        },
    ],
    "brand_daraz_001": [
        {
            "product_id": "prod_daraz_001",
            "name": "Flash Sale — Smartphones",
            "category": "electronics",
            "description": (
                "Up to 40% off on top smartphone brands — Samsung, Xiaomi, Realme. "
                "Limited stock. Flash sale every Friday noon."
            ),
            "image_url": "/uploads/products/sample_daraz_phones.jpg",
            "target_audience": {
                "age_range": "18-40",
                "occupation": ["student", "working_professional", "traveler"],
                "city": ["Dhaka", "Chittagong"],
                "dietary": [],
            },
        },
        {
            "product_id": "prod_daraz_002",
            "name": "Summer Fashion Collection",
            "category": "fashion",
            "description": (
                "Trendy summer outfits and accessories for men and women. "
                "Lightweight fabrics perfect for the BD heat — new arrivals daily."
            ),
            "image_url": "/uploads/products/sample_daraz_fashion.jpg",
            "target_audience": {
                "age_range": "15-35",
                "occupation": ["student", "working_professional"],
                "city": ["Dhaka", "Chittagong", "Rajshahi"],
                "dietary": [],
            },
        },
        {
            "product_id": "prod_daraz_003",
            "name": "Home Essentials Bundle",
            "category": "home_essentials",
            "description": (
                "Everything for your home — cookware, storage solutions, and cleaning "
                "supplies. Great value, delivered to your door within 48 hours."
            ),
            "image_url": "/uploads/products/sample_daraz_home.jpg",
            "target_audience": {
                "age_range": "25-55",
                "occupation": ["family", "working_professional"],
                "city": ["Dhaka", "Chittagong", "Sylhet", "Rajshahi"],
                "dietary": [],
            },
        },
        {
            "product_id": "prod_daraz_004",
            "name": "Student Stationery Pack",
            "category": "stationery",
            "description": (
                "Complete stationery bundle — notebooks, pens, highlighters, and a "
                "backpack. SSC/HSC exam season special at student-friendly prices."
            ),
            "image_url": "/uploads/products/sample_daraz_stationery.jpg",
            "target_audience": {
                "age_range": "13-22",
                "occupation": ["student"],
                "city": ["Dhaka", "Chittagong", "Sylhet", "Rajshahi"],
                "dietary": [],
            },
        },
    ],
    "brand_foodpanda_001": [
        {
            "product_id": "prod_fpanda_001",
            "name": "Kacchi Biryani Special",
            "category": "meal",
            "description": (
                "Authentic mutton kacchi biryani from Dhaka's top restaurants. "
                "Order before noon for guaranteed lunch delivery."
            ),
            "image_url": "/uploads/products/sample_fpanda_biryani.jpg",
            "target_audience": {
                "age_range": "18-55",
                "occupation": ["student", "working_professional", "family"],
                "city": ["Dhaka", "Chittagong"],
                "dietary": ["halal"],
            },
        },
        {
            "product_id": "prod_fpanda_002",
            "name": "Iftar Combo Pack",
            "category": "meal",
            "description": (
                "A complete iftar spread — dates, sharbat, beguni, chhola, and mains. "
                "Pre-order by 3pm for guaranteed iftar delivery. Ramadan exclusive."
            ),
            "image_url": "/uploads/products/sample_fpanda_iftar.jpg",
            "target_audience": {
                "age_range": "all",
                "occupation": ["student", "working_professional", "family"],
                "city": ["Dhaka", "Chittagong", "Sylhet", "Rajshahi"],
                "dietary": ["halal"],
            },
        },
        {
            "product_id": "prod_fpanda_003",
            "name": "Late Night Snacks Bundle",
            "category": "snack",
            "description": (
                "Paratha rolls, egg chop, and fries delivered after 10pm. "
                "For the night owls of Dhaka — available until 2am in select areas."
            ),
            "image_url": "/uploads/products/sample_fpanda_latenight.jpg",
            "target_audience": {
                "age_range": "18-30",
                "occupation": ["student", "working_professional"],
                "city": ["Dhaka"],
                "dietary": ["halal", "none"],
            },
        },
        {
            "product_id": "prod_fpanda_004",
            "name": "Office Lunch Set",
            "category": "meal",
            "description": (
                "Balanced lunch box — rice, dal, two curries, and salad from verified "
                "kitchens. Group order discounts available for 5+ people."
            ),
            "image_url": "/uploads/products/sample_fpanda_office_lunch.jpg",
            "target_audience": {
                "age_range": "22-45",
                "occupation": ["working_professional"],
                "city": ["Dhaka", "Chittagong"],
                "dietary": ["halal", "none"],
            },
        },
    ],
    "brand_bkash_001": [
        {
            "product_id": "prod_bkash_001",
            "name": "Send Money — Zero Fee",
            "category": "service",
            "description": (
                "Send money to any bKash account for free. Instant transfer, 24/7. "
                "No bank account needed — works from any mobile number."
            ),
            "image_url": "/uploads/products/sample_bkash_send.jpg",
            "target_audience": {
                "age_range": "18-65",
                "occupation": ["student", "working_professional", "family", "traveler"],
                "city": ["Dhaka", "Chittagong", "Sylhet", "Rajshahi"],
                "dietary": [],
            },
        },
        {
            "product_id": "prod_bkash_002",
            "name": "Mobile Recharge + 5% Cashback",
            "category": "service",
            "description": (
                "Recharge any mobile number via bKash and get 5% cashback instantly. "
                "Works for Grameenphone, Robi, Banglalink, and Teletalk."
            ),
            "image_url": "/uploads/products/sample_bkash_recharge.jpg",
            "target_audience": {
                "age_range": "15-45",
                "occupation": ["student", "working_professional"],
                "city": ["Dhaka", "Chittagong", "Sylhet", "Rajshahi"],
                "dietary": [],
            },
        },
        {
            "product_id": "prod_bkash_003",
            "name": "Utility Bill Payment",
            "category": "service",
            "description": (
                "Pay electricity, gas, water, and internet bills through bKash in "
                "seconds. No queue. No cash. No hassle."
            ),
            "image_url": "/uploads/products/sample_bkash_bills.jpg",
            "target_audience": {
                "age_range": "25-65",
                "occupation": ["family", "working_professional"],
                "city": ["Dhaka", "Chittagong", "Sylhet", "Rajshahi"],
                "dietary": [],
            },
        },
        {
            "product_id": "prod_bkash_004",
            "name": "Shop & Pay Online",
            "category": "service",
            "description": (
                "Pay on Daraz, Chaldal, Shajgoj, and 100+ partner apps with bKash. "
                "Secure one-tap checkout — no card needed."
            ),
            "image_url": "/uploads/products/sample_bkash_shop.jpg",
            "target_audience": {
                "age_range": "16-45",
                "occupation": ["student", "working_professional", "traveler"],
                "city": ["Dhaka", "Chittagong", "Rajshahi"],
                "dietary": [],
            },
        },
    ],
    "brand_mezbaan_001": [
        {
            "product_id": "prod_mezbaan_001",
            "name": "Mutton Kacchi Biryani",
            "category": "meal",
            "description": (
                "Mezbaan's signature slow-cooked mutton kacchi biryani. Marinated for "
                "12 hours in our secret blend of 22 spices. Served with borhani and salad."
            ),
            "image_url": "/uploads/products/sample_mezbaan_kacchi.jpg",
            "target_audience": {
                "age_range": "18-65",
                "occupation": ["family", "working_professional", "student"],
                "city": ["Dhaka"],
                "dietary": ["halal"],
            },
        },
        {
            "product_id": "prod_mezbaan_002",
            "name": "Ilish Macher Jhol",
            "category": "meal",
            "description": (
                "Fresh Padma river hilsa cooked in traditional mustard-green chili "
                "gravy. Seasonal dish — available July to October only."
            ),
            "image_url": "/uploads/products/sample_mezbaan_hilsa.jpg",
            "target_audience": {
                "age_range": "25-70",
                "occupation": ["family", "working_professional"],
                "city": ["Dhaka"],
                "dietary": ["halal", "none"],
            },
        },
        {
            "product_id": "prod_mezbaan_003",
            "name": "Family Platter (serves 10)",
            "category": "meal",
            "description": (
                "A full spread for the family — kacchi biryani, roast chicken, beef "
                "rezala, mixed salad, and borhani. Perfect for celebrations and get-togethers."
            ),
            "image_url": "/uploads/products/sample_mezbaan_family.jpg",
            "target_audience": {
                "age_range": "25-65",
                "occupation": ["family"],
                "city": ["Dhaka"],
                "dietary": ["halal"],
            },
        },
        {
            "product_id": "prod_mezbaan_004",
            "name": "Ramadan Iftar Box",
            "category": "meal",
            "description": (
                "Complete iftar for 4 — dates, sherbat, khichuri, beguni, halim, "
                "piyaju, and kheer. Pre-order by 12pm. Ramadan exclusive."
            ),
            "image_url": "/uploads/products/sample_mezbaan_iftar.jpg",
            "target_audience": {
                "age_range": "all",
                "occupation": ["family", "working_professional"],
                "city": ["Dhaka"],
                "dietary": ["halal"],
            },
        },
    ],
}


# ── Seed functions ────────────────────────────────────────────────────────────

def seed_personas(conn):
    with open(DATA_DIR / "demo_personas.json") as f:
        personas = json.load(f)

    cursor = conn.cursor()
    inserted = 0
    for p in personas:
        cursor.execute(
            """INSERT OR IGNORE INTO personas
               (persona_id, display_name, age, gender, city, occupation_mode,
                language_preference, dietary, spending_tier, persona_data)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                p["id"],
                p["display_name"],
                p["age"],
                p.get("gender", "unspecified"),
                p["city"],
                p["occupation_mode"],
                p["language_preference"],
                p.get("dietary", "none"),
                p["spending_tier"],
                json.dumps(p),
            ),
        )
        inserted += cursor.rowcount
    conn.commit()
    return inserted, len(personas)


def seed_brands(conn):
    cursor = conn.cursor()
    inserted = 0
    for brand in BRANDS:
        cursor.execute(
            """INSERT OR IGNORE INTO brands
               (brand_id, display_name, tagline, description, logo_url,
                voice_data, visual_data, constraints_data, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                brand["brand_id"],
                brand["display_name"],
                brand.get("tagline"),
                brand.get("description"),
                brand.get("logo_url"),
                json.dumps(brand["voice_data"]),
                json.dumps(brand["visual_data"]),
                json.dumps(brand["constraints_data"]),
                SEED_TIMESTAMP,
            ),
        )
        inserted += cursor.rowcount
    conn.commit()
    return inserted, len(BRANDS)


def seed_products(conn):
    cursor = conn.cursor()
    total = sum(len(v) for v in PRODUCTS.values())
    inserted = 0
    for brand_id, products in PRODUCTS.items():
        for product in products:
            cursor.execute(
                """INSERT OR IGNORE INTO products
                   (product_id, brand_id, name, category, description,
                    image_url, target_audience, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    product["product_id"],
                    brand_id,
                    product["name"],
                    product["category"],
                    product.get("description"),
                    product.get("image_url"),
                    json.dumps(product.get("target_audience", {})),
                    SEED_TIMESTAMP,
                ),
            )
            inserted += cursor.rowcount
    conn.commit()
    return inserted, total


def print_counts(conn):
    cursor = conn.cursor()
    tables = ["personas", "brands", "products", "ads", "conversion_events",
              "user_patterns", "optimization_cycles"]
    print("\nFinal table counts:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table:<25} {count}")


if __name__ == "__main__":
    print("Initialising database schema...")
    init_db()

    conn = get_connection()

    print("Seeding personas...")
    ins, total = seed_personas(conn)
    print(f"  {ins} inserted, {total - ins} already existed  ({total} total)")

    print("Seeding brands...")
    ins, total = seed_brands(conn)
    print(f"  {ins} inserted, {total - ins} already existed  ({total} total)")

    print("Seeding products...")
    ins, total = seed_products(conn)
    print(f"  {ins} inserted, {total - ins} already existed  ({total} total)")

    print_counts(conn)
    conn.close()
    print("\nSeed complete.")
