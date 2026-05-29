import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { listPersonas } from '../api/personas';

const PersonaContext = createContext(null);

export function PersonaProvider({ children }) {
  const [personas, setPersonas] = useState([]);
  const [currentPersona, setCurrentPersona] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listPersonas()
      .then((data) => {
        setPersonas(data);
        setCurrentPersona(data[0] ?? null);
      })
      .catch((err) => console.error('Failed to load personas:', err))
      .finally(() => setLoading(false));
  }, []);

  const selectPersona = useCallback((personaId) => {
    const found = personas.find((p) => p.persona_id === personaId);
    if (found) setCurrentPersona(found);
  }, [personas]);

  return (
    <PersonaContext.Provider value={{ personas, currentPersona, setCurrentPersona: selectPersona, loading }}>
      {children}
    </PersonaContext.Provider>
  );
}

export function usePersona() {
  return useContext(PersonaContext);
}

export default PersonaContext;
