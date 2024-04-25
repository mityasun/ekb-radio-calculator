import { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getDefaultRadio, getRadioStations } from '../api';
import { useCityStore, useRadioStore } from 'shared/store';
import { RadioFullModel } from 'shared/types';

export const useDefaultRadios = () => {
  const cityId = useCityStore((state) => state.selectedCity)?.id as number | null;
  const { selectedRadioId, setRadios, setSelectedRadio, setSelectedRadioId } = useRadioStore();

  const radios = useQuery({
    queryKey: ['radios', cityId],
    queryFn: () => getRadioStations(cityId),
    enabled: !!cityId
  }).data;

  const radioFull =
    (useQuery({
      queryKey: ['radio', selectedRadioId],
      queryFn: () => getDefaultRadio(selectedRadioId)
    }).data as RadioFullModel | undefined) || null;

  console.log('Это selectedRadio ' + radioFull);

  useEffect(() => {
    if (!radios) return;
    setRadios(radios);

    const defaultRadio = radios.find((radio) => radio.default === true);

    if (defaultRadio) {
      setSelectedRadioId(defaultRadio.id);
    }
  }, [radios]);

  console.log(selectedRadioId);

  useEffect(() => {
    if (radioFull?.id) {
      setSelectedRadioId(radioFull?.id);
      setSelectedRadio(radioFull);
    } else {
      setSelectedRadio(null);
    }
  }, [radioFull?.id]);
};
