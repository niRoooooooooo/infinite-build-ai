import { useState } from 'react';
import ProductCard from './ProductCard';
import ProductUploadForm from './ProductUploadForm';

function AddProductTile({ onClick }) {
  return (
    <button
      onClick={onClick}
      className="border-2 border-dashed border-outline-variant rounded-xl flex flex-col items-center justify-center gap-stack-sm text-on-surface-variant hover:bg-surface-container hover:border-primary transition-all group min-h-[250px]"
    >
      <div className="w-12 h-12 rounded-full bg-surface-container-high flex items-center justify-center group-hover:bg-primary/10 group-hover:text-primary transition-colors">
        <span className="material-symbols-outlined text-[32px]">add</span>
      </div>
      <span className="text-label-md">Add new product</span>
    </button>
  );
}

export default function ProductsSection({ brand, products = [], onProductAdded }) {
  const [showUpload, setShowUpload] = useState(false);
  const [pendingGenerateProduct, setPendingGenerateProduct] = useState(null);

  function handleGenerateAd(product) {
    setPendingGenerateProduct(product);
    // Signal to parent (BrandDetailPage) to pre-select this product in GenerateAdButton
    if (onProductAdded?.onGenerateAd) {
      onProductAdded.onGenerateAd(product);
    }
  }

  return (
    <section className="space-y-stack-md">
      <div className="flex justify-between items-end">
        <h2 className="text-headline-sm text-on-surface">Products ({products.length})</h2>
        <button
          onClick={() => setShowUpload(true)}
          className="flex items-center gap-1 px-stack-md py-stack-sm bg-primary text-on-primary rounded-lg text-label-md font-semibold hover:opacity-90 transition-opacity active:scale-95"
        >
          <span className="material-symbols-outlined text-[18px]">add</span>
          Add product
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-gutter">
        {products.map((p) => (
          <ProductCard
            key={p.product_id}
            product={p}
            onGenerateAd={() => handleGenerateAd(p)}
          />
        ))}
        <AddProductTile onClick={() => setShowUpload(true)} />
      </div>

      {showUpload && (
        <ProductUploadForm
          brandId={brand.brand_id}
          onSuccess={(newProduct) => {
            if (onProductAdded) onProductAdded(newProduct);
          }}
          onClose={() => setShowUpload(false)}
        />
      )}
    </section>
  );
}
