import { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getDefaultRadio, getRadioStations } from '../api';
import { useStore } from 'shared/store';
import { RadioModel } from 'shared/types';

export const useDefaultRadios = () => {
  const { selectedCity, selectedRadioId, setSelectedRadio, setSelectedRadioId } = useStore();

  const cityId = selectedCity?.id as number | null;

  const { data: radios, isLoading } = useQuery({
    queryKey: ['radios', cityId],
    queryFn: () => getRadioStations(cityId),
    enabled: !!cityId
  });

  const { data: radioFull } = useQuery({
    queryKey: ['radio', selectedRadioId],
    queryFn: () => getDefaultRadio(selectedRadioId)
  });

  useEffect(() => {
    if (!radios) return;

    const defaultRadio: RadioModel = radios.find((radio: RadioModel) => radio.default === true) || radios[0];

    if (defaultRadio) {
      setSelectedRadioId(defaultRadio.id);
    } else {
      setSelectedRadioId(null);
      setSelectedRadio(null);
    }
  }, [radios]);

  useEffect(() => {
    if (!radioFull) return;

    if (radioFull.id) {
      setSelectedRadioId(radioFull.id);
      setSelectedRadio(radioFull);
    } else {
      setSelectedRadio(null);
    }
  }, [radioFull?.id]);

  return { radios, isLoading };
};
