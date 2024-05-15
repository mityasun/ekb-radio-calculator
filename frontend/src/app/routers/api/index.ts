import axios from 'axios';
import { apiBaseUrl } from 'shared/constants/apiBaseUrl';
import { SystemText } from 'shared/types';

export const getSystemText = async (): Promise<SystemText> => {
  const response = await axios.get(`${apiBaseUrl}/api/system-texts/1/`);
  return response.data;
};
