import axios from 'axios';
import { apiBaseUrl } from 'shared/constants/apiBaseUrl';
import { RadioFullModel, RadioModel } from 'shared/types';

export const getRadioStations = async (cityId: number | null): Promise<RadioModel[] | []> => {
  if (!cityId) return [];
  const response = await axios.get(`${apiBaseUrl}/api/stations/?city=${cityId}`);
  return response ? response.data.results : [];
};

export const getDefaultRadio = async (radioId: number | null): Promise<RadioFullModel | null> => {
  if (!radioId) return null;
  const response = await axios.get(`${apiBaseUrl}/api/stations/${radioId}/`);
  return response ? response.data : {};
};
