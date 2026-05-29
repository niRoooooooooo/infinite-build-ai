const BASE_URL = 'http://localhost:8000';

export async function logConversion({ ad_id, persona_id, converted, source }) {
  const res = await fetch(`${BASE_URL}/api/events`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ad_id, persona_id, converted, source }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`logConversion failed (${res.status}): ${text}`);
  }
  return res.json();
}
