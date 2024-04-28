import { useCallback, useEffect } from 'react';
import { AppSelect } from 'shared/ui/appSelect';
import { useAdSettingsStore } from 'shared/store';
import { AudioDuration, AppSelectOption } from 'shared/types';

const maxWidth = '100%';

export const AdDurationSelector = () => {
  const { adSettings, audioDurations, setAudioDuration } = useAdSettingsStore();

  useEffect(() => {
    if (!audioDurations) return;

    const defaultAudioDuration =
      audioDurations.find((duration: AudioDuration) => duration.default) || audioDurations[0];

    if (!defaultAudioDuration) return;
    setAudioDuration(defaultAudioDuration);
  }, [audioDurations]);

  const options =
    audioDurations?.map((duration: AudioDuration) => ({
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
      const selectedDuration = audioDurations?.find(
        (duration: AudioDuration) => duration.id.toString() === (newValue as AppSelectOption).value
      );
      if (selectedDuration) {
        setAudioDuration(selectedDuration);
      }
    },
    [audioDurations]
  );

  return (
    <AppSelect
      placeholder={!audioDurations ? 'Загрузка...' : 'Выберите продолжительность'}
      maxWidth={maxWidth}
      options={options}
      onChange={onChange}
      value={getValue()}
    />
  );
};
