const BASE_URL = 'http://localhost:8000';

export async function generateAd({ brand_id, product_id, persona_id }) {
  const res = await fetch(`${BASE_URL}/api/ads/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ brand_id, product_id, persona_id }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`generateAd failed (${res.status}): ${text}`);
  }
  return res.json();
}
