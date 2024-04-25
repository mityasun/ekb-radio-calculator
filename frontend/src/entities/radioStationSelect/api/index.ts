import axios from 'axios';
import { apiBaseUrl } from 'shared/constants/apiBaseUrl';

export const getRadioStations = async (cityId: number | null) => {
  if (!cityId) return [];
  const response = await axios.get(`${apiBaseUrl}/api/stations?city=${cityId}`);
  return response ? response.data.results : [];
};

export const getDefaultRadio = async (radioId: number | null) => {
  if (!radioId) return {};
  const response = await axios.get(`${apiBaseUrl}/api/stations/${radioId}`);
  return response ? response.data : {};
};
