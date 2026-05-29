const BASE_URL = 'http://localhost:8000';

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${path} failed (${res.status}): ${text}`);
  }
  return res.json();
}

export function listBrands() {
  return request('/api/brands');
}

export function getBrand(brandId) {
  return request(`/api/brands/${brandId}`);
}

export function createBrand(formData) {
  return request('/api/brands', { method: 'POST', body: formData });
}

export function getBrandProducts(brandId) {
  return request(`/api/brands/${brandId}/products`);
}

export function addProduct(brandId, formData) {
  return request(`/api/brands/${brandId}/products`, { method: 'POST', body: formData });
}

export function getBrandPerformance(brandId) {
  return request(`/api/brands/${brandId}/performance`);
}

export function getBrandTopAds(brandId) {
  return request(`/api/brands/${brandId}/top-ads`);
}
