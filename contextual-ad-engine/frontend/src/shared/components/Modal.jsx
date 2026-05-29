import { useEffect } from 'react';

export default function Modal({ title, onClose, children, maxWidth = 'max-w-[500px]' }) {
  useEffect(() => {
    const handleKey = (e) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('keydown', handleKey);
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', handleKey);
      document.body.style.overflow = '';
    };
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-[100] flex items-center justify-center p-4"
      style={{ background: 'rgba(250,250,250,0.7)', backdropFilter: 'blur(8px)' }}
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div className={`bg-surface-container-lowest w-full ${maxWidth} rounded-xl border border-outline-variant shadow-2xl overflow-hidden`}>
        <div className="px-stack-lg py-stack-md border-b border-outline-variant flex justify-between items-center bg-surface-container-low">
          <h2 className="text-headline-sm font-semibold text-on-surface">{title}</h2>
          <button
            onClick={onClose}
            className="p-1 text-on-surface-variant hover:text-on-surface transition-colors rounded-lg hover:bg-surface-container-high"
          >
            <span className="material-symbols-outlined">close</span>
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}
