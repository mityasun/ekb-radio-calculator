import { CityModel } from './cityModels';

export type RadioModel = {
  id: number;
  default: boolean;
  name: string;
};

export type AudienceSex = {
  sex: 'Женщины' | 'Мужчины';
  percent: number;
};

export type AudienceAge = {
  age: string;
  percent: number;
};

export type MonthRate = {
  id: number;
  rate: number;
};

export type BlockPosition = {
  id: number;
  block_position: string;
  default: boolean;
};

export type BlockPositionRate = {
  block_position: BlockPosition;
  rate: number;
};

export type TimeInterval = {
  id: number;
  time_interval: string;
};

export type AudioDuration = {
  id: number;
  audio_duration: number;
  default: boolean;
};

export type IntervalPrice = {
  time_interval: TimeInterval;
  audio_duration: AudioDuration;
  interval_price: number;
};

export type AmountDiscount = {
  order_amount: number;
  discount: number;
};

export type DayDiscount = {
  total_days: number;
  discount: number;
};

export type VolumeDiscount = {
  order_volume: number;
  discount: number;
};

export interface RadioFullModel extends RadioModel {
  title: string;
  description: string;
  city: CityModel;
  broadcast_zone: string;
  reach_dly: number | null;
  reach_dly_percent: number | null;
  other_person_rate: number;
  hour_selected_rate: number;
  logo: string;
  audience_sex: AudienceSex[] | [];
  audience_age: AudienceAge[] | [];
  month_rate: MonthRate[];
  block_position_rate: BlockPositionRate[];
  interval_price: IntervalPrice[];
  amount_discount: AmountDiscount[];
  days_discount: DayDiscount[] | [];
  volume_discount: VolumeDiscount[] | [];
}
