import axios from 'axios';
import { apiBaseUrl } from 'shared/constants/apiBaseUrl';
import { TimeInterval } from 'shared/types';

export const getTimeIntervals = async (): Promise<TimeInterval[]> => {
  const response = await axios.get(`${apiBaseUrl}/api/time-intervals/`);
  return response.data.results;
};
