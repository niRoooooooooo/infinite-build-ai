const iconMap = {
  default: 'bolt',
  date: 'event',
  warning: 'trending_down',
};

export default function RecommendationsPanel({ recommendations = [] }) {
  return (
    <div className="bg-primary/5 border border-primary/20 rounded-xl p-stack-lg">
      <div className="flex items-center gap-stack-sm mb-stack-lg">
        <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-on-primary shrink-0">
          <span
            className="material-symbols-outlined text-[20px]"
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            lightbulb
          </span>
        </div>
        <h3 className="text-headline-sm text-primary">AI Recommendations</h3>
      </div>

      {recommendations.length === 0 ? (
        <div className="text-center py-6">
          <span className="material-symbols-outlined text-[40px] text-outline-variant block mb-3">lightbulb</span>
          <p className="text-body-sm text-on-surface-variant">
            Run the optimization cycle to generate AI recommendations for this brand.
          </p>
        </div>
      ) : (
        <div className="space-y-stack-md">
          {recommendations.map((rec, i) => (
            <div
              key={i}
              className="bg-surface-container-lowest p-stack-md rounded-lg border border-outline-variant shadow-sm flex gap-stack-md hover:border-primary transition-colors cursor-pointer"
            >
              <span className={`material-symbols-outlined shrink-0 ${rec.type === 'warning' ? 'text-error' : 'text-primary'}`}>
                {iconMap[rec.type] || iconMap.default}
              </span>
              <p className="text-body-sm text-on-surface">{rec.text}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
