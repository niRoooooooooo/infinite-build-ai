const BASE_URL = 'http://localhost:8000';

async function request(path) {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${path} failed (${res.status}): ${text}`);
  }
  return res.json();
}

export function listPersonas() {
  return request('/api/personas');
}

export function getPersona(personaId) {
  return request(`/api/personas/${personaId}`);
}
