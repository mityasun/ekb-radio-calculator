import { useCallback, useEffect } from 'react';
import { AppSelect, AppSelectOption } from 'shared/ui/appSelect';
import { useAdSettingsStore } from 'shared/store';
import { getAudioDurations } from '../api';
import { useQuery } from '@tanstack/react-query';
import { AdDuration } from 'shared/types';

const maxWidth = '100%';

export const AdDurationSelector = () => {
  const { adSettings, setAudioDuration } = useAdSettingsStore();
  const { data, isLoading } = useQuery({ queryKey: ['audio-durations'], queryFn: getAudioDurations });

  useEffect(() => {
    if (!data) return;

    const defaultAudioDuration = data.find((duration: AdDuration) => duration.default) || data[0];

    if (!defaultAudioDuration) return;
    setAudioDuration(defaultAudioDuration);
  }, [data]);

  const options =
    data?.map((duration: AdDuration) => ({
      value: duration.id.toString(),
      label: duration.audio_duration + ' сек'
    })) || [];

  const getValue = useCallback(() => {
    return adSettings.audio_duration
      ? options.find((duration) => duration.value.toString() === (adSettings.audio_duration?.id || '').toString())
      : null;
  }, [adSettings, options]);

  const onChange = useCallback(
    (newValue: unknown) => {
      const selectedDuration = data?.find(
        (duration: AdDuration) => duration.id.toString() === (newValue as AppSelectOption).value
      );
      if (selectedDuration) {
        setAudioDuration(selectedDuration);
      }
    },
    [data]
  );

  return (
    <AppSelect
      placeholder={isLoading ? 'Загрузка...' : 'Выберите продолжительность'}
      maxWidth={maxWidth}
      options={options}
      onChange={onChange}
      value={getValue()}
    />
  );
};
