import { create } from 'zustand';
import { RadioModel, RadioState, RadioFullModel } from '../types';

const useRadioStore = create<RadioState>()((set) => ({
  radios: [],
  selectedRadio: null,
  selectedRadioId: null,
  setRadios: (radios: RadioModel[]) => set({ radios }),
  setSelectedRadio: (radio: RadioFullModel | null) => set({ selectedRadio: radio }),
  setSelectedRadioId: (radioId: number | null) => set({ selectedRadioId: radioId })
}));

export { useRadioStore };
