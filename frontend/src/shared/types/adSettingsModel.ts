export interface AdSettings {
  audio_duration?: AdDuration;
  block_position?: string;
  month?: string;
  hour_selection?: boolean;
  other_person?: boolean;
}

export interface AdSettingsState {
  adSettings: AdSettings;
  setAdSettings: (adSettings: AdSettings) => void;
  setAudioDuration: (audioDuration: number) => void;
  setBlockPosition: (blockPosition: string) => void;
  setMonth: (month: string) => void;
  setGuaranteedHour: (hourSelection: boolean) => void;
  setThirdParty: (otherPerson: boolean) => void;
}

export interface AdDuration {
  id: number;
  audio_duration: number;
  default: boolean;
}

export interface AdDurationOptions {
  value: number;
  label: string;
}
