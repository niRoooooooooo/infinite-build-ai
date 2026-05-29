import ConversionButtons from './ConversionButtons';

const BASE_URL = 'http://localhost:8000';
const PINK = '#D70F64';

function resolveUrl(url) {
  if (!url) return null;
  if (url.startsWith('http')) return url;
  return `${BASE_URL}${url}`;
}

export default function SponsoredAdCard({ ad }) {
  const brand = ad.brand || {};
  const creative = ad.creative_data || {};
  const assets = ad.assets_data || {};
  const imageUrl = resolveUrl(assets.gif_url || assets.image_url);
  const logoUrl = resolveUrl(brand.logo_url);

  return (
    <article className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      {/* Brand header row */}
      <div className="flex items-center justify-between px-4 py-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-white border border-gray-200 flex items-center justify-center overflow-hidden shrink-0 p-1">
            {logoUrl ? (
              <img
                src={logoUrl}
                alt={brand.display_name}
                className="w-full h-full object-contain"
                onError={(e) => { e.currentTarget.style.display = 'none'; }}
              />
            ) : (
              <span className="font-bold text-[11px]" style={{ color: PINK }}>
                {brand.display_name?.[0]?.toUpperCase()}
              </span>
            )}
          </div>
          <div>
            <p className="text-[14px] font-semibold text-gray-900">{brand.display_name || 'Brand'}</p>
            <p className="text-[11px] font-bold uppercase tracking-wider text-gray-400">Sponsored</p>
          </div>
        </div>
        <button className="text-gray-400 hover:text-gray-600 transition-colors p-1">
          <span className="material-symbols-outlined text-[20px]">more_horiz</span>
        </button>
      </div>

      {/* Ad image */}
      {imageUrl && (
        <div className="w-full aspect-square bg-gray-100 overflow-hidden">
          <img
            src={imageUrl}
            alt={creative.headline || 'Sponsored'}
            className="w-full h-full object-cover"
            onError={(e) => { e.currentTarget.parentElement.style.display = 'none'; }}
          />
        </div>
      )}

      {/* Ad copy + conversion */}
      <div className="px-4 py-4 space-y-3">
        {creative.headline && (
          <h2 className="text-[17px] font-bold text-gray-900 leading-snug">{creative.headline}</h2>
        )}
        {creative.body_copy && (
          <p className="text-[14px] text-gray-500 leading-relaxed">{creative.body_copy}</p>
        )}
        <ConversionButtons ad={ad} />
      </div>
    </article>
  );
}
