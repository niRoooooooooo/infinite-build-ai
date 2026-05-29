const BASE_URL = 'http://localhost:8000';

async function request(path) {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${path} failed (${res.status}): ${text}`);
  }
  return res.json();
}

export function getFeed(personaId) {
  return request(`/api/feed/${personaId}`);
}

export function getOrganicFeed() {
  return request('/api/organic-feed');
}
