import axios from 'axios';
import { apiBaseUrl } from 'shared/constants/apiBaseUrl';
import { AdDuration } from 'shared/types';

export const getAudioDurations = async (): Promise<AdDuration[]> => {
  const response = await axios.get(`${apiBaseUrl}/api/audio-durations/`);
  return response.data.results;
};
