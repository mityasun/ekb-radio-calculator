import { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getDefaultRadio, getRadioStations } from '../api';
import { useCityStore, useRadioStore } from 'shared/store';
import { RadioFullModel, RadioModel } from 'shared/types';

export const useDefaultRadios = () => {
  const cityId = useCityStore((state) => state.selectedCity)?.id as number | null;
  const { selectedRadioId, setRadios, setSelectedRadio, setSelectedRadioId } = useRadioStore();

  const { data: radios, isLoading } = useQuery({
    queryKey: ['radios', cityId],
    queryFn: () => getRadioStations(cityId),
    enabled: !!cityId
  });

  const radioFull =
    (useQuery({
      queryKey: ['radio', selectedRadioId],
      queryFn: () => getDefaultRadio(selectedRadioId)
    }).data as RadioFullModel | undefined) || null;

  useEffect(() => {
    if (!radios) return;
    setRadios(radios);

    const defaultRadio: RadioModel = radios.find((radio: RadioModel) => radio.default === true) || radios[0];

    if (defaultRadio) {
      setSelectedRadioId(defaultRadio.id);
    } else {
      setSelectedRadioId(null);
    }
  }, [radios]);

  useEffect(() => {
    if (radioFull?.id) {
      setSelectedRadioId(radioFull?.id);
      setSelectedRadio(radioFull);
    } else {
      setSelectedRadio(null);
    }
  }, [radioFull?.id]);

  return { isLoading };
};
