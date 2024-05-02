import { create } from 'zustand';
import {
  AppSettings,
  StoreState,
  AdMonth,
  AudioDuration,
  BlockPosition,
  TimeInterval,
  RadioFullModel,
  CityModel,
  CustomerSelection
} from 'shared/types';
import { getAudioDurations, getBlockPositions, getTimeIntervals } from 'shared/utils';

const initState = {
  hour_selected_rate: false,
  other_person_rate: false
};

const useStore = create<StoreState>()((set) => ({
  appSettings: initState,
  audioDurations: null,
  timeIntervals: null,
  blockPositions: null,
  selectedRadio: null,
  selectedRadioId: null,
  selectedCity: null,
  customer_selection: [],
  setAppSettings: (appSettings: AppSettings) => set({ appSettings }),
  setAudioDurations: (audioDurations: AudioDuration[]) => set({ audioDurations }),
  setTimeIntervals: (timeIntervals: TimeInterval[]) => set({ timeIntervals }),
  setBlockPositions: (blockPositions: BlockPosition[]) => set({ blockPositions }),
  setAudioDuration: (audioDuration: AudioDuration) =>
    set((state) => ({ appSettings: { ...state.appSettings, audio_duration: audioDuration } })),
  setBlockPosition: (blockPosition: BlockPosition) =>
    set((state) => ({ appSettings: { ...state.appSettings, block_position: blockPosition } })),
  setMonth: (month: AdMonth) => set((state) => ({ appSettings: { ...state.appSettings, month } })),
  setHourSelection: (hourSelection: boolean) =>
    set((state) => ({ appSettings: { ...state.appSettings, hour_selected_rate: hourSelection } })),
  setOtherPerson: (otherPerson: boolean) =>
    set((state) => ({ appSettings: { ...state.appSettings, other_person_rate: otherPerson } })),
  setSelectedRadio: (radio: RadioFullModel | null) => {
    set({ selectedRadio: radio });
    if (radio && radio.interval_price) {
      set({ audioDurations: getAudioDurations(radio.interval_price) });
      set({ blockPositions: getBlockPositions(radio.block_position_rate) });
      set({ timeIntervals: getTimeIntervals(radio.interval_price) });
    }
  },
  setSelectedRadioId: (radioId: number | null) => set({ selectedRadioId: radioId }),
  setSelectedCity: (city: CityModel | null) => set({ selectedCity: city }),
  setCustomerSelection: (customer_selection: CustomerSelection) =>
    set((state) => ({ customer_selection: [...state.customer_selection, customer_selection] })),
  deleteCustomerSelection: (customer_selection: CustomerSelection) =>
    set((state) => ({
      customer_selection: state.customer_selection?.filter(
        (selection) =>
          selection.date !== customer_selection.date || selection.time_interval !== customer_selection.time_interval
      )
    })),
  clearCustomerSelections: () => set({ customer_selection: [] })
}));

export { useStore };
