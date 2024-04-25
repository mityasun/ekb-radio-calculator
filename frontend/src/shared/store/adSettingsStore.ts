import { create } from 'zustand';
import { AdSettings, AdSettingsState } from 'shared/types';

const useAdSettings = create<AdSettingsState>()((set) => ({
  adSettings: {},
  setAdSettings: (adSettings: AdSettings) => set({ adSettings }),
  setAudioDuration: (audioDuration: number) =>
    set((state) => ({ adSettings: { ...state.adSettings, audio_duration: audioDuration } })),
  setBlockPosition: (blockPosition: string) =>
    set((state) => ({ adSettings: { ...state.adSettings, block_position: blockPosition } })),
  setMonth: (month: string) => set((state) => ({ adSettings: { ...state.adSettings, month } })),
  setGuaranteedHour: (hourSelection: boolean) =>
    set((state) => ({ adSettings: { ...state.adSettings, hour_selection: hourSelection } })),
  setThirdParty: (otherPerson: boolean) =>
    set((state) => ({ adSettings: { ...state.adSettings, other_person: otherPerson } }))
}));

export { useAdSettings };
