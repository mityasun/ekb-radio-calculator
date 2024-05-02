import { CityModel } from './cityModels';
import { CustomerSelection } from './orderModel';
import { AudioDuration, BlockPosition, RadioFullModel, TimeInterval } from './radioModels';

export interface AppSettings {
  audio_duration?: AudioDuration;
  block_position?: BlockPosition;
  month?: AdMonth;
  hour_selected_rate?: boolean;
  other_person_rate?: boolean;
}

export interface AdMonth {
  id: number;
  month: string;
  default: boolean;
}

export interface StoreState {
  appSettings: AppSettings;
  audioDurations: AudioDuration[] | null;
  blockPositions: BlockPosition[] | null;
  timeIntervals: TimeInterval[] | null;
  selectedRadioId: number | null;
  selectedRadio: RadioFullModel | null;
  selectedCity: CityModel | null;
  customer_selection: CustomerSelection[] | [];
  setSelectedRadio: (radio: RadioFullModel | null) => void;
  setSelectedRadioId: (radioId: number | null) => void;
  setAppSettings: (appSettings: AppSettings) => void;
  setAudioDurations: (audioDurations: AudioDuration[]) => void;
  setBlockPositions: (blockPositions: BlockPosition[]) => void;
  setTimeIntervals: (timeIntervals: TimeInterval[]) => void;
  setAudioDuration: (audioDuration: AudioDuration) => void;
  setBlockPosition: (blockPosition: BlockPosition) => void;
  setMonth: (month: AdMonth) => void;
  setHourSelection: (hourSelection: boolean) => void;
  setOtherPerson: (otherPerson: boolean) => void;
  setSelectedCity: (city: CityModel | null) => void;
  setCustomerSelection: (customer_selection: CustomerSelection) => void;
  deleteCustomerSelection: (customer_selection: CustomerSelection) => void;
  clearCustomerSelections: () => void;
}
