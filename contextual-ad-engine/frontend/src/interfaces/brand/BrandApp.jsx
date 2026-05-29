import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { BrandProvider } from '../../context/BrandContext';
import BrandGridPage from './pages/BrandGridPage';
import BrandDetailPage from './pages/BrandDetailPage';

const navItems = [
  { icon: 'grid_view', label: 'Brand Grid', to: '/brand' },
  { icon: 'monitoring', label: 'Performance', to: null },
  { icon: 'psychology', label: 'Recommendations', to: null },
  { icon: 'inventory_2', label: 'Catalog', to: null },
];

function Sidebar() {
  const location = useLocation();
  const isGrid = location.pathname === '/brand' || location.pathname === '/brand/';

  return (
    <aside className="fixed left-0 top-16 bottom-0 w-[240px] flex flex-col p-stack-md z-40 bg-surface-container-low border-r border-outline-variant">
      <div className="flex items-center gap-stack-sm px-2 py-4 mb-4">
        <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-white flex-shrink-0">
          <span className="material-symbols-outlined text-[18px]" style={{ fontVariationSettings: "'FILL' 1" }}>grid_view</span>
        </div>
        <div>
          <p className="text-label-md font-bold text-on-surface leading-tight">Brand Workspace</p>
          <p className="text-[10px] text-on-surface-variant leading-none uppercase tracking-wider">Marketing Admin</p>
        </div>
      </div>

      <nav className="flex-1 space-y-1">
        {navItems.map(({ icon, label, to }) => {
          const active = to && (to === '/brand' ? isGrid : location.pathname.startsWith(to));
          const base = 'flex items-center gap-3 px-3 py-2 rounded-lg transition-all duration-200 w-full text-left';
          const activeClass = 'bg-secondary-container text-on-secondary-container font-bold';
          const inactiveClass = 'text-on-surface-variant hover:bg-surface-container-high';

          if (to) {
            return (
              <Link key={label} to={to} className={`${base} ${active ? activeClass : inactiveClass}`}>
                <span className="material-symbols-outlined text-[20px]">{icon}</span>
                <span className="text-label-md">{label}</span>
              </Link>
            );
          }
          return (
            <button key={label} disabled className={`${base} ${inactiveClass} opacity-50 cursor-default`}>
              <span className="material-symbols-outlined text-[20px]">{icon}</span>
              <span className="text-label-md">{label}</span>
            </button>
          );
        })}
      </nav>

      <div className="mt-auto border-t border-outline-variant pt-4 space-y-1">
        <button disabled className="w-full flex items-center gap-3 px-3 py-2 text-on-surface-variant opacity-50 cursor-default rounded-lg">
          <span className="material-symbols-outlined text-[20px]">settings</span>
          <span className="text-label-md">Settings</span>
        </button>
        <button disabled className="w-full flex items-center gap-3 px-3 py-2 text-on-surface-variant opacity-50 cursor-default rounded-lg">
          <span className="material-symbols-outlined text-[20px]">help_outline</span>
          <span className="text-label-md">Support</span>
        </button>
      </div>
    </aside>
  );
}

function TopBar() {
  return (
    <header className="fixed top-0 w-full z-50 flex justify-between items-center px-margin-desktop h-16 bg-surface shadow-sm border-b border-outline-variant">
      <div className="flex items-center gap-stack-lg">
        <span className="text-headline-md font-bold text-primary">AdPersona AI</span>
      </div>
      <div className="hidden md:flex items-center space-x-8">
        <span className="text-primary border-b-2 border-primary pb-1 text-label-md font-medium">Brands</span>
      </div>
      <div className="flex items-center gap-stack-md">
        <Link
          to="/consumer"
          className="hidden lg:block text-label-md text-on-surface-variant hover:text-primary transition-colors duration-200"
        >
          Switch to Consumer View
        </Link>
        <button className="p-2 text-on-surface-variant hover:bg-surface-container-high rounded-full transition-colors duration-150">
          <span className="material-symbols-outlined">notifications</span>
        </button>
        <div className="h-8 w-8 rounded-full bg-primary-container flex items-center justify-center border border-outline-variant flex-shrink-0">
          <span className="material-symbols-outlined text-[18px] text-on-primary-container">person</span>
        </div>
      </div>
    </header>
  );
}

export default function BrandApp() {
  return (
    <BrandProvider>
      <TopBar />
      <Sidebar />
      <main className="ml-[240px] pt-16 min-h-screen bg-background">
        <div className="max-w-[1440px] mx-auto p-margin-desktop">
          <Routes>
            <Route index element={<BrandGridPage />} />
            <Route path=":brandId/*" element={<BrandDetailPage />} />
          </Routes>
        </div>
      </main>
    </BrandProvider>
  );
}
