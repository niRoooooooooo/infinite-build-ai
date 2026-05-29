const BASE_URL = 'http://localhost:8000';

export async function runCycle(brandId) {
  const res = await fetch(`${BASE_URL}/api/optimization/run-cycle`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ brand_id: brandId }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`runCycle failed (${res.status}): ${text}`);
  }
  return res.json();
}
