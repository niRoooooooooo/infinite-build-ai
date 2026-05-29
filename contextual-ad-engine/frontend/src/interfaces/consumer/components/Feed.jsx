import { useState, useEffect } from 'react';
import { usePersona } from '../../../context/PersonaContext';
import { getFeed } from '../../../api/feed';
import OrganicCard from './OrganicCard';
import SponsoredAdCard from './SponsoredAdCard';

const SECTION_HEADERS = {
  0: 'Popular near you',
  4: 'Recommended for you',
  8: 'Trending in Dhaka',
  12: 'New arrivals',
};

function SkeletonCard() {
  return (
    <div className="bg-white rounded-xl shadow-sm overflow-hidden animate-pulse">
      <div className="w-full aspect-video bg-gray-200" />
      <div className="p-4 space-y-2">
        <div className="h-3 bg-gray-200 rounded w-1/4" />
        <div className="h-5 bg-gray-200 rounded w-3/4" />
        <div className="h-3 bg-gray-200 rounded w-full" />
        <div className="h-3 bg-gray-200 rounded w-2/3" />
      </div>
    </div>
  );
}

export default function Feed() {
  const { currentPersona } = usePersona();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!currentPersona) return;
    setLoading(true);
    setError(null);
    getFeed(currentPersona.persona_id)
      .then((data) => setItems(data.feed || []))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [currentPersona]);

  if (loading) {
    return (
      <div className="space-y-4">
        {Array.from({ length: 4 }).map((_, i) => <SkeletonCard key={i} />)}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12 text-gray-400">
        <span className="material-symbols-outlined text-[40px] block mb-2">wifi_off</span>
        <p className="text-[14px]">Could not load feed. Check the backend is running.</p>
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="text-center py-12 text-gray-400">
        <span className="material-symbols-outlined text-[40px] block mb-2">inbox</span>
        <p className="text-[14px]">No feed items yet.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {items.map((item, idx) => (
        <div key={item.id || item.ad_id || idx}>
          {SECTION_HEADERS[idx] && (
            <h3 className="text-[13px] font-bold uppercase tracking-wider text-gray-400 pt-2 pb-1 px-1">
              {SECTION_HEADERS[idx]}
            </h3>
          )}
          {item.type === 'sponsored'
            ? <SponsoredAdCard ad={item} />
            : <OrganicCard item={item} />
          }
        </div>
      ))}
    </div>
  );
}
