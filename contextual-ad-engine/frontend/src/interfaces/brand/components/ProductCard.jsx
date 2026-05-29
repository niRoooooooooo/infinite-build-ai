const BASE_URL = 'http://localhost:8000';

const categoryStyle = {
  beverage: 'bg-blue-50 text-blue-700',
  snack: 'bg-orange-50 text-orange-700',
  meal: 'bg-red-50 text-red-700',
  grocery: 'bg-green-50 text-green-700',
  electronics: 'bg-purple-50 text-purple-700',
  fashion: 'bg-pink-50 text-pink-700',
  service: 'bg-teal-50 text-teal-700',
};

export default function ProductCard({ product, onGenerateAd }) {
  const catClass = categoryStyle[product.category?.toLowerCase()] || 'bg-surface-container text-on-surface-variant';

  return (
    <div className="bg-surface-container-lowest border border-outline-variant rounded-xl overflow-hidden shadow-sm flex flex-col group hover:shadow-md transition-shadow">
      <div className="h-48 bg-surface-container-low relative">
        {product.image_url ? (
          <img
            src={`${BASE_URL}${product.image_url}`}
            alt={product.name}
            className="w-full h-full object-cover"
            onError={(e) => { e.currentTarget.style.display = 'none'; }}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <span className="material-symbols-outlined text-[48px] text-outline-variant">inventory_2</span>
          </div>
        )}
        {product.category && (
          <span className={`absolute top-2 right-2 px-stack-sm py-0.5 rounded text-[10px] font-bold uppercase ${catClass}`}>
            {product.category}
          </span>
        )}
      </div>
      <div className="p-stack-md flex-1 flex flex-col gap-1">
        <h3 className="text-body-lg font-bold text-on-surface leading-snug">{product.name}</h3>
        {product.description && (
          <p className="text-body-sm text-on-surface-variant line-clamp-2 flex-1">{product.description}</p>
        )}
        <button
          onClick={onGenerateAd}
          className="mt-auto w-full py-stack-sm bg-primary text-on-primary rounded-lg text-label-md font-semibold opacity-0 group-hover:opacity-100 transition-opacity hover:brightness-105"
        >
          Generate ad
        </button>
      </div>
    </div>
  );
}
