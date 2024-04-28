import axios from 'axios';
import { apiBaseUrl } from 'shared/constants/apiBaseUrl';
import { CityModel } from 'shared/types';

export const getCities = async (): Promise<CityModel[] | null> => {
  const response = await axios.get(`${apiBaseUrl}/api/cities/`);
  return response.data.results;
};
