import { usePersona } from '../../../context/PersonaContext';

export default function PersonaSwitcher() {
  const { personas, currentPersona, setCurrentPersona } = usePersona();

  if (!currentPersona) return null;

  return (
    <div className="relative flex items-center">
      <div className="relative">
        <select
          value={currentPersona.persona_id}
          onChange={(e) => setCurrentPersona(e.target.value)}
          className="appearance-none pl-3 pr-8 py-2 rounded-xl text-[13px] font-semibold text-white cursor-pointer focus:outline-none"
          style={{ backgroundColor: 'rgba(255,255,255,0.15)', border: '1px solid rgba(255,255,255,0.25)' }}
        >
          {personas.map((p) => (
            <option
              key={p.persona_id}
              value={p.persona_id}
              style={{ backgroundColor: '#D70F64', color: '#fff' }}
            >
              {p.display_name}, {p.age} — {p.city}
            </option>
          ))}
        </select>
        <span
          className="material-symbols-outlined absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none text-white text-[16px]"
        >
          expand_more
        </span>
      </div>
    </div>
  );
}
