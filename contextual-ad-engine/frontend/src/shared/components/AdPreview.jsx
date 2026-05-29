const BASE_URL = 'http://localhost:8000';

function resolveUrl(url) {
  if (!url) return null;
  if (url.startsWith('http')) return url;
  return `${BASE_URL}${url}`;
}

export default function AdPreview({ ad, compact = false }) {
  if (!ad) return null;

  const assets = ad.assets_data || ad.assets || {};
  const creative = ad.creative_data || ad.creative || {};
  const imageUrl = resolveUrl(assets.gif_url || assets.image_url);

  return (
    <div className="bg-white border border-outline-variant rounded-xl overflow-hidden">
      {imageUrl && (
        <div className={compact ? 'h-32' : 'aspect-[4/3]'}>
          <img
            src={imageUrl}
            alt={creative.headline || 'Ad preview'}
            className="w-full h-full object-cover"
          />
        </div>
      )}
      <div className="p-stack-md space-y-stack-xs">
        {creative.headline && (
          <h3 className="text-headline-sm font-semibold text-on-surface leading-snug">
            {creative.headline}
          </h3>
        )}
        {creative.body_copy && !compact && (
          <p className="text-body-sm text-on-surface-variant line-clamp-2">{creative.body_copy}</p>
        )}
        {creative.cta && (
          <button className="w-full mt-2 py-2.5 bg-primary text-on-primary rounded-lg text-label-md font-semibold hover:opacity-90 transition-opacity">
            {creative.cta}
          </button>
        )}
      </div>
    </div>
  );
}
