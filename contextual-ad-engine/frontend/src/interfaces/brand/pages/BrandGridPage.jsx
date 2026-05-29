import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useBrand } from '../../../context/BrandContext';
import BrandBlock from '../components/BrandBlock';
import AddBrandForm from '../components/AddBrandForm';
import Button from '../../../shared/components/Button';

function SkeletonCard() {
  return (
    <div className="bg-surface-container-lowest rounded-xl border border-outline-variant p-stack-lg animate-pulse">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-12 h-12 rounded-lg bg-surface-container-high flex-shrink-0" />
        <div className="flex-1">
          <div className="h-5 bg-surface-container-high rounded w-3/4 mb-2" />
          <div className="h-3 bg-surface-container-high rounded w-1/2" />
        </div>
      </div>
      <div className="h-3 bg-surface-container-high rounded w-1/3 mb-3" />
      <div className="h-16 bg-surface-container-high rounded-lg mb-6" />
      <div className="flex justify-between pt-4 border-t border-surface-variant">
        <div className="h-4 bg-surface-container-high rounded w-1/2" />
        <div className="h-4 bg-surface-container-high rounded w-1/4" />
      </div>
    </div>
  );
}

function AddBrandTile({ onClick }) {
  return (
    <div
      onClick={onClick}
      className="border-2 border-dashed border-outline-variant rounded-xl p-stack-lg flex flex-col items-center justify-center text-center opacity-60 hover:opacity-100 transition-opacity cursor-pointer min-h-[200px]"
    >
      <div className="w-12 h-12 rounded-full bg-surface-container-high flex items-center justify-center mb-4">
        <span className="material-symbols-outlined text-primary text-[32px]">add</span>
      </div>
      <p className="text-headline-sm text-on-surface font-semibold">New Brand</p>
      <p className="text-body-sm text-on-surface-variant mt-1">Click to expand your reach</p>
    </div>
  );
}

export default function BrandGridPage() {
  const { brands, loading } = useBrand();
  const navigate = useNavigate();
  const [showAddForm, setShowAddForm] = useState(false);

  return (
    <>
      {/* Page header */}
      <div className="flex justify-between items-end mb-stack-lg">
        <div>
          <h1 className="text-headline-lg text-on-surface">
            Brands {!loading && `(${brands.length})`}
          </h1>
          <p className="text-body-md text-on-surface-variant mt-1">
            Manage your brand workspaces and view performance
          </p>
        </div>
        <Button
          variant="primary"
          size="lg"
          icon="add"
          onClick={() => setShowAddForm(true)}
        >
          Add brand
        </Button>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-gutter">
        {loading ? (
          Array.from({ length: 5 }).map((_, i) => <SkeletonCard key={i} />)
        ) : brands.length === 0 ? (
          <div className="col-span-3 text-center py-16 text-on-surface-variant">
            <span className="material-symbols-outlined text-[48px] mb-4 block opacity-40">storefront</span>
            <p className="text-body-lg">No brands yet. Add your first brand to get started.</p>
          </div>
        ) : (
          brands.map((brand) => (
            <BrandBlock
              key={brand.brand_id}
              brand={brand}
              mode="summary"
              onClick={() => navigate(`/brand/${brand.brand_id}`)}
            />
          ))
        )}

        {!loading && (
          <AddBrandTile onClick={() => setShowAddForm(true)} />
        )}
      </div>

      {showAddForm && (
        <AddBrandForm onClose={() => setShowAddForm(false)} />
      )}
    </>
  );
}
