import { IntervalPrice } from 'shared/types';

export const getAudioDurations = (intervalPrice: IntervalPrice[]) => {
  return intervalPrice
    .map((item) => {
      return {
        id: item.audio_duration.id,
        default: item.audio_duration.default,
        audio_duration: item.audio_duration.audio_duration
      };
    })
    .filter(
      (value, index, self) =>
        self.findIndex(
          (item) =>
            item.id === value.id && item.default === value.default && item.audio_duration === value.audio_duration
        ) === index
    );
};
