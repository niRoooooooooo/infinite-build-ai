function StatCard({ icon, value, label, highlight }) {
  return (
    <div className={`rounded-xl p-stack-lg flex flex-col justify-between border shadow-sm ${highlight ? 'bg-secondary-container/30 border-secondary/20' : 'bg-surface-container-lowest border-outline-variant'}`}>
      <span className={`material-symbols-outlined mb-stack-md ${highlight ? 'text-secondary' : 'text-primary'}`}>{icon}</span>
      <div>
        <p className={`leading-none ${highlight ? 'text-headline-sm text-secondary' : 'text-display-stat text-on-surface'}`}>{value}</p>
        <p className={`text-label-md mt-stack-xs ${highlight ? 'text-secondary' : 'text-on-surface-variant'}`}>{label}</p>
      </div>
    </div>
  );
}

export default function AttributionMetrics({ metrics }) {
  if (!metrics) return null;

  const acquired = metrics.customers_acquired ?? 0;
  const shown = metrics.total_ads_shown ?? 0;
  const rate = metrics.overall_conversion_rate ?? 0;
  const bestSeg = metrics.best_segment || 'N/A';
  const breakdown = metrics.segment_breakdown || [];

  return (
    <div className="space-y-stack-lg">
      {/* Headline metric */}
      <div className="bg-surface-container-lowest border border-outline-variant rounded-xl p-stack-lg shadow-sm flex flex-col justify-center min-h-[160px]">
        <div className="flex items-baseline gap-stack-md">
          <span className="text-display-lg text-primary font-bold">{acquired}</span>
          {acquired > 0 && (
            <span className="text-green-600 font-bold flex items-center text-label-md">
              <span className="material-symbols-outlined text-[16px]">trending_up</span> active
            </span>
          )}
        </div>
        <p className="text-headline-sm text-on-surface mt-stack-sm">customers acquired this week</p>
        {acquired > 0 && (
          <div className="mt-stack-md w-full bg-surface-container-low h-2 rounded-full overflow-hidden">
            <div className="bg-primary h-full rounded-full" style={{ width: `${Math.min(rate * 10, 100)}%`, transition: 'width 1s ease' }} />
          </div>
        )}
      </div>

      {/* Three stat cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-stack-md">
        <StatCard icon="ad_units" value={shown.toLocaleString()} label="ads shown" />
        <StatCard icon="data_exploration" value={`${rate}%`} label="conversion rate" />
        <StatCard icon="stars" value={bestSeg} label="best segment" highlight />
      </div>

      {/* Segment breakdown */}
      {breakdown.length > 0 && (
        <div className="bg-surface-container-lowest border border-outline-variant rounded-xl overflow-hidden shadow-sm">
          <div className="p-stack-lg border-b border-outline-variant">
            <h3 className="text-headline-sm text-on-surface">Where customers came from</h3>
          </div>
          <div className="p-stack-lg space-y-stack-md">
            {breakdown.map((seg, i) => (
              <div key={seg.segment} className="space-y-stack-xs">
                <div className="flex justify-between text-label-md">
                  <span className="text-on-surface capitalize">{seg.segment}</span>
                  <span className="font-bold">{seg.percent}%</span>
                </div>
                <div className="w-full bg-surface-container h-3 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full"
                    style={{
                      width: `${seg.percent}%`,
                      backgroundColor: i === 0 ? '#00685f' : i === 1 ? 'rgba(0,104,95,0.6)' : 'rgba(0,104,95,0.3)',
                      transition: 'width 1s cubic-bezier(0.4,0,0.2,1)',
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {acquired === 0 && breakdown.length === 0 && (
        <p className="text-body-sm text-on-surface-variant text-center py-4 italic">
          No conversion data yet. Ads will populate this section as users interact with them in Interface A.
        </p>
      )}
    </div>
  );
}
