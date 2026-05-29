const BASE_URL = 'http://localhost:8000';

const TYPE_META = {
  news:   { label: 'NEWS',   color: 'text-blue-600',  border: 'border-blue-500' },
  recipe: { label: 'RECIPE', color: 'text-orange-600', border: 'border-orange-400' },
  social: { label: 'SOCIAL', color: 'text-purple-600', border: 'border-purple-400' },
  event:  { label: 'EVENT',  color: 'text-green-600',  border: 'border-green-500' },
};

function timeAgo() {
  const mins = [15, 30, 45, 60, 90, 120, 180];
  const m = mins[Math.floor(Math.random() * mins.length)];
  return m < 60 ? `${m}m ago` : `${Math.floor(m / 60)}h ago`;
}

export default function OrganicCard({ item }) {
  const meta = TYPE_META[item.type] || TYPE_META.news;
  const hasImage = item.image && !item.image.includes('/static/');

  // For event/social types without image: render a text-forward card
  if (!hasImage && (item.type === 'social' || item.type === 'event')) {
    return (
      <article className={`bg-white rounded-xl shadow-sm overflow-hidden border-l-4 ${meta.border} p-4 group hover:-translate-y-0.5 transition-transform duration-200`}>
        <div className="flex items-center gap-2 mb-2">
          <span className={`text-[11px] font-bold uppercase tracking-wider ${meta.color}`}>
            {meta.label} • {timeAgo()}
          </span>
        </div>
        <h2 className="text-[16px] font-bold text-gray-900 leading-snug mb-1">{item.title}</h2>
        {item.body && (
          <p className="text-[13px] text-gray-500 line-clamp-2">{item.body}</p>
        )}
        <div className="flex items-center gap-4 mt-3">
          <div className="flex items-center gap-1 text-gray-400 text-[12px]">
            <span className="material-symbols-outlined text-[14px]">thumb_up</span>
            {Math.floor(Math.random() * 200 + 20)}
          </div>
          <div className="flex items-center gap-1 text-gray-400 text-[12px]">
            <span className="material-symbols-outlined text-[14px]">chat_bubble_outline</span>
            {Math.floor(Math.random() * 50 + 5)}
          </div>
        </div>
      </article>
    );
  }

  return (
    <article className="bg-white rounded-xl shadow-sm overflow-hidden group hover:-translate-y-0.5 transition-transform duration-200">
      {/* Image */}
      <div className="w-full aspect-video overflow-hidden bg-gray-100">
        {hasImage ? (
          <img
            src={`${BASE_URL}${item.image}`}
            alt={item.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            onError={(e) => { e.currentTarget.parentElement.style.display = 'none'; }}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-200">
            <span className="material-symbols-outlined text-[48px] text-gray-300">image</span>
          </div>
        )}
      </div>
      {/* Body */}
      <div className="p-4 space-y-2">
        <div className="flex items-center gap-2">
          <span className={`text-[11px] font-bold uppercase tracking-wider ${meta.color}`}>
            {meta.label} • {timeAgo()}
          </span>
        </div>
        <h2 className="text-[16px] font-bold text-gray-900 leading-snug">{item.title}</h2>
        {item.body && (
          <p className="text-[13px] text-gray-500 line-clamp-2">{item.body}</p>
        )}
        <div className="flex items-center gap-4 pt-1">
          <div className="flex items-center gap-1 text-gray-400 text-[12px]">
            <span className="material-symbols-outlined text-[14px]">thumb_up</span>
            {Math.floor(Math.random() * 300 + 30)}
          </div>
          <div className="flex items-center gap-1 text-gray-400 text-[12px]">
            <span className="material-symbols-outlined text-[14px]">chat_bubble_outline</span>
            {Math.floor(Math.random() * 60 + 5)}
          </div>
          <div className="flex items-center gap-1 text-gray-400 text-[12px]">
            <span className="material-symbols-outlined text-[14px]">share</span>
            Share
          </div>
        </div>
      </div>
    </article>
  );
}
