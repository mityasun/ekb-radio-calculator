export interface AdSettings {
  audio_duration?: AdDuration;
  block_position?: AdBlockPosition;
  month?: AdMonth;
  hour_selected_rate?: boolean;
  other_person_rate?: boolean;
}

export interface AdDuration {
  id: number;
  audio_duration: number;
  default: boolean;
}

export interface AdBlockPosition {
  id: number;
  block_position: number;
  default: boolean;
}

export interface AdDurationOptions {
  value: number;
  label: string;
}

export interface AdBlockPositionOptions {
  value: number;
  label: string;
}

export interface AdMonth {
  id: number;
  month: string;
  default: boolean;
}

export interface AdMonthOptions {
  value: number;
  label: string;
}

export interface AdSettingsState {
  adSettings: AdSettings;
  setAdSettings: (adSettings: AdSettings) => void;
  setAudioDuration: (audioDuration: AdDuration) => void;
  setBlockPosition: (blockPosition: AdBlockPosition) => void;
  setMonth: (month: AdMonth) => void;
  setHourSelection: (hourSelection: boolean) => void;
  setOtherPerson: (otherPerson: boolean) => void;
}
