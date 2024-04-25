import axios from 'axios';
import { apiBaseUrl } from 'shared/constants/apiBaseUrl';

export const getAudioDurations = async () => {
  const response = await axios.get(`${apiBaseUrl}/api/audio-durations/`);
  return response.data.results;
};
