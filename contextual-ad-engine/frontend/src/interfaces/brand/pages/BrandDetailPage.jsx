import { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getBrand, getBrandProducts, getBrandPerformance, getBrandTopAds } from '../../../api/brands';
import BrandIdentitySection from '../components/BrandIdentitySection';
import ProductsSection from '../components/ProductsSection';
import PerformanceSection from '../components/PerformanceSection';
import OptimizationTrigger from '../components/OptimizationTrigger';
import GenerateAdButton from '../components/GenerateAdButton';

function SkeletonBlock({ h = 'h-48' }) {
  return <div className={`${h} bg-surface-container-high rounded-xl animate-pulse`} />;
}

export default function BrandDetailPage() {
  const { brandId } = useParams();
  const [brand, setBrand] = useState(null);
  const [products, setProducts] = useState([]);
  const [performance, setPerformance] = useState(null);
  const [topAds, setTopAds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);
  const [preSelectedProduct, setPreSelectedProduct] = useState(null);

  const loadAll = useCallback(async () => {
    setLoading(true);
    setNotFound(false);
    try {
      const [b, prods, perf, ads] = await Promise.all([
        getBrand(brandId),
        getBrandProducts(brandId),
        getBrandPerformance(brandId),
        getBrandTopAds(brandId),
      ]);
      setBrand(b);
      setProducts(prods);
      setPerformance(perf);
      setTopAds(ads);
    } catch (err) {
      if (err.message?.includes('404')) setNotFound(true);
      else console.error(err);
    } finally {
      setLoading(false);
    }
  }, [brandId]);

  useEffect(() => { loadAll(); }, [loadAll]);

  function handleProductAdded(newProduct) {
    setProducts((prev) => [...prev, newProduct]);
  }

  if (loading) {
    return (
      <div className="space-y-stack-lg">
        <div className="flex items-center gap-2 mb-stack-lg">
          <div className="h-4 w-16 bg-surface-container-high rounded animate-pulse" />
          <div className="h-4 w-4 bg-surface-container-high rounded animate-pulse" />
          <div className="h-4 w-24 bg-surface-container-high rounded animate-pulse" />
        </div>
        <div className="flex flex-col lg:flex-row gap-gutter">
          <div className="flex-1 space-y-stack-lg">
            <SkeletonBlock h="h-56" />
            <SkeletonBlock h="h-80" />
            <SkeletonBlock h="h-64" />
          </div>
          <div className="w-full lg:w-[320px] shrink-0">
            <SkeletonBlock h="h-96" />
          </div>
        </div>
      </div>
    );
  }

  if (notFound) {
    return (
      <div className="text-center py-24">
        <span className="material-symbols-outlined text-[56px] text-outline-variant block mb-4">storefront</span>
        <h2 className="text-headline-md text-on-surface mb-2">Brand not found</h2>
        <p className="text-body-md text-on-surface-variant mb-6">The brand "{brandId}" doesn't exist.</p>
        <Link to="/brand" className="text-primary text-label-md hover:underline flex items-center gap-1 justify-center">
          <span className="material-symbols-outlined text-[18px]">arrow_back</span>
          Back to all brands
        </Link>
      </div>
    );
  }

  if (!brand) return null;

  return (
    <>
      {/* Breadcrumb */}
      <nav className="flex items-center gap-stack-sm mb-stack-lg text-on-surface-variant text-label-md">
        <Link to="/brand" className="hover:text-primary transition-colors">Brands</Link>
        <span className="material-symbols-outlined text-[16px]">chevron_right</span>
        <span className="text-on-surface font-semibold">{brand.display_name}</span>
      </nav>

      <div className="flex flex-col lg:flex-row gap-gutter">
        {/* Main content column */}
        <div className="flex-1 space-y-stack-lg min-w-0">
          <BrandIdentitySection brand={brand} />

          <ProductsSection
            brand={brand}
            products={products}
            onProductAdded={(newProduct) => {
              handleProductAdded(newProduct);
            }}
          />

          <PerformanceSection
            performance={performance}
            topAds={topAds}
            recommendations={[]}
          />

          <OptimizationTrigger
            brandId={brandId}
            onCycleComplete={() => {
              getBrandPerformance(brandId).then(setPerformance).catch(() => {});
              getBrandTopAds(brandId).then(setTopAds).catch(() => {});
            }}
          />
        </div>

        {/* Sticky right sidebar */}
        <div className="w-full lg:w-[320px] shrink-0">
          <div className="sticky top-24">
            <GenerateAdButton
              brand={brand}
              products={products}
              preSelectedProduct={preSelectedProduct}
            />

            {/* Tip card */}
            <div className="mt-stack-md bg-primary/5 rounded-xl p-stack-md border border-primary/10">
              <div className="flex gap-stack-sm">
                <span className="material-symbols-outlined text-primary text-[20px]">lightbulb</span>
                <p className="text-label-sm text-on-surface-variant">
                  Select a persona + product, then click Generate to see a contextually personalized ad created in real time.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
