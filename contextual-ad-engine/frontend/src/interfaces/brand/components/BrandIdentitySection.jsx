const BASE_URL = 'http://localhost:8000';

function Swatch({ color, label }) {
  return (
    <div className="flex items-center gap-2">
      <div
        className="w-7 h-7 rounded-full border-2 border-white shadow"
        style={{ backgroundColor: color }}
        title={label}
      />
      <span className="text-[11px] text-on-surface-variant font-mono">{color}</span>
    </div>
  );
}

export default function BrandIdentitySection({ brand }) {
  const visual = brand.visual_data || {};
  const voice = brand.voice_data || {};
  const toneStr = voice.tone || '';
  const tones = toneStr.split(/[_,\s]+/).filter(Boolean);

  return (
    <section className="relative overflow-hidden bg-surface-container-lowest border border-outline-variant rounded-xl p-stack-lg shadow-sm">
      <div
        className="absolute top-0 right-0 w-64 h-64 rounded-full -mr-20 -mt-20 blur-3xl opacity-60"
        style={{ backgroundColor: (visual.primary_color || '#00685f') + '22' }}
      />
      <div className="flex flex-col md:flex-row gap-stack-lg items-start relative z-10">
        {/* Logo */}
        <div
          className="w-32 h-32 rounded-xl flex items-center justify-center border border-outline-variant shrink-0 text-white font-bold text-headline-lg overflow-hidden"
          style={{ backgroundColor: visual.primary_color || '#00685f' }}
        >
          {brand.logo_url ? (
            <img
              src={`${BASE_URL}${brand.logo_url}`}
              alt={brand.display_name}
              className="w-full h-full object-cover"
              onError={(e) => { e.currentTarget.style.display = 'none'; }}
            />
          ) : (
            brand.display_name?.[0]?.toUpperCase()
          )}
        </div>

        {/* Info */}
        <div className="flex-1 space-y-stack-md">
          <div className="flex justify-between items-start gap-4">
            <div>
              <h1 className="text-headline-lg text-on-surface">{brand.display_name}</h1>
              {brand.tagline && (
                <p className="text-label-md text-primary italic mt-1">"{brand.tagline}"</p>
              )}
            </div>
            <button className="flex items-center gap-1 px-stack-md py-stack-sm border border-outline text-on-surface rounded-lg text-label-md hover:bg-surface-variant transition-colors shrink-0">
              <span className="material-symbols-outlined text-[18px]">edit</span>
              Edit identity
            </button>
          </div>

          {brand.description && (
            <p className="text-body-md text-on-surface-variant max-w-2xl">{brand.description}</p>
          )}

          {tones.length > 0 && (
            <div className="flex flex-wrap gap-stack-sm">
              {tones.map((t) => (
                <span key={t} className="px-stack-md py-stack-xs bg-secondary-container/30 text-on-secondary-container rounded-full text-label-sm">
                  {t}
                </span>
              ))}
            </div>
          )}

          <div className="pt-stack-sm">
            <p className="text-label-sm text-on-surface-variant mb-stack-sm">Brand Palette</p>
            <div className="flex gap-stack-md flex-wrap">
              {visual.primary_color && <Swatch color={visual.primary_color} label="Primary" />}
              {visual.accent_color && <Swatch color={visual.accent_color} label="Accent" />}
              {visual.secondary_color && <Swatch color={visual.secondary_color} label="Secondary" />}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
