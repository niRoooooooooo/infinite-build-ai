# Master Document — Frontend & UI Architecture

**Project:** Contextual Ad Intelligence Engine (Bangladesh-focused)
**Stage:** Hackathon MVP (1–3 day build)
**Scope of this document:** The two user interfaces — Interface A (consumer view) and Interface B (brand management). Component structure, screen layouts, file paths, image upload, and how the two interfaces connect.

---

## 1. Purpose

The system has two distinct user-facing interfaces, each serving a different audience:

- **Interface A:** Consumer view — shows ads as end users would see them, in a realistic feed
- **Interface B:** Brand management — where brands set up their identity, upload products, and view performance

Both interfaces share the same backend, the same data, and the same generated ads. They are two views into one system.

---

## 2. Architectural Overview

```
┌─────────────────────────────────────────────────────────────┐
│  Shared Backend                                              │
│  - Brand database                                            │
│  - Personas                                                  │
│  - Conversion events                                         │
│  - Generated ad library                                      │
│  - Optimization patterns                                     │
└─────────────────────────────────────────────────────────────┘
              ↑                              ↑
              │                              │
┌─────────────────────────┐    ┌──────────────────────────────┐
│  INTERFACE A             │    │  INTERFACE B                  │
│  Consumer Feed View       │    │  Brand Management             │
│                           │    │                                │
│  - Persona switcher       │    │  - Brand grid (all brands)    │
│  - Personalized feed       │    │  - Brand block (per brand)    │
│  - Sponsored ad cards      │    │    - Identity / kit            │
│  - "Take offer" / "Skip"   │    │    - Products (with images)    │
│                           │    │    - Performance / attribution │
│                           │    │  - Add new brand               │
│                           │    │  - Generate ad now             │
│                           │    │  - Run optimization cycle      │
└─────────────────────────────┘    └────────────────────────────────┘
```

### 2.1 The connection between interfaces

When a user clicks "Take offer" on an ad in Interface A, the conversion event is logged. The brand block for that ad's brand in Interface B updates immediately:
- "Customers acquired" counter increments
- Performance section recalculates winning patterns
- Optimization can now incorporate this new data

This live connection is the demo's most compelling moment.

---

## 3. Tech Stack

**Recommended stack** (adjust if your team has stronger skills elsewhere):

| Layer | Tool | Why |
|---|---|---|
| Framework | React (via Vite) | Fast dev experience, easy team coordination |
| Styling | Tailwind CSS | Rapid polished UI in 3 days |
| State | React Context + hooks | No Redux complexity for MVP |
| Routing | React Router | Two top-level routes (`/consumer` and `/brand`) |
| Charts | Recharts | Simple charts for performance section |
| Forms | React Hook Form | Clean brand/product creation forms |
| Image upload | Standard `<input type="file">` + FormData | No external library needed |
| Icons | lucide-react | Clean icon set |

**Backend assumption** (matches previous documents):
- Python (FastAPI or Flask) or Node (Express) — your team's choice
- SQLite for storage
- File-based image storage for uploaded product images

---

## 4. Project Structure

```
/frontend/
├── public/
│   └── index.html
├── src/
│   ├── App.jsx                          # Main router
│   ├── main.jsx                          # Vite entry
│   ├── styles/
│   │   └── globals.css                   # Tailwind imports
│   ├── api/
│   │   ├── brands.js                     # Brand API client
│   │   ├── personas.js                   # Persona API client
│   │   ├── ads.js                        # Ad generation API client
│   │   ├── events.js                     # Conversion event API client
│   │   └── optimization.js               # Optimization API client
│   ├── context/
│   │   ├── PersonaContext.jsx            # Current persona state (Interface A)
│   │   └── BrandContext.jsx              # Current brand state (Interface B)
│   ├── interfaces/
│   │   ├── consumer/                     # Interface A
│   │   │   ├── ConsumerApp.jsx
│   │   │   ├── pages/
│   │   │   │   └── FeedPage.jsx
│   │   │   └── components/
│   │   │       ├── PersonaSwitcher.jsx
│   │   │       ├── Feed.jsx
│   │   │       ├── OrganicCard.jsx
│   │   │       ├── SponsoredAdCard.jsx
│   │   │       └── ConversionButtons.jsx
│   │   └── brand/                         # Interface B
│   │       ├── BrandApp.jsx
│   │       ├── pages/
│   │       │   ├── BrandGridPage.jsx
│   │       │   └── BrandDetailPage.jsx
│   │       └── components/
│   │           ├── BrandBlock.jsx
│   │           ├── BrandIdentitySection.jsx
│   │           ├── ProductsSection.jsx
│   │           ├── ProductCard.jsx
│   │           ├── ProductUploadForm.jsx
│   │           ├── PerformanceSection.jsx
│   │           ├── AttributionMetrics.jsx
│   │           ├── TopAdsList.jsx
│   │           ├── GenerateAdButton.jsx
│   │           ├── OptimizationTrigger.jsx
│   │           ├── AdExplanationPanel.jsx
│   │           └── AddBrandForm.jsx
│   └── shared/
│       ├── components/
│       │   ├── AdPreview.jsx              # Renders a generated ad
│       │   ├── ImageUpload.jsx            # Reusable upload widget
│       │   ├── Modal.jsx
│       │   ├── ProgressIndicator.jsx
│       │   └── Button.jsx
│       └── utils/
│           ├── formatDate.js
│           └── formatCurrency.js
├── package.json
├── tailwind.config.js
└── vite.config.js
```

---

## 5. Routing

Two top-level routes split the two interfaces:

```jsx
// App.jsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import ConsumerApp from "./interfaces/consumer/ConsumerApp";
import BrandApp from "./interfaces/brand/BrandApp";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/brand" />} />
        <Route path="/consumer/*" element={<ConsumerApp />} />
        <Route path="/brand/*" element={<BrandApp />} />
      </Routes>
    </BrowserRouter>
  );
}
```

For the demo, judges navigate by clicking between the two routes. Add a small "switch interface" link at the top of each app so the navigation is obvious.

---

## 6. Interface A — Consumer Feed View

### 6.1 Purpose

Shows the personalized ad feed that an end user would see. Acts as the demo's "this is what users experience" view.

### 6.2 Single page

Interface A has one main page: `FeedPage.jsx`. No sub-navigation needed.

### 6.3 Page layout

```
┌─────────────────────────────────────────────────────────┐
│  HEADER                                                  │
│  [Logo]  [Switch to Brand View]  [Persona Switcher ▼]   │
├─────────────────────────────────────────────────────────┤
│  Active persona summary                                  │
│  "Rafi, 22, Dhaka, Student, Banglish speaker"           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [Organic content card]                                  │
│                                                          │
│  [SPONSORED — Brand X ad card with conversion buttons]   │
│                                                          │
│  [Organic content card]                                  │
│                                                          │
│  [Organic content card]                                  │
│                                                          │
│  [SPONSORED — Brand Y ad card with conversion buttons]   │
│                                                          │
│  [Organic content card]                                  │
│                                                          │
│  [SPONSORED — Brand X different ad with buttons]         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

Roughly: every 2–3 organic cards is followed by a sponsored card.

### 6.4 Components

#### 6.4.1 `PersonaSwitcher.jsx`

A dropdown listing all 5 demo personas. Selecting one updates `PersonaContext` and refreshes the feed.

```jsx
function PersonaSwitcher() {
  const { currentPersona, setPersona } = usePersona();
  const personas = usePersonaList();  // from API

  return (
    <select 
      value={currentPersona.id} 
      onChange={(e) => setPersona(e.target.value)}
    >
      {personas.map(p => (
        <option key={p.id} value={p.id}>
          {p.display_name} ({p.age}, {p.city})
        </option>
      ))}
    </select>
  );
}
```

#### 6.4.2 `Feed.jsx`

Fetches the feed for the current persona. The feed is a mixed list of organic content cards and sponsored ads.

```jsx
function Feed() {
  const { currentPersona } = usePersona();
  const [feedItems, setFeedItems] = useState([]);

  useEffect(() => {
    if (!currentPersona) return;
    
    async function loadFeed() {
      const organicCards = await fetchOrganicCards();
      const sponsoredAds = await fetchPersonalizedAds(currentPersona.id);
      const interleaved = interleaveFeed(organicCards, sponsoredAds);
      setFeedItems(interleaved);
    }
    
    loadFeed();
  }, [currentPersona]);

  return (
    <div className="feed">
      {feedItems.map((item, idx) =>
        item.type === "organic" 
          ? <OrganicCard key={idx} data={item} />
          : <SponsoredAdCard key={idx} ad={item} />
      )}
    </div>
  );
}
```

#### 6.4.3 `OrganicCard.jsx`

Static content cards that fill the feed between ads. For MVP, 10–15 hand-curated cards rotate. Examples:
- News-style headlines
- Recipe tips
- Local events
- Random posts

These exist purely to make the ads not feel like the only content.

**File:** `/data/organic_feed.json`

```json
[
  { "id": "org_001", "type": "news", "title": "Rain expected this weekend in Dhaka", "image": "/static/news1.jpg" },
  { "id": "org_002", "type": "recipe", "title": "5-minute khichuri tip", "image": "/static/recipe1.jpg" },
  { "id": "org_003", "type": "social", "title": "Friend posted a photo", "image": "/static/social1.jpg" },
  ...
]
```

#### 6.4.4 `SponsoredAdCard.jsx`

Renders a generated ad in the feed style. Includes a small "Sponsored" tag, the brand logo, the generated visual, the headline, and conversion buttons.

```jsx
function SponsoredAdCard({ ad }) {
  return (
    <article className="ad-card">
      <header className="ad-header">
        <img src={ad.brand.logo} className="brand-logo" />
        <span className="brand-name">{ad.brand.display_name}</span>
        <span className="sponsored-tag">Sponsored</span>
      </header>
      
      <AdPreview ad={ad} />
      
      <ConversionButtons ad={ad} />
    </article>
  );
}
```

#### 6.4.5 `AdPreview.jsx` (shared)

Renders the ad's visual asset. Auto-selects based on what's available:

```jsx
function AdPreview({ ad }) {
  if (ad.assets.gif_url) {
    return <img src={ad.assets.gif_url} alt={ad.creative.headline} />;
  }
  if (ad.assets.video_url) {
    return <video src={ad.assets.video_url} autoPlay loop muted />;
  }
  return <img src={ad.assets.image_url} alt={ad.creative.headline} />;
}
```

Below the visual, render the headline and CTA.

#### 6.4.6 `ConversionButtons.jsx`

The two-button conversion decision.

```jsx
function ConversionButtons({ ad }) {
  const { currentPersona } = usePersona();
  const [decided, setDecided] = useState(false);

  async function handleConvert(converted) {
    await api.logConversion({
      ad_id: ad.ad_id,
      persona_id: currentPersona.id,
      converted: converted,
      source: "live_interaction"
    });
    setDecided(converted ? "taken" : "skipped");
  }

  if (decided === "taken") return <p className="success">Offer claimed.</p>;
  if (decided === "skipped") return <p className="muted">Skipped.</p>;

  return (
    <div className="conversion-buttons">
      <button onClick={() => handleConvert(true)}>Take the offer</button>
      <button onClick={() => handleConvert(false)} className="secondary">Skip</button>
    </div>
  );
}
```

### 6.5 Ad selection logic

When the feed loads, the backend returns personalized ads. For MVP demo, the ad selection per slot is:

- **Pre-computed for demo predictability:** each persona has a curated list of 5–8 ads that will appear, in a known order
- **Sources from multiple brands:** so judges see brand diversity in the feed
- **All ads tagged with optimization metadata:** so the "Why this ad?" panel works

For production, the logic would be round-robin across brands with relevance scoring. Mention this as the production model in the pitch.

### 6.6 The "Why this ad?" panel (Interface A)

Optional, but powerful. A small expandable section below each ad:

```
[ Show why this ad → ]

(when expanded)
"Selected because: Hot Dhaka afternoon + Rafi's GIF preference.
Confidence: 78% based on 23 prior interactions."
```

This makes the system's intelligence visible to judges from the consumer side too.

---

## 7. Interface B — Brand Management

### 7.1 Purpose

Where brands set up their identity, manage products, and view performance. Multi-tenant: shows all brands as separate blocks.

### 7.2 Two pages

- **`BrandGridPage.jsx`** — main page with all brand blocks
- **`BrandDetailPage.jsx`** — expanded view of one brand

### 7.3 Brand Grid page layout

```
┌─────────────────────────────────────────────────────────┐
│  HEADER                                                  │
│  [Logo]  [Switch to Consumer View]                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Brands ({count})                              [+ Add]  │
│                                                          │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │  PRAN block      │  │  DARAZ block     │            │
│  └──────────────────┘  └──────────────────┘            │
│                                                          │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │  FOODPANDA block │  │  bKASH block     │            │
│  └──────────────────┘  └──────────────────┘            │
│                                                          │
│  ┌──────────────────┐                                   │
│  │  LOCAL RESTAURANT│                                   │
│  └──────────────────┘                                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

Click any brand block to expand into `BrandDetailPage`.

### 7.4 Brand Block component

This is the most important component in Interface B. It appears as a summary card on the grid page and as a fuller layout on the detail page.

#### 7.4.1 `BrandBlock.jsx` — summary mode (used on grid)

```
┌────────────────────────────────────────────┐
│  [LOGO]  PRAN                              │
│  "Quality always"                          │
├────────────────────────────────────────────┤
│  4 products                                │
│  Top: Mango Juice                          │
├────────────────────────────────────────────┤
│  89 customers acquired this week           │
│  Top ad: 47% conversion                    │
├────────────────────────────────────────────┤
│  [Manage →]                                │
└────────────────────────────────────────────┘
```

#### 7.4.2 `BrandBlock.jsx` — detail mode (used on detail page)

The full version contains:
- Identity section (logo, name, description, voice — editable)
- Products section (grid of product cards, "+ Add product" button)
- Performance section (attribution metrics, top ads, optimization controls)
- Live generation panel (generate a new ad for this brand now)

### 7.5 Brand identity section

#### 7.5.1 `BrandIdentitySection.jsx`

```jsx
function BrandIdentitySection({ brand, onEdit }) {
  return (
    <section className="brand-identity">
      <div className="logo-area">
        <img src={brand.logo_url} alt={brand.display_name} />
      </div>
      
      <div className="info">
        <h2>{brand.display_name}</h2>
        <p className="tagline">{brand.tagline}</p>
        <p className="description">{brand.description}</p>
        
        <div className="voice-tags">
          <span>Tone: {brand.voice.tone}</span>
          <span>Style: {brand.voice.personality}</span>
        </div>
        
        <div className="brand-colors">
          <div style={{ background: brand.visual.primary_color }} />
          <div style={{ background: brand.visual.accent_color }} />
          <div style={{ background: brand.visual.secondary_color }} />
        </div>
        
        <button onClick={onEdit}>Edit identity</button>
      </div>
    </section>
  );
}
```

### 7.6 Products section

#### 7.6.1 `ProductsSection.jsx`

A grid of product cards plus an "Add product" tile.

```jsx
function ProductsSection({ brand }) {
  const [products, setProducts] = useState(brand.products);
  const [showUploadForm, setShowUploadForm] = useState(false);

  return (
    <section className="products-section">
      <h3>Products ({products.length})</h3>
      
      <div className="products-grid">
        {products.map(p => (
          <ProductCard 
            key={p.id} 
            product={p} 
            onGenerateAd={() => generateAdForProduct(brand.brand_id, p.id)}
          />
        ))}
        
        <button 
          className="add-product-tile"
          onClick={() => setShowUploadForm(true)}
        >
          + Add product
        </button>
      </div>
      
      {showUploadForm && (
        <ProductUploadForm 
          brandId={brand.brand_id}
          onSubmit={(newProduct) => {
            setProducts([...products, newProduct]);
            setShowUploadForm(false);
          }}
          onCancel={() => setShowUploadForm(false)}
        />
      )}
    </section>
  );
}
```

#### 7.6.2 `ProductCard.jsx`

```jsx
function ProductCard({ product, onGenerateAd }) {
  return (
    <div className="product-card">
      <img src={product.image_url} alt={product.name} />
      <h4>{product.name}</h4>
      <p className="category">{product.category}</p>
      <p className="description">{product.description}</p>
      <button onClick={onGenerateAd} className="primary">
        Generate ad
      </button>
    </div>
  );
}
```

The "Generate ad" button is the most demo-critical interaction in Interface B. Clicking it generates a new ad in real time using the current brand kit and the system's optimization data.

#### 7.6.3 `ProductUploadForm.jsx`

The product upload form — **the form judges fill during the live demo** (per your spec).

```jsx
function ProductUploadForm({ brandId, onSubmit, onCancel }) {
  const [name, setName] = useState("");
  const [category, setCategory] = useState("");
  const [description, setDescription] = useState("");
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [uploading, setUploading] = useState(false);

  function handleImageChange(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    setImage(file);
    setImagePreview(URL.createObjectURL(file));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setUploading(true);
    
    const formData = new FormData();
    formData.append("brand_id", brandId);
    formData.append("name", name);
    formData.append("category", category);
    formData.append("description", description);
    formData.append("image", image);
    
    const newProduct = await api.uploadProduct(formData);
    setUploading(false);
    onSubmit(newProduct);
  }

  return (
    <form onSubmit={handleSubmit} className="product-upload-form">
      <h3>Add Product</h3>
      
      <label>
        Product name
        <input 
          type="text" 
          value={name} 
          onChange={(e) => setName(e.target.value)}
          required
          placeholder="e.g., Pran Mango Juice 1L"
        />
      </label>
      
      <label>
        Category
        <select 
          value={category} 
          onChange={(e) => setCategory(e.target.value)}
          required
        >
          <option value="">Select category</option>
          <option value="beverage">Beverage</option>
          <option value="snack">Snack</option>
          <option value="meal">Meal</option>
          <option value="grocery">Grocery</option>
          <option value="electronics">Electronics</option>
          <option value="fashion">Fashion</option>
          <option value="service">Service</option>
        </select>
      </label>
      
      <label>
        Description
        <textarea 
          value={description} 
          onChange={(e) => setDescription(e.target.value)}
          required
          placeholder="Describe the product, its appeal, target audience"
          rows={3}
        />
      </label>
      
      <label>
        Product image
        <input 
          type="file" 
          accept="image/*"
          onChange={handleImageChange}
          required
        />
      </label>
      
      {imagePreview && (
        <div className="image-preview">
          <img src={imagePreview} alt="Preview" />
        </div>
      )}
      
      <div className="form-actions">
        <button type="submit" disabled={uploading}>
          {uploading ? "Uploading..." : "Add product"}
        </button>
        <button type="button" onClick={onCancel}>Cancel</button>
      </div>
    </form>
  );
}
```

#### 7.6.4 Image upload backend

**Endpoint:** `POST /api/brands/{brand_id}/products`

**Backend handling:**

```python
@app.route("/api/brands/<brand_id>/products", methods=["POST"])
def upload_product(brand_id):
    name = request.form["name"]
    category = request.form["category"]
    description = request.form["description"]
    image_file = request.files["image"]
    
    # Generate unique filename
    ext = os.path.splitext(image_file.filename)[1]
    filename = f"{brand_id}_{uuid.uuid4().hex}{ext}"
    save_path = f"/uploads/products/{filename}"
    
    image_file.save(f".{save_path}")
    
    # Optionally: resize/optimize image
    optimize_image(f".{save_path}")
    
    product_id = generate_product_id()
    product = {
        "id": product_id,
        "brand_id": brand_id,
        "name": name,
        "category": category,
        "description": description,
        "image_url": save_path,
        "created_at": now()
    }
    
    save_product(product)
    return jsonify(product)
```

**Storage path:** `/uploads/products/` (served as static files)

### 7.7 Performance section

This is where the attribution story lives. **"You became our customer through this ad."**

#### 7.7.1 `PerformanceSection.jsx`

```jsx
function PerformanceSection({ brand }) {
  const [metrics, setMetrics] = useState(null);
  const [topAds, setTopAds] = useState([]);

  useEffect(() => {
    api.getBrandPerformance(brand.brand_id).then(data => {
      setMetrics(data.metrics);
      setTopAds(data.top_ads);
    });
  }, [brand]);

  if (!metrics) return <Loading />;

  return (
    <section className="performance-section">
      <h3>Performance</h3>
      
      <AttributionMetrics metrics={metrics} />
      
      <TopAdsList ads={topAds} />
      
      <RecommendationsPanel brandId={brand.brand_id} />
      
      <OptimizationTrigger brandId={brand.brand_id} />
    </section>
  );
}
```

#### 7.7.2 `AttributionMetrics.jsx`

The attribution-first display. Lead with customers, not impressions.

```jsx
function AttributionMetrics({ metrics }) {
  return (
    <div className="attribution-metrics">
      <div className="metric headline-metric">
        <span className="value">{metrics.customers_acquired}</span>
        <span className="label">customers acquired this week</span>
      </div>
      
      <div className="metric-row">
        <div className="metric">
          <span className="value">{metrics.total_ads_shown}</span>
          <span className="label">ads shown</span>
        </div>
        
        <div className="metric">
          <span className="value">{metrics.overall_conversion_rate}%</span>
          <span className="label">conversion rate</span>
        </div>
        
        <div className="metric">
          <span className="value">{metrics.best_segment}</span>
          <span className="label">best segment</span>
        </div>
      </div>
      
      <div className="segment-breakdown">
        <h4>Where customers came from:</h4>
        <ul>
          {metrics.segment_breakdown.map(s => (
            <li key={s.segment}>
              <span className="segment-name">{s.segment}</span>
              <span className="segment-percent">{s.percent}%</span>
              <div className="bar">
                <div className="fill" style={{ width: `${s.percent}%` }} />
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

#### 7.7.3 `TopAdsList.jsx`

```jsx
function TopAdsList({ ads }) {
  return (
    <div className="top-ads-list">
      <h4>Top performing ads</h4>
      {ads.map(ad => (
        <div key={ad.ad_id} className="top-ad-row">
          <div className="ad-thumb">
            <AdPreview ad={ad} />
          </div>
          <div className="ad-details">
            <p className="headline">{ad.creative.headline}</p>
            <p className="meta">
              {ad.conversion_rate}% conversion • 
              {ad.customers_acquired} customers acquired
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}
```

### 7.8 Generate ad now (live generation)

#### 7.8.1 `GenerateAdButton.jsx`

The "wow" interaction in Interface B. Brand picks a persona + product, clicks generate, sees a new ad appear in real time.

```jsx
function GenerateAdButton({ brand }) {
  const [selectedPersona, setSelectedPersona] = useState(null);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [generating, setGenerating] = useState(false);
  const [generatedAd, setGeneratedAd] = useState(null);

  async function handleGenerate() {
    setGenerating(true);
    setGeneratedAd(null);
    
    const ad = await api.generateAd({
      brand_id: brand.brand_id,
      product_id: selectedProduct.id,
      persona_id: selectedPersona.id
    });
    
    setGeneratedAd(ad);
    setGenerating(false);
  }

  return (
    <div className="generate-ad-panel">
      <h4>Generate ad now</h4>
      
      <PersonaSelector value={selectedPersona} onChange={setSelectedPersona} />
      <ProductSelector products={brand.products} value={selectedProduct} onChange={setSelectedProduct} />
      
      <button 
        onClick={handleGenerate} 
        disabled={!selectedPersona || !selectedProduct || generating}
      >
        {generating ? "Generating..." : "Generate ad"}
      </button>
      
      {generating && <ProgressIndicator />}
      
      {generatedAd && (
        <div className="generated-ad-result">
          <AdPreview ad={generatedAd} />
          <AdExplanationPanel ad={generatedAd} />
        </div>
      )}
    </div>
  );
}
```

#### 7.8.2 `AdExplanationPanel.jsx`

Shows the "Why this ad?" reasoning (from Document 4).

```jsx
function AdExplanationPanel({ ad }) {
  const meta = ad.optimization_metadata;
  
  return (
    <div className="ad-explanation">
      <h5>Why this ad?</h5>
      <ul>
        <li>Mode: {meta.mode} ({meta.mode === "exploit" ? "60% rule" : "40% rule"})</li>
        <li>Format: {ad.ad_tags.visual} ({meta.rationale})</li>
        <li>Tone: {ad.ad_tags.tone}</li>
        <li>Profile: {meta.user_profile_source}, confidence {meta.user_profile_confidence}</li>
        <li>Sample size: {meta.sample_size} prior interactions</li>
      </ul>
    </div>
  );
}
```

### 7.9 Optimization trigger

#### 7.9.1 `OptimizationTrigger.jsx`

From Document 4. The "Run weekly optimization cycle" button.

```jsx
function OptimizationTrigger({ brandId }) {
  const [running, setRunning] = useState(false);
  const [results, setResults] = useState(null);

  async function handleRun() {
    setRunning(true);
    const r = await api.runOptimizationCycle(brandId);
    setResults(r);
    setRunning(false);
  }

  return (
    <div className="optimization-trigger">
      <button onClick={handleRun} disabled={running}>
        {running ? "Running cycle..." : "Run weekly optimization cycle"}
      </button>
      
      {running && <ProgressIndicator steps={[
        "Extracting user patterns...",
        "Aggregating insights...",
        "Reshaping libraries...",
        "Generating recommendations..."
      ]} />}
      
      {results && (
        <div className="cycle-results">
          <p>Analyzed {results.events_processed} events.</p>
          <p>Updated {results.users_updated} user profiles.</p>
          <p>Generated {results.new_recommendations} recommendations.</p>
        </div>
      )}
    </div>
  );
}
```

### 7.10 Add new brand

#### 7.10.1 `AddBrandForm.jsx`

The form to register a new brand. Used during demo as "this is how a brand signs up." Pre-loaded brands fill the grid; live brand creation is optional.

```jsx
function AddBrandForm({ onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    display_name: "",
    tagline: "",
    description: "",
    voice_tone: "",
    primary_color: "#000000",
    accent_color: "#ffffff",
    logo: null,
  });

  async function handleSubmit(e) {
    e.preventDefault();
    
    const fd = new FormData();
    Object.entries(formData).forEach(([k, v]) => fd.append(k, v));
    
    const newBrand = await api.createBrand(fd);
    onSubmit(newBrand);
  }

  return (
    <form onSubmit={handleSubmit} className="add-brand-form">
      <h3>Register new brand</h3>
      
      <label>Brand name <input type="text" required onChange={e => setFormData({...formData, display_name: e.target.value})} /></label>
      <label>Tagline <input type="text" onChange={e => setFormData({...formData, tagline: e.target.value})} /></label>
      <label>Description <textarea onChange={e => setFormData({...formData, description: e.target.value})} /></label>
      <label>Voice / tone <input type="text" placeholder="warm, friendly, family-oriented" onChange={e => setFormData({...formData, voice_tone: e.target.value})} /></label>
      
      <div className="color-row">
        <label>Primary color <input type="color" onChange={e => setFormData({...formData, primary_color: e.target.value})} /></label>
        <label>Accent color <input type="color" onChange={e => setFormData({...formData, accent_color: e.target.value})} /></label>
      </div>
      
      <label>Logo <input type="file" accept="image/*" required onChange={e => setFormData({...formData, logo: e.target.files[0]})} /></label>
      
      <div className="form-actions">
        <button type="submit">Create brand</button>
        <button type="button" onClick={onCancel}>Cancel</button>
      </div>
    </form>
  );
}
```

---

## 8. Backend Endpoints (Frontend Touchpoints)

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/brands` | GET | List all brands |
| `/api/brands` | POST | Create new brand |
| `/api/brands/{id}` | GET | Get brand detail |
| `/api/brands/{id}` | PUT | Update brand |
| `/api/brands/{id}/products` | GET | List brand's products |
| `/api/brands/{id}/products` | POST | Add product (multipart with image) |
| `/api/brands/{id}/performance` | GET | Performance metrics |
| `/api/brands/{id}/top-ads` | GET | Top performing ads |
| `/api/personas` | GET | List demo personas |
| `/api/personas/{id}` | GET | Get persona detail |
| `/api/feed/{persona_id}` | GET | Personalized feed for persona |
| `/api/ads/generate` | POST | Generate ad on demand |
| `/api/events` | POST | Log conversion event |
| `/api/optimization/run-cycle` | POST | Run optimization cycle for brand |
| `/api/organic-feed` | GET | Static organic content cards |
| `/uploads/products/{filename}` | GET | Static-served product images |

---

## 9. Connection Between A and B (The Demo's Best Moment)

The two interfaces are wired live. A click in Interface A updates Interface B immediately.

### 9.1 Live update mechanism

For MVP, polling works fine. Interface B's performance section refetches every 5–10 seconds. When a judge clicks "Take offer" in A, B updates within seconds.

For production, you'd use WebSockets. Mention this as a production detail.

### 9.2 Demo sequence using this connection

1. Open both interfaces in adjacent browser tabs
2. In A: Browse feed as Rafi. Click "Take offer" on a Pran ad.
3. Switch to B: Pran's "customers acquired" counter has incremented
4. Switch back to A: Browse as Nusrat. Take a different brand's offer.
5. Switch to B: That brand's counter updates.

This back-and-forth is the most concrete demonstration of "the system works end-to-end."

---

## 10. Styling & Visual Polish

### 10.1 Visual identity

The system itself needs a brand. Pick:
- A primary color (recommend: deep purple, teal, or dark green — avoid clashing with brand demo colors)
- A clean font (Inter, Plus Jakarta Sans, or similar)
- Generous whitespace
- Soft shadows on cards

### 10.2 Interface A styling

Should feel like a real consumer app. References:
- Foodpanda's card grid
- Instagram's feed
- Facebook's news feed

Sponsored cards should look almost identical to organic cards — that's the "native ad" thesis in action.

### 10.3 Interface B styling

Should feel like a serious SaaS dashboard. References:
- Linear (clean, modern)
- Notion (organized, calm)
- Stripe Dashboard (data-dense but readable)

Brand blocks on the grid should feel like trading cards — visually distinct, easy to scan.

### 10.4 Mobile responsiveness

For MVP demo, design for desktop primarily. Add basic responsive breakpoints so it doesn't break on a tablet if a judge picks one up. Don't optimize for mobile — that's a v2 task.

---

## 11. State Management

### 11.1 Two context providers

```jsx
// PersonaContext.jsx — for Interface A
const PersonaContext = createContext();

export function PersonaProvider({ children }) {
  const [currentPersona, setCurrentPersona] = useState(null);
  const [personas, setPersonas] = useState([]);

  useEffect(() => {
    api.getPersonas().then(data => {
      setPersonas(data);
      setCurrentPersona(data[0]);  // default to first persona
    });
  }, []);

  return (
    <PersonaContext.Provider value={{ currentPersona, setCurrentPersona, personas }}>
      {children}
    </PersonaContext.Provider>
  );
}
```

```jsx
// BrandContext.jsx — for Interface B
const BrandContext = createContext();

export function BrandProvider({ children }) {
  const [brands, setBrands] = useState([]);
  const [currentBrand, setCurrentBrand] = useState(null);  // null = on grid page

  useEffect(() => {
    api.getBrands().then(setBrands);
  }, []);

  function refreshBrands() {
    api.getBrands().then(setBrands);
  }

  return (
    <BrandContext.Provider value={{ brands, currentBrand, setCurrentBrand, refreshBrands }}>
      {children}
    </BrandContext.Provider>
  );
}
```

No Redux or external state management needed for MVP.

---

## 12. Pre-loaded Demo Data (Critical for Demo Day)

Before the demo, the system should already contain:

### 12.1 Brands (5 pre-loaded)

1. **Pran** — FMCG, beverages and snacks, 4 products
2. **Daraz** — E-commerce, electronics and lifestyle, 4 products
3. **Foodpanda** — Food delivery, 4 restaurant partners as "products"
4. **bKash** — Fintech, services as products
5. **One local brand** — your choice (a Dhaka restaurant, a Chittagong clothing brand, etc.)

### 12.2 Products per brand (5–10 minimum total)

Each pre-loaded with:
- Name, category, description
- Real image (stock photo or actual brand product image)

### 12.3 Personas (5 pre-loaded — already defined in Document 3)

### 12.4 Conversion events (1000+ pre-seeded)

From Document 3's seed script. Ensures dashboards have meaningful data.

### 12.5 Organic feed cards (10–15)

Hand-curated for Interface A.

### 12.6 At least 30 pre-generated ads

From Document 2's pre-generation. Distributed across brands and personas.

**Build all this on Day 1–2 so Day 3 is purely polish and rehearsal.**

---

## 13. Integration Plan (For Build Team)

**Frontend developer ownership** with backend collaboration for endpoints.

### Day 1 — Skeleton
- Set up Vite + React + Tailwind project
- Build routing (`/consumer`, `/brand`)
- Build PersonaContext and BrandContext
- Build static layouts for FeedPage and BrandGridPage
- Connect to backend stubs

### Day 2 — Core components
- Morning: Interface B grid + BrandBlock summary
- Morning: BrandDetailPage with all sections
- Afternoon: ProductsSection + ProductCard + ProductUploadForm
- Afternoon: PerformanceSection + AttributionMetrics
- Evening: Interface A feed + SponsoredAdCard + ConversionButtons

### Day 3 — Polish & integration
- Wire live updates (polling)
- Add AdExplanationPanel everywhere relevant
- Add OptimizationTrigger
- Style pass — make it look polished, not student-project
- Test the connection between A and B
- Lock the code

---

## 14. Demo Flow Through the UI

For the 5-minute demo, the screen-by-screen sequence:

1. **Start on Interface B grid (10 sec)** — "Here are the brands using our system." Show 5 brand blocks.

2. **Click into Pran's block (30 sec)** — Walk through identity, products, performance. Highlight "89 customers acquired."

3. **Click "Generate ad" on a Pran product (45 sec)** — Pick Rafi as persona. Show ad generate live. Show "Why this ad?" panel.

4. **Switch to Interface A (45 sec)** — Login as Rafi. Browse feed. Find the Pran ad in the feed. Click "Take offer."

5. **Back to Interface B (30 sec)** — Show "customers acquired" counter has incremented. Show updated top ads.

6. **Click "Run optimization cycle" (45 sec)** — Show the cycle running. Show updated insights.

7. **Generate another ad for Rafi (30 sec)** — Show it's now biased toward his learned preferences. Show "Why this ad?" reflects the new data.

8. **Switch back to Interface A (15 sec)** — Login as Nusrat (different persona). Show her feed has completely different ads.

9. **Add a new product live (45 sec)** — In Interface B, upload a new product image, fill the form, submit. Show it appearing in the products grid. Generate an ad for it instantly.

10. **Close (15 sec)** — "Two interfaces, one intelligent system. Brands manage their products and see customer attribution. Users see ads that feel made for them — because they were."

Total: ~5 minutes. Every screen in the document is used. No screen is dead weight.

---

## 15. Documents Status

- ✅ Document 1: Data Collection APIs
- ✅ Document 2: Content Generation APIs
- ✅ Document 3: Performance Measurement & Conversion Loop
- ✅ Document 4: Optimization & Pattern Learning
- ✅ Document 5: Frontend / UI Architecture (this document)
- **Document 6:** Demo Flow & Pitch Script (next)

---

## 16. Open Decisions for Your Team

1. **Tech stack confirmed?** (React + Vite + Tailwind unless otherwise specified)
2. **Pre-loaded brands** — confirm the 5 brands list
3. **Live product upload in demo** — confirmed yes (per your spec)
4. **Live brand registration in demo** — yes/no? Recommend showing the form but not filling it live (slower than product upload).
5. **Polling vs WebSockets for live updates** — recommend polling for MVP.
