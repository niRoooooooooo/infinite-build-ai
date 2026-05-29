import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { listBrands } from '../api/brands';

const BrandContext = createContext(null);

export function BrandProvider({ children }) {
  const [brands, setBrands] = useState([]);
  const [currentBrand, setCurrentBrand] = useState(null);
  const [loading, setLoading] = useState(true);

  const refreshBrands = useCallback(async () => {
    try {
      const data = await listBrands();
      setBrands(data);
    } catch (err) {
      console.error('Failed to load brands:', err);
    }
  }, []);

  useEffect(() => {
    setLoading(true);
    refreshBrands().finally(() => setLoading(false));
  }, [refreshBrands]);

  return (
    <BrandContext.Provider value={{ brands, currentBrand, setCurrentBrand, refreshBrands, loading }}>
      {children}
    </BrandContext.Provider>
  );
}

export function useBrand() {
  return useContext(BrandContext);
}

export default BrandContext;
