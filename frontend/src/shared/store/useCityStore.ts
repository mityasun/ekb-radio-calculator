import { create } from 'zustand';
import { CityModel, CityState } from '../types';

const useCityStore = create<CityState>()((set) => ({
  selectedCity: null,
  setSelectedCity: (city: CityModel | null) => set({ selectedCity: city })
}));

export { useCityStore };
