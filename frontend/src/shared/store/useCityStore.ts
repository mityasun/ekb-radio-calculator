import { create } from 'zustand';
import { CityModel, CityState } from '../types';

const useCityStore = create<CityState>()((set) => ({
  cities: [],
  selectedCity: null,
  setCities: (cities: CityModel[]) => set({ cities }),
  setSelectedCity: (city: CityModel) => set({ selectedCity: city })
}));

export { useCityStore };
