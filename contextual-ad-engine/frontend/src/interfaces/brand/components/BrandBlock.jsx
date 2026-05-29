import { useState, useEffect } from 'react';
import { getBrandProducts } from '../../../api/brands';

const BASE_URL = 'http://localhost:8000';

function LogoBox({ brand }) {
  const [imgError, setImgError] = useState(false);
  const initial = brand.display_name?.[0]?.toUpperCase() ?? '?';
  const bgColor = brand.visual_data?.primary_color ?? '#00685f';

  if (brand.logo_url && !imgError) {
    return (
      <div className="w-12 h-12 rounded-lg border border-outline-variant overflow-hidden flex-shrink-0 bg-white">
        <img
          src={`${BASE_URL}${brand.logo_url}`}
          alt={`${brand.display_name} logo`}
          className="w-full h-full object-cover"
          onError={() => setImgError(true)}
        />
      </div>
    );
  }

  return (
    <div
      className="w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0 text-white font-bold text-xl"
      style={{ backgroundColor: bgColor }}
    >
      {initial}
    </div>
  );
}

export default function BrandBlock({ brand, mode = 'summary', onClick }) {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    if (mode !== 'summary') return;
    getBrandProducts(brand.brand_id)
      .then(setProducts)
      .catch(() => {});
  }, [brand.brand_id, mode]);

  if (mode !== 'summary') {
    // Batch 2 will fill detail mode
    return null;
  }

  const topProduct = products[0];

  return (
    <div
      onClick={onClick}
      className="bg-surface-container-lowest rounded-xl border border-outline-variant p-stack-lg flex flex-col h-full cursor-pointer group"
      style={{
        boxShadow: '0px 1px 3px rgba(0,0,0,0.05), 0px 1px 2px rgba(0,0,0,0.03)',
        transition: 'transform 0.2s ease, box-shadow 0.2s ease',
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'translateY(-4px)';
        e.currentTarget.style.boxShadow = '0px 10px 15px -3px rgba(0,0,0,0.08)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = 'translateY(0)';
        e.currentTarget.style.boxShadow = '0px 1px 3px rgba(0,0,0,0.05), 0px 1px 2px rgba(0,0,0,0.03)';
      }}
    >
      {/* Header row: logo + name/tagline + conversion chip */}
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center gap-3">
          <LogoBox brand={brand} />
          <div>
            <h3 className="text-headline-sm text-on-surface font-semibold leading-tight">{brand.display_name}</h3>
            <p className="text-body-sm text-on-surface-variant mt-0.5">{brand.tagline}</p>
          </div>
        </div>
        <span className="bg-secondary-container text-on-secondary-container px-3 py-1 rounded-full text-[12px] font-bold whitespace-nowrap ml-2 flex-shrink-0">
          — top ad
        </span>
      </div>

      {/* Products row */}
      <div className="mb-6 flex-grow">
        <p className="text-[12px] font-bold uppercase tracking-wider text-on-surface-variant mb-2">
          Featured Products {products.length > 0 ? `(${products.length})` : ''}
        </p>
        {topProduct ? (
          <div className="flex items-center gap-3 p-3 bg-surface rounded-lg border border-outline-variant">
            <div className="w-10 h-10 rounded bg-white overflow-hidden flex-shrink-0 flex items-center justify-center border border-outline-variant">
              {topProduct.image_url ? (
                <img
                  src={`${BASE_URL}${topProduct.image_url}`}
                  alt={topProduct.name}
                  className="w-full h-full object-cover"
                  onError={(e) => { e.currentTarget.style.display = 'none'; }}
                />
              ) : (
                <span className="material-symbols-outlined text-on-surface-variant text-[20px]">inventory_2</span>
              )}
            </div>
            <div>
              <p className="text-label-md text-on-surface">{topProduct.name}</p>
              <p className="text-[12px] text-on-surface-variant">Top Performer</p>
            </div>
          </div>
        ) : (
          <div className="flex items-center gap-3 p-3 bg-surface rounded-lg border border-outline-variant">
            <div className="w-10 h-10 rounded bg-surface-container-high flex-shrink-0 flex items-center justify-center">
              <span className="material-symbols-outlined text-on-surface-variant text-[20px]">inventory_2</span>
            </div>
            <div>
              <p className="text-label-md text-on-surface-variant">No products yet</p>
            </div>
          </div>
        )}
      </div>

      {/* Footer: customers + manage link */}
      <div className="flex justify-between items-center mt-auto pt-4 border-t border-surface-variant">
        <div className="flex items-center gap-1 text-on-surface-variant">
          <span className="material-symbols-outlined text-[18px]">group</span>
          <span className="text-label-md font-bold">
            — <span className="font-normal opacity-70">customers this week</span>
          </span>
        </div>
        <span className="text-primary text-label-md hover:underline flex items-center gap-1 group-hover:underline">
          Manage <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
        </span>
      </div>
    </div>
  );
}
