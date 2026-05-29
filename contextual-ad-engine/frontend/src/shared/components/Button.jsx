const variants = {
  primary: 'bg-primary text-on-primary hover:opacity-90 shadow-sm',
  secondary: 'bg-white text-on-surface border border-outline-variant hover:bg-surface-container-high',
  ghost: 'text-primary hover:bg-primary/5',
  danger: 'bg-error text-on-error hover:opacity-90',
};

const sizes = {
  sm: 'px-3 py-1.5 text-label-sm rounded-lg',
  md: 'px-4 py-2.5 text-label-md rounded-xl',
  lg: 'px-6 py-3 text-label-md rounded-xl',
};

export default function Button({
  children,
  variant = 'primary',
  size = 'md',
  className = '',
  icon,
  loading = false,
  disabled = false,
  onClick,
  type = 'button',
  fullWidth = false,
}) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={[
        'inline-flex items-center justify-center gap-2 font-medium transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed',
        variants[variant],
        sizes[size],
        fullWidth ? 'w-full' : '',
        className,
      ].join(' ')}
    >
      {loading ? (
        <span className="material-symbols-outlined text-[18px] animate-spin">sync</span>
      ) : icon ? (
        <span className="material-symbols-outlined text-[18px]">{icon}</span>
      ) : null}
      {children}
    </button>
  );
}
