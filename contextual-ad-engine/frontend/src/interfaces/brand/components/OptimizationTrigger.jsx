import { useState, useEffect, useRef } from 'react';
import ProgressIndicator from '../../../shared/components/ProgressIndicator';
import { runCycle } from '../../../api/optimization';

const STEPS = [
  'Extracting user patterns...',
  'Aggregating insights...',
  'Reshaping libraries...',
  'Generating recommendations...',
];

export default function OptimizationTrigger({ brandId, onCycleComplete }) {
  const [running, setRunning] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState([]);
  const [results, setResults] = useState(null);
  const timerRef = useRef(null);

  function clearTimers() {
    if (timerRef.current) clearTimeout(timerRef.current);
  }

  useEffect(() => () => clearTimers(), []);

  async function handleRun() {
    setRunning(true);
    setResults(null);
    setCompletedSteps([]);
    setCurrentStep(0);

    // Animate steps at ~800ms each while API call runs in parallel
    let step = 0;
    function advance() {
      if (step < STEPS.length - 1) {
        setCompletedSteps((prev) => [...prev, step]);
        step += 1;
        setCurrentStep(step);
        timerRef.current = setTimeout(advance, 900);
      }
    }
    timerRef.current = setTimeout(advance, 900);

    try {
      const data = await runCycle(brandId);
      clearTimers();
      setCompletedSteps([0, 1, 2, 3]);
      setCurrentStep(STEPS.length);
      setResults(data);
      if (onCycleComplete) onCycleComplete(data);
    } catch (err) {
      clearTimers();
      console.error('Optimization cycle failed:', err);
    } finally {
      setRunning(false);
    }
  }

  return (
    <section className="bg-surface-container-lowest border border-outline-variant rounded-xl p-stack-lg shadow-sm space-y-stack-lg">
      <div className="flex items-center gap-stack-sm">
        <span className="material-symbols-outlined text-primary">auto_awesome</span>
        <h2 className="text-headline-sm text-on-surface">AI Optimization</h2>
      </div>

      {!running && !results && (
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <p className="text-body-md text-on-surface-variant max-w-lg">
            Run a full optimization cycle to re-analyze user patterns, aggregate insights, and generate fresh AI recommendations for this brand.
          </p>
          <button
            onClick={handleRun}
            className="flex items-center gap-2 px-6 py-3 bg-primary text-on-primary rounded-xl text-label-md font-bold shadow-sm hover:opacity-90 active:scale-95 transition-all shrink-0"
          >
            <span className="material-symbols-outlined">auto_awesome</span>
            Run optimization cycle
          </button>
        </div>
      )}

      {running && (
        <div className="space-y-stack-md">
          <ProgressIndicator steps={STEPS} currentStep={currentStep} completedSteps={completedSteps} />
          <button
            disabled
            className="w-full py-stack-md bg-surface-container-high text-on-surface-variant text-label-md rounded-xl flex items-center justify-center gap-2 border border-outline-variant cursor-not-allowed"
          >
            <span className="material-symbols-outlined animate-spin">sync</span>
            Running optimization cycle...
          </button>
        </div>
      )}

      {results && !running && (
        <div className="space-y-stack-md">
          <ProgressIndicator steps={STEPS} currentStep={STEPS.length} completedSteps={[0, 1, 2, 3]} />

          <div className="bg-secondary-container/20 border border-secondary-fixed-dim/30 rounded-xl p-stack-lg space-y-stack-sm">
            <div className="flex items-center gap-2 mb-stack-sm">
              <span className="material-symbols-outlined text-primary" style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>
              <p className="text-label-md font-bold text-on-surface">Cycle complete</p>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-surface-container-lowest rounded-lg p-3 border border-outline-variant">
                <p className="text-display-stat text-on-surface leading-none">{results.events_processed ?? 0}</p>
                <p className="text-label-sm text-on-surface-variant mt-1">events processed</p>
              </div>
              <div className="bg-surface-container-lowest rounded-lg p-3 border border-outline-variant">
                <p className="text-display-stat text-on-surface leading-none">{results.users_updated ?? 0}</p>
                <p className="text-label-sm text-on-surface-variant mt-1">profiles updated</p>
              </div>
            </div>
          </div>

          <button
            onClick={handleRun}
            className="flex items-center gap-2 px-stack-md py-stack-sm border border-outline-variant text-on-surface-variant rounded-lg text-label-md hover:bg-surface-container-high transition-colors"
          >
            <span className="material-symbols-outlined text-[18px]">refresh</span>
            Run again
          </button>
        </div>
      )}
    </section>
  );
}
