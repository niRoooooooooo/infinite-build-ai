const BASE_URL = 'http://localhost:8000';

export default function TopAdsList({ ads = [] }) {
  if (ads.length === 0) {
    return (
      <div className="bg-surface-container-lowest border border-outline-variant rounded-xl p-stack-lg shadow-sm">
        <h4 className="text-label-md text-on-surface-variant uppercase tracking-wider mb-stack-md">Top performing ads</h4>
        <div className="text-center py-8">
          <span className="material-symbols-outlined text-[40px] text-outline-variant block mb-3">movie_edit</span>
          <p className="text-body-sm text-on-surface-variant">
            No ad performance yet. Run a campaign to see top performing ads here.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-surface-container-lowest border border-outline-variant rounded-xl overflow-hidden shadow-sm">
      <div className="p-stack-lg border-b border-outline-variant">
        <h4 className="text-label-md text-on-surface-variant uppercase tracking-wider">Top performing ads</h4>
      </div>
      <div className="divide-y divide-outline-variant">
        {ads.map((ad) => {
          const creative = ad.creative_data || {};
          const assets = ad.assets_data || {};
          const imageUrl = assets.gif_url || assets.image_url;
          const rate = ad.conversion_rate != null ? `${(ad.conversion_rate * 100).toFixed(1)}%` : '—';

          return (
            <div key={ad.ad_id} className="flex items-center gap-stack-md px-stack-lg py-stack-md hover:bg-surface-container-low transition-colors">
              <div className="w-16 h-16 rounded overflow-hidden shrink-0 bg-surface-container-high flex items-center justify-center">
                {imageUrl ? (
                  <img
                    src={`${BASE_URL}${imageUrl}`}
                    alt={creative.headline || 'ad'}
                    className="w-full h-full object-cover"
                    onError={(e) => { e.currentTarget.style.display = 'none'; }}
                  />
                ) : (
                  <span className="material-symbols-outlined text-on-surface-variant text-[24px]">image</span>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-label-md text-on-surface truncate">{creative.headline || 'Untitled ad'}</p>
                <p className="text-label-sm text-on-surface-variant mt-0.5">
                  {ad.customers_acquired} customer{ad.customers_acquired !== 1 ? 's' : ''} acquired
                </p>
              </div>
              <div className="text-right shrink-0">
                <p className="text-primary font-bold text-label-md">{rate} Conv.</p>
                <p className="text-label-sm text-on-surface-variant">{ad.shown} shown</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
