import { createContext, useContext } from 'react'

const PersonaContext = createContext(null)

export function PersonaProvider({ children }) {
  return (
    <PersonaContext.Provider value={null}>
      {children}
    </PersonaContext.Provider>
  )
}

export function usePersona() {
  return useContext(PersonaContext)
}

export default PersonaContext
