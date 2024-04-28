export interface CityModel {
  id: number;
  default: boolean;
  name: string;
}

export interface CityState {
  selectedCity: CityModel | null;
  setSelectedCity: (city: CityModel) => void;
}
