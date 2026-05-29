export default function ProgressIndicator({ steps = [], currentStep = 0, completedSteps = [] }) {
  return (
    <div className="space-y-stack-sm">
      {steps.map((step, i) => {
        const isDone = completedSteps.includes(i) || i < currentStep;
        const isActive = i === currentStep;
        const isPending = i > currentStep && !isDone;

        return (
          <div
            key={i}
            className={[
              'flex items-center gap-stack-md p-stack-md rounded-lg border transition-all',
              isDone
                ? 'bg-secondary-container/10 border-secondary-container/30'
                : isActive
                ? 'bg-surface-container border-primary ring-1 ring-primary/20'
                : 'opacity-50 grayscale border-outline-variant/30',
            ].join(' ')}
          >
            <div
              className={[
                'w-8 h-8 rounded-full flex items-center justify-center shrink-0',
                isDone
                  ? 'bg-primary text-on-primary'
                  : isActive
                  ? 'bg-primary-container text-on-primary-container'
                  : 'border-2 border-outline-variant',
              ].join(' ')}
            >
              {isDone ? (
                <span className="material-symbols-outlined text-[18px]">check</span>
              ) : isActive ? (
                <span className="material-symbols-outlined text-[18px] animate-spin">refresh</span>
              ) : null}
            </div>

            <div className="flex-1 min-w-0">
              <p className={`text-label-md ${isActive ? 'font-bold text-on-surface' : 'text-on-surface'}`}>
                {step}
              </p>
              {isActive && (
                <div className="w-full bg-surface-container-high h-1.5 rounded-full mt-1 overflow-hidden">
                  <div className="bg-primary h-full rounded-full w-2/3 relative">
                    <div className="absolute inset-0 bg-white/20 animate-pulse" />
                  </div>
                </div>
              )}
            </div>

            <span className={`text-label-sm shrink-0 ${isDone ? 'text-primary font-medium' : isActive ? 'text-primary font-bold' : 'text-on-surface-variant'}`}>
              {isDone ? 'Done' : isActive ? 'Running' : 'Pending'}
            </span>
          </div>
        );
      })}
    </div>
  );
}
