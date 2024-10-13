import { useCallback, useEffect } from 'react';
import { AppSelect } from 'shared/ui/appSelect';
import { useStore } from 'shared/store';
import { AudioDuration, AppSelectOption } from 'shared/types';
import { AUDIO_DURATION_CONTENT_TEXT, maxWidth } from '../configs';

export const DurationSelect = () => {
  const appSettings = useStore((state) => state.appSettings);
  const audioDurations = useStore((state) => state.audioDurations);
  const setAudioDuration = useStore((state) => state.setAudioDuration);
  const customer_selection = useStore((state) => state.customer_selection);

  useEffect(() => {
    if (!audioDurations) return;

    const defaultAudioDuration =
      audioDurations.find((duration: AudioDuration) => duration.default) || audioDurations[0];

    const isAudioDurationFound = Boolean(
      audioDurations.find((duration: AudioDuration) => appSettings.audio_duration?.id === duration.id)
    );

    if (!defaultAudioDuration || customer_selection.length > 0 || isAudioDurationFound) return;
    setAudioDuration(defaultAudioDuration);
  }, [audioDurations, customer_selection.length]);

  const options =
    audioDurations?.map((duration: AudioDuration) => ({
      value: duration.id.toString(),
      label: duration.audio_duration + AUDIO_DURATION_CONTENT_TEXT.UNIT_SEC
    })) || [];

  const getValue = useCallback(() => {
    return appSettings.audio_duration
      ? options.find((duration) => duration.value.toString() === (appSettings.audio_duration?.id || '').toString())
      : null;
  }, [appSettings, options]);

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
      placeholder={!audioDurations ? AUDIO_DURATION_CONTENT_TEXT.LOADING : AUDIO_DURATION_CONTENT_TEXT.SELECT_DURATION}
      maxWidth={maxWidth}
      options={options}
      onChange={onChange}
      value={getValue()}
    />
  );
};
