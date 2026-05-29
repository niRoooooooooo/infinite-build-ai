import { Link } from 'react-router-dom';
import { usePersona } from '../../../context/PersonaContext';
import PersonaSwitcher from '../components/PersonaSwitcher';
import Feed from '../components/Feed';

const PINK = '#D70F64';
const PINK_DARK = '#A80050';

const CATEGORIES = [
  { icon: 'restaurant', label: 'Restaurants' },
  { icon: 'local_grocery_store', label: 'Groceries' },
  { icon: 'storefront', label: 'Shops' },
  { icon: 'medication', label: 'Pharma' },
  { icon: 'devices', label: 'Electronics' },
];

function TopNav() {
  return (
    <header
      className="sticky top-0 z-50 w-full shadow-md"
      style={{ backgroundColor: PINK }}
    >
      <div className="max-w-[1200px] mx-auto px-12 h-20 flex items-center gap-6">
        {/* Logo */}
        <span className="text-[22px] font-black text-white tracking-tight shrink-0">
          foodpanda
        </span>

        {/* Location pill */}
        <div
          className="hidden lg:flex items-center gap-1 px-4 py-2 rounded-full cursor-pointer transition-colors shrink-0"
          style={{ backgroundColor: 'rgba(255,255,255,0.15)' }}
        >
          <span
            className="material-symbols-outlined text-white text-[18px]"
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            location_on
          </span>
          <div className="flex flex-col leading-none ml-1">
            <span className="text-[10px] text-white/70 font-medium">Deliver to</span>
            <span className="text-[13px] text-white font-semibold">Dhaka, Bangladesh</span>
          </div>
          <span className="material-symbols-outlined text-white text-[16px] ml-1">expand_more</span>
        </div>

        {/* Search bar */}
        <div className="flex-grow max-w-xl">
          <div className="relative">
            <input
              type="text"
              placeholder="Search for restaurants, cuisines, and more..."
              className="w-full bg-white rounded-xl py-3 pl-12 pr-4 text-[14px] text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 transition-all"
              style={{ boxShadow: 'none' }}
            />
            <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-[20px]">
              search
            </span>
          </div>
        </div>

        {/* Right controls */}
        <div className="flex items-center gap-4 ml-auto shrink-0">
          <Link
            to="/brand"
            className="text-white text-[13px] font-semibold hidden lg:block px-3 py-2 rounded-lg hover:bg-white/10 transition-colors"
          >
            Switch to Brand View
          </Link>

          <div className="flex items-center gap-2 pl-4" style={{ borderLeft: '1px solid rgba(255,255,255,0.2)' }}>
            <button className="relative p-2 rounded-full hover:bg-white/10 transition-colors">
              <span className="material-symbols-outlined text-white">shopping_cart</span>
              <span
                className="absolute -top-0.5 -right-0.5 text-[10px] font-bold h-4 w-4 flex items-center justify-center rounded-full"
                style={{ backgroundColor: 'white', color: PINK }}
              >
                2
              </span>
            </button>
            <PersonaSwitcher />
          </div>
        </div>
      </div>
    </header>
  );
}

function HeroBanner() {
  return (
    <section className="max-w-[1200px] mx-auto px-12 mt-8 mb-10">
      <div
        className="relative w-full rounded-[2rem] overflow-hidden"
        style={{ height: '360px' }}
      >
        {/* Gradient background as hero placeholder */}
        <div
          className="absolute inset-0"
          style={{
            background: `linear-gradient(135deg, ${PINK_DARK} 0%, ${PINK} 40%, #FF6B9D 100%)`,
          }}
        />
        <div
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage:
              "url(\"data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E\")",
          }}
        />

        <div className="absolute inset-0 flex items-center px-16">
          <div className="max-w-md text-white">
            <span
              className="px-3 py-1 rounded text-[11px] font-bold mb-4 inline-block"
              style={{ backgroundColor: 'rgba(255,255,255,0.2)' }}
            >
              SPONSORED
            </span>
            <h1 className="text-[42px] font-black leading-tight mb-4">
              Flash Sale:<br />Up to 50% Off!
            </h1>
            <p className="text-[16px] mb-8 opacity-90 leading-relaxed">
              Dhaka's favourite flavours delivered to your door — zero delivery fees today.
            </p>
            <button
              className="flex items-center gap-2 px-8 py-4 rounded-xl font-bold text-[14px] text-white hover:opacity-90 active:scale-95 transition-all"
              style={{ backgroundColor: 'rgba(255,255,255,0.2)', border: '2px solid rgba(255,255,255,0.4)' }}
            >
              Order Now
              <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
            </button>
          </div>
        </div>

        {/* Decorative food emoji circles */}
        <div className="absolute right-12 top-1/2 -translate-y-1/2 flex gap-4 opacity-30">
          {['🍛', '🥘', '🍜'].map((emoji, i) => (
            <div
              key={i}
              className="w-28 h-28 rounded-full bg-white/20 flex items-center justify-center text-[52px]"
              style={{ transform: `translateY(${(i - 1) * 24}px)` }}
            >
              {emoji}
            </div>
          ))}
        </div>

        {/* Carousel dots */}
        <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex gap-2">
          <div className="w-8 h-1.5 bg-white rounded-full" />
          <div className="w-2 h-1.5 bg-white/40 rounded-full" />
          <div className="w-2 h-1.5 bg-white/40 rounded-full" />
        </div>
      </div>
    </section>
  );
}

function CategoryIcons() {
  return (
    <section className="max-w-[1200px] mx-auto px-12 mb-10">
      <div className="flex justify-around md:justify-start gap-8">
        {CATEGORIES.map(({ icon, label }) => (
          <div
            key={label}
            className="flex flex-col items-center gap-3 cursor-pointer group"
          >
            <div
              className="w-20 h-20 rounded-full flex items-center justify-center transition-all group-hover:scale-110 group-hover:shadow-lg"
              style={{ backgroundColor: '#FFECF3' }}
            >
              <span
                className="material-symbols-outlined text-[36px]"
                style={{
                  fontVariationSettings: "'FILL' 1",
                  color: PINK,
                }}
              >
                {icon}
              </span>
            </div>
            <span className="text-[13px] font-semibold text-gray-700">{label}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

function PersonaSummary() {
  const { currentPersona } = usePersona();
  if (!currentPersona) return null;

  const p = currentPersona;
  return (
    <div className="flex justify-center mb-6 opacity-70 hover:opacity-100 transition-opacity">
      <div
        className="flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-gray-200 shadow-sm cursor-pointer text-[13px] text-gray-700"
      >
        <div
          className="w-6 h-6 rounded-full flex items-center justify-center text-white text-[11px] font-bold shrink-0"
          style={{ backgroundColor: PINK }}
        >
          {p.display_name?.[0]}
        </div>
        <span className="font-medium">
          {p.display_name}, {p.age} — {p.city}
        </span>
        <span className="text-gray-400 text-[11px]">
          ({p.occupation_mode?.replace(/_/g, ' ')})
        </span>
        <span className="material-symbols-outlined text-gray-400 text-[16px]">expand_more</span>
      </div>
    </div>
  );
}

export default function FeedPage() {
  return (
    <div className="min-h-screen" style={{ backgroundColor: '#fbf9f9' }}>
      <TopNav />
      <HeroBanner />
      <CategoryIcons />

      {/* Feed column */}
      <div className="max-w-[680px] mx-auto px-4 pb-16">
        <PersonaSummary />
        <Feed />
      </div>

      {/* Footer */}
      <footer
        className="mt-16 py-8 text-center text-[12px] text-white/70"
        style={{ backgroundColor: PINK }}
      >
        <p className="font-bold text-white mb-1">foodpanda · AdPersona AI Demo</p>
        <p>© 2026 Contextual Ad Intelligence Engine · Bangladesh</p>
      </footer>
    </div>
  );
}
