import AttributionMetrics from './AttributionMetrics';
import TopAdsList from './TopAdsList';
import RecommendationsPanel from './RecommendationsPanel';

export default function PerformanceSection({ performance, topAds = [], recommendations = [] }) {
  return (
    <section className="space-y-stack-lg">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-headline-sm text-on-surface">Performance</h2>
          <p className="text-on-surface-variant text-label-md mt-0.5">This week</p>
        </div>
      </div>

      <AttributionMetrics metrics={performance} />
      <TopAdsList ads={topAds} />
      <RecommendationsPanel recommendations={recommendations} />
    </section>
  );
}
