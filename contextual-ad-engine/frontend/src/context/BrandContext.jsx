import { createContext, useContext } from 'react'

const BrandContext = createContext(null)

export function BrandProvider({ children }) {
  return (
    <BrandContext.Provider value={null}>
      {children}
    </BrandContext.Provider>
  )
}

export function useBrand() {
  return useContext(BrandContext)
}

export default BrandContext
