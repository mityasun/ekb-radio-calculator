import { create } from 'zustand';
import { AdDuration, AdSettings, AdSettingsState, AdBlockPosition, AdMonth } from 'shared/types';

const initState = {
  hour_selected_rate: false,
  other_person_rate: false
};

const useAdSettings = create<AdSettingsState>()((set) => ({
  adSettings: initState,
  setAdSettings: (adSettings: AdSettings) => set({ adSettings }),
  setAudioDuration: (audioDuration: AdDuration) =>
    set((state) => ({ adSettings: { ...state.adSettings, audio_duration: audioDuration } })),
  setBlockPosition: (blockPosition: AdBlockPosition) =>
    set((state) => ({ adSettings: { ...state.adSettings, block_position: blockPosition } })),
  setMonth: (month: AdMonth) => set((state) => ({ adSettings: { ...state.adSettings, month } })),
  setHourSelection: (hourSelection: boolean) =>
    set((state) => ({ adSettings: { ...state.adSettings, hour_selected_rate: hourSelection } })),
  setOtherPerson: (otherPerson: boolean) =>
    set((state) => ({ adSettings: { ...state.adSettings, other_person_rate: otherPerson } }))
}));

export { useAdSettings };
