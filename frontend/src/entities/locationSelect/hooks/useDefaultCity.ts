import { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getCities } from '../api';
import { useCityStore } from 'shared/store';
import { CityModel } from 'shared/types';

export const useDefaultCity = () => {
  const { data, isLoading } = useQuery({ queryKey: ['cities'], queryFn: getCities });
  const { setCities, setSelectedCity } = useCityStore();

  useEffect(() => {
    if (!data) return;
    setCities(data);

    const defaultCity = data.find((city: CityModel) => city.default) || data[0];

    if (!defaultCity) return;
    setSelectedCity(defaultCity);
  }, [data]);

  return { isLoading };
};
