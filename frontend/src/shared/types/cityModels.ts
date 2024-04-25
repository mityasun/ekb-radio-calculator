export interface CityModel {
  id: number;
  default: boolean;
  name: string;
}

export interface CityState {
  cities: CityModel[];
  selectedCity: CityModel | null;
  setCities: (cities: CityModel[]) => void;
  setSelectedCity: (city: CityModel) => void;
}
