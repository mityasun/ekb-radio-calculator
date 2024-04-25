import { mockData, mockStationData } from './mockData';

export const getRadioStations = async (cityId: number | null) => {
  const response = mockData.filter((city) => city.cityId === cityId)[0];
  return response ? response.radios : [];
};

export const getDefaultRadio = async (radioId: number | null) => {
  const response = mockStationData.id === radioId ? mockStationData : null;
  return response;
};
