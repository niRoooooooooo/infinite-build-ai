import { useState } from 'react';
import { logConversion } from '../../../api/events';
import { usePersona } from '../../../context/PersonaContext';

const PINK = '#D70F64';

export default function ConversionButtons({ ad }) {
  const { currentPersona } = usePersona();
  const [decision, setDecision] = useState(null); // null | 'taken' | 'skipped'
  const [logging, setLogging] = useState(false);

  async function handleConvert(converted) {
    if (logging || decision) return;
    setLogging(true);
    try {
      await logConversion({
        ad_id: ad.ad_id,
        persona_id: currentPersona?.persona_id,
        converted,
        source: 'live_interaction',
      });
    } catch (err) {
      console.error('logConversion failed:', err);
    } finally {
      setLogging(false);
      setDecision(converted ? 'taken' : 'skipped');
    }
  }

  if (decision === 'taken') {
    return (
      <div className="flex items-center gap-2 py-3 px-4 rounded-full bg-green-50 border border-green-200">
        <span className="material-symbols-outlined text-green-600 text-[18px]" style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>
        <span className="text-[14px] font-semibold text-green-700">Offer claimed!</span>
      </div>
    );
  }

  if (decision === 'skipped') {
    return (
      <p className="text-[13px] text-gray-400 text-center py-2">Skipped</p>
    );
  }

  return (
    <div className="flex gap-3">
      <button
        onClick={() => handleConvert(true)}
        disabled={logging}
        className="flex-1 h-12 rounded-full text-white font-semibold text-[14px] hover:opacity-90 active:scale-95 transition-all disabled:opacity-60"
        style={{ backgroundColor: PINK }}
      >
        Take the offer
      </button>
      <button
        onClick={() => handleConvert(false)}
        disabled={logging}
        className="flex-1 h-12 rounded-full bg-gray-100 text-gray-700 font-semibold text-[14px] hover:bg-gray-200 active:scale-95 transition-all disabled:opacity-60"
      >
        Skip
      </button>
    </div>
  );
}
