import axios from 'axios';
import { apiBaseUrl } from 'shared/constants/apiBaseUrl';

export const getCities = async () => {
  const response = await axios.get(`${apiBaseUrl}/api/cities/`);
  return response.data.results;
};
