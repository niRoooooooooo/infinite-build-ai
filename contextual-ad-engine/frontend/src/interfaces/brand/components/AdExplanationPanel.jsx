import { useState } from 'react';

export default function AdExplanationPanel({ ad }) {
  const [expanded, setExpanded] = useState(true);
  if (!ad) return null;

  const meta = ad.optimization_metadata || ad.optimization_data || {};
  const tags = ad.ad_tags || {};

  return (
    <div className="bg-secondary-container/20 border border-secondary-fixed-dim/50 rounded-xl overflow-hidden">
      <button
        onClick={() => setExpanded((v) => !v)}
        className="w-full flex items-center gap-2 px-stack-md py-stack-sm text-on-secondary-container hover:bg-secondary-container/20 transition-colors"
      >
        <span className="material-symbols-outlined text-[20px]" style={{ fontVariationSettings: "'FILL' 1" }}>
          auto_awesome
        </span>
        <span className="text-label-md font-bold flex-1 text-left">Why this ad?</span>
        <span className="material-symbols-outlined text-[18px]">
          {expanded ? 'expand_less' : 'expand_more'}
        </span>
      </button>

      {expanded && (
        <div className="px-stack-md pb-stack-md space-y-stack-sm">
          <div className="space-y-2">
            {meta.mode && (
              <div className="flex gap-2 text-body-sm text-on-surface-variant">
                <span className="text-primary font-bold">•</span>
                <span><span className="font-medium text-on-surface">Mode:</span> {meta.mode} — {meta.mode === 'exploit' ? '60% rule (top pattern)' : '40% rule (exploration)'}</span>
              </div>
            )}
            {tags.visual && (
              <div className="flex gap-2 text-body-sm text-on-surface-variant">
                <span className="text-primary font-bold">•</span>
                <span><span className="font-medium text-on-surface">Format:</span> {tags.visual}</span>
              </div>
            )}
            {tags.tone && (
              <div className="flex gap-2 text-body-sm text-on-surface-variant">
                <span className="text-primary font-bold">•</span>
                <span><span className="font-medium text-on-surface">Tone:</span> {tags.tone}</span>
              </div>
            )}
            {meta.rationale && (
              <div className="flex gap-2 text-body-sm text-on-surface-variant">
                <span className="text-primary font-bold">•</span>
                <span><span className="font-medium text-on-surface">Rationale:</span> {meta.rationale}</span>
              </div>
            )}
            {meta.user_profile_confidence != null && (
              <div className="flex gap-2 text-body-sm text-on-surface-variant">
                <span className="text-primary font-bold">•</span>
                <span><span className="font-medium text-on-surface">Confidence:</span> {meta.user_profile_confidence} ({meta.user_profile_source || 'aggregate'})</span>
              </div>
            )}
            {meta.sample_size != null && (
              <div className="flex gap-2 text-body-sm text-on-surface-variant">
                <span className="text-primary font-bold">•</span>
                <span><span className="font-medium text-on-surface">Sample size:</span> {meta.sample_size} prior interactions</span>
              </div>
            )}
            {!meta.mode && !tags.visual && !meta.rationale && (
              <p className="text-body-sm text-on-surface-variant italic">No optimization metadata available for this ad.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
