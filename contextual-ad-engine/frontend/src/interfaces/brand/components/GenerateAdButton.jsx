import { useState, useEffect } from 'react';
import { listPersonas } from '../../../api/personas';
import { generateAd } from '../../../api/ads';
import AdPreview from '../../../shared/components/AdPreview';
import AdExplanationPanel from './AdExplanationPanel';

export default function GenerateAdButton({ brand, products = [], preSelectedProduct = null }) {
  const [personas, setPersonas] = useState([]);
  const [selectedPersona, setSelectedPersona] = useState('');
  const [selectedProduct, setSelectedProduct] = useState(preSelectedProduct?.product_id || '');
  const [generating, setGenerating] = useState(false);
  const [generatedAd, setGeneratedAd] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    listPersonas().then(setPersonas).catch(() => {});
  }, []);

  useEffect(() => {
    if (preSelectedProduct) setSelectedProduct(preSelectedProduct.product_id);
  }, [preSelectedProduct]);

  async function handleGenerate() {
    if (!selectedPersona || !selectedProduct) return;
    setGenerating(true);
    setGeneratedAd(null);
    setError(null);
    try {
      const ad = await generateAd({
        brand_id: brand.brand_id,
        product_id: selectedProduct,
        persona_id: selectedPersona,
      });
      setGeneratedAd(ad);
    } catch (err) {
      setError(err.message ?? 'Generation failed. Try again.');
    } finally {
      setGenerating(false);
    }
  }

  const canGenerate = selectedPersona && selectedProduct && !generating;

  return (
    <div className="bg-surface-container-lowest border border-outline-variant rounded-xl overflow-hidden shadow-sm">
      {/* Header */}
      <div className="px-stack-lg py-stack-md border-b border-outline-variant bg-surface-container-low flex items-center gap-2">
        <span className="material-symbols-outlined text-primary">magic_button</span>
        <h3 className="text-headline-sm text-on-surface">Generate Ad Now</h3>
      </div>

      <div className="p-stack-lg space-y-stack-md">
        {/* Persona selector */}
        <div className="space-y-stack-xs">
          <label className="text-label-sm text-on-surface-variant">Select Persona</label>
          <div className="relative">
            <select
              value={selectedPersona}
              onChange={(e) => setSelectedPersona(e.target.value)}
              className="w-full h-11 px-stack-md rounded-xl border border-outline-variant bg-surface focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none text-on-surface text-body-sm transition-all appearance-none cursor-pointer"
            >
              <option value="">Choose a persona...</option>
              {personas.map((p) => (
                <option key={p.persona_id} value={p.persona_id}>
                  {p.display_name} — {p.age}, {p.city}
                </option>
              ))}
            </select>
            <span className="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-on-surface-variant text-[18px]">expand_more</span>
          </div>
        </div>

        {/* Product selector */}
        <div className="space-y-stack-xs">
          <label className="text-label-sm text-on-surface-variant">Select Product</label>
          <div className="relative">
            <select
              value={selectedProduct}
              onChange={(e) => setSelectedProduct(e.target.value)}
              className="w-full h-11 px-stack-md rounded-xl border border-outline-variant bg-surface focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none text-on-surface text-body-sm transition-all appearance-none cursor-pointer"
            >
              <option value="">Choose a product...</option>
              {products.map((p) => (
                <option key={p.product_id} value={p.product_id}>{p.name}</option>
              ))}
            </select>
            <span className="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-on-surface-variant text-[18px]">expand_more</span>
          </div>
        </div>

        {/* Generate button */}
        <button
          onClick={handleGenerate}
          disabled={!canGenerate}
          className="w-full bg-primary text-on-primary py-stack-md rounded-xl font-bold flex items-center justify-center gap-2 shadow-sm hover:opacity-90 active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {generating ? (
            <><span className="material-symbols-outlined animate-spin">sync</span> Generating...</>
          ) : (
            <><span className="material-symbols-outlined">auto_awesome</span> Generate ad</>
          )}
        </button>

        {error && (
          <p className="text-error text-body-sm text-center">{error}</p>
        )}

        {/* Result */}
        {generatedAd ? (
          <div className="space-y-stack-md pt-stack-sm border-t border-outline-variant/50">
            <p className="text-label-sm text-on-surface-variant uppercase tracking-wider">Ad Preview</p>
            <AdPreview ad={generatedAd} />
            <AdExplanationPanel ad={generatedAd} />
            <div className="grid grid-cols-2 gap-stack-sm">
              <button
                onClick={() => setGeneratedAd(null)}
                className="flex flex-col items-center justify-center gap-1 p-stack-md border border-outline-variant rounded-xl hover:bg-surface-container-high transition-all group text-on-surface-variant text-label-sm"
              >
                <span className="material-symbols-outlined group-hover:text-primary">refresh</span>
                Generate another
              </button>
              <button
                className="flex flex-col items-center justify-center gap-1 p-stack-md border border-outline-variant rounded-xl hover:bg-surface-container-high transition-all group text-on-surface-variant text-label-sm"
              >
                <span className="material-symbols-outlined group-hover:text-primary">bookmark_add</span>
                Save to library
              </button>
            </div>
          </div>
        ) : !generating && (
          <div className="border-t border-outline-variant/50 pt-stack-lg text-center py-stack-lg">
            <span className="material-symbols-outlined text-[48px] text-outline-variant mb-stack-sm block">movie_edit</span>
            <p className="text-body-sm text-on-surface-variant">Generated ads will appear here</p>
          </div>
        )}
      </div>
    </div>
  );
}
