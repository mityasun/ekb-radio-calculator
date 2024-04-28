import { create } from 'zustand';
import {
  AdSettings,
  AdSettingsState,
  AdMonth,
  AudioDuration,
  BlockPosition,
  TimeInterval,
  RadioFullModel
} from 'shared/types';
import { getAudioDurations, getBlockPositions } from 'shared/utils';

const initState = {
  hour_selected_rate: false,
  other_person_rate: false
};

const useAdSettingsStore = create<AdSettingsState>()((set) => ({
  adSettings: initState,
  audioDurations: null,
  timeIntervals: null,
  blockPositions: null,
  selectedRadio: null,
  selectedRadioId: null,
  setAdSettings: (adSettings: AdSettings) => set({ adSettings }),
  setAudioDurations: (audioDurations: AudioDuration[]) => set({ audioDurations }),
  setTimeIntervals: (timeIntervals: TimeInterval[]) => set({ timeIntervals }),
  setBlockPositions: (blockPositions: BlockPosition[]) => set({ blockPositions }),
  setAudioDuration: (audioDuration: AudioDuration) =>
    set((state) => ({ adSettings: { ...state.adSettings, audio_duration: audioDuration } })),
  setBlockPosition: (blockPosition: BlockPosition) =>
    set((state) => ({ adSettings: { ...state.adSettings, block_position: blockPosition } })),
  setMonth: (month: AdMonth) => set((state) => ({ adSettings: { ...state.adSettings, month } })),
  setHourSelection: (hourSelection: boolean) =>
    set((state) => ({ adSettings: { ...state.adSettings, hour_selected_rate: hourSelection } })),
  setOtherPerson: (otherPerson: boolean) =>
    set((state) => ({ adSettings: { ...state.adSettings, other_person_rate: otherPerson } })),
  setSelectedRadio: (radio: RadioFullModel | null) => {
    set({ selectedRadio: radio });
    if (radio && radio.interval_price) {
      set({ audioDurations: getAudioDurations(radio.interval_price) });
      set({ blockPositions: getBlockPositions(radio.block_position_rate) });
    }
  },
  setSelectedRadioId: (radioId: number | null) => set({ selectedRadioId: radioId })
}));

export { useAdSettingsStore };
