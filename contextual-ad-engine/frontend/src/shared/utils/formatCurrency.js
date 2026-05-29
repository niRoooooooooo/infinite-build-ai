export function formatNumber(n) {
  if (n === null || n === undefined) return '—';
  if (n >= 1000) return `${(n / 1000).toFixed(1)}k`;
  return String(n);
}

export function formatPercent(n, decimals = 1) {
  if (n === null || n === undefined) return '—';
  return `${Number(n).toFixed(decimals)}%`;
}
