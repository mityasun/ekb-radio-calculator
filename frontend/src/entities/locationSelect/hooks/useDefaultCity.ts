import { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getCities } from '../api';
import { useCityStore } from 'shared/store';

export const useDefaultCity = () => {
  const { data } = useQuery({ queryKey: ['cities'], queryFn: getCities });
  const { setCities, setSelectedCity } = useCityStore();

  useEffect(() => {
    if (!data) return;
    setCities(data);

    const defaultCity = data.find((city) => city.default);
    if (!defaultCity) return;
    setSelectedCity(defaultCity);
  }, [data]);
};
