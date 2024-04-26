import axios from 'axios';
import { apiBaseUrl } from 'shared/constants/apiBaseUrl';

export const getBlockPositions = async () => {
  const response = await axios.get(`${apiBaseUrl}/api/block-positions/`);
  return response.data.results;
};
