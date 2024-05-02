import { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getCities } from '../api';
import { useStore } from 'shared/store';
import { CityModel } from 'shared/types';

export const useDefaultCity = () => {
  const { data: cities, isLoading } = useQuery({ queryKey: ['cities'], queryFn: getCities });
  const { setSelectedCity } = useStore();

  useEffect(() => {
    if (!cities) return;

    const defaultCity = cities.find((city: CityModel) => city.default) || cities[0];

    if (!defaultCity) return;
    setSelectedCity(defaultCity);
  }, [cities]);

  return { isLoading, cities };
};
